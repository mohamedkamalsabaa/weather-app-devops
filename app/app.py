from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
import requests
import matplotlib.pyplot as plt
import io
import os
import logging
from datetime import datetime
from config import config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# Configuration shortcuts
DB_FILE = app.config['DATABASE_FILE']
API_KEY = app.config['OPENWEATHER_API_KEY']
MAX_CITY_LENGTH = app.config['MAX_CITY_LENGTH']
API_TIMEOUT = app.config['API_TIMEOUT']
PLOT_MAX_ENTRIES = app.config['PLOT_MAX_ENTRIES']

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure static directory exists
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

# Ensure database exists
def init_db():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    temperature REAL,
                    humidity INTEGER,
                    description TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_city', methods=['POST'])
def add_city():
    city = request.form.get('city', '').strip()
    
    # Input validation
    if not city:
        flash('Please enter a city name', 'error')
        return redirect(url_for('home'))
    
    if len(city) > MAX_CITY_LENGTH:
        flash('City name too long', 'error')
        return redirect(url_for('home'))
    
    # Check if API key is configured
    if not API_KEY:
        flash('Weather API not configured. Please set OPENWEATHER_API_KEY environment variable.', 'error')
        return redirect(url_for('home'))

    # Fetch weather data
    weather_data = fetch_weather(city)
    if weather_data:
        save_to_db(city, weather_data)
        flash(f'Weather data for {city} added successfully!', 'success')
    else:
        flash(f'Could not fetch weather data for {city}. Please check the city name.', 'error')

    return redirect(url_for('home'))

@app.route('/weather')
def weather():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT city, temperature, humidity, description, timestamp FROM weather ORDER BY timestamp DESC')
            data = cursor.fetchall()
        return render_template('weather.html', weather_data=data)
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        flash('Error retrieving weather data', 'error')
        return redirect(url_for('home'))

@app.route('/plot')
def plot():
    try:
        # Generate a plot of weather data
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT city, temperature FROM weather ORDER BY timestamp DESC LIMIT ?', (PLOT_MAX_ENTRIES,))
            data = cursor.fetchall()

        if not data:
            flash('No weather data available for plotting', 'error')
            return redirect(url_for('home'))

        cities = [row[0] for row in data]
        temperatures = [row[1] for row in data]

        plt.figure(figsize=(10, 6))
        plt.bar(cities, temperatures, color='skyblue')
        plt.title(f'City Temperatures (Latest {PLOT_MAX_ENTRIES} Entries)')
        plt.xlabel('City')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plot_path = os.path.join(app.config['STATIC_FOLDER'], 'plot.png')
        plt.savefig(plot_path)
        plt.close()  # Important: close the figure to free memory
        
        return send_file(plot_path, mimetype='image/png')
    except Exception as e:
        logger.error(f"Error generating plot: {e}")
        flash('Error generating temperature plot', 'error')
        return redirect(url_for('home'))

def fetch_weather(city):
    try:
        if not API_KEY:
            logger.error("API key not configured")
            return None
            
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        # Check if the response contains valid data
        if 'main' not in data or 'weather' not in data:
            logger.error(f"Invalid response format for city: {city}")
            return None

        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching weather data for {city}: {e}")
        return None
    except KeyError as e:
        logger.error(f"Missing data in API response for {city}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching weather data for {city}: {e}")
        return None

def save_to_db(city, weather_data):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO weather (city, temperature, humidity, description)
                VALUES (?, ?, ?, ?)
            ''', (city, weather_data['temperature'], weather_data['humidity'], weather_data['description']))
            conn.commit()
            logger.info(f"Weather data saved for city: {city}")
    except Exception as e:
        logger.error(f"Error saving weather data for {city}: {e}")
        raise

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
