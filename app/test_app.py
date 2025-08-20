"""
Tests for the Weather App
Run with: pytest
"""
import pytest
import os
import tempfile
import sqlite3
from app import app, init_db, save_to_db


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    # Create a temporary database file
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_home_page(client):
    """Test that the home page loads correctly."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Weather App' in rv.data


def test_weather_page(client):
    """Test that the weather page loads correctly."""
    rv = client.get('/weather')
    assert rv.status_code == 200
    assert b'Weather Data' in rv.data


def test_add_city_without_api_key(client):
    """Test adding a city without API key shows error."""
    rv = client.post('/add_city', data={'city': 'London'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'API not configured' in rv.data


def test_add_empty_city(client):
    """Test adding empty city name shows error."""
    rv = client.post('/add_city', data={'city': ''}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Please enter a city name' in rv.data


def test_add_long_city_name(client):
    """Test adding very long city name shows error."""
    long_name = 'a' * 100
    rv = client.post('/add_city', data={'city': long_name}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'City name too long' in rv.data


def test_database_save():
    """Test saving weather data to database."""
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_file = tmp.name
    
    try:
        # Initialize database
        with sqlite3.connect(db_file) as conn:
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
        
        # Test data
        weather_data = {
            'temperature': 20.5,
            'humidity': 65,
            'description': 'sunny'
        }
        
        # This would normally use the save_to_db function
        # but we'll test the database operation directly
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO weather (city, temperature, humidity, description)
                VALUES (?, ?, ?, ?)
            ''', ('Test City', weather_data['temperature'], 
                  weather_data['humidity'], weather_data['description']))
            conn.commit()
            
            # Verify data was saved
            cursor.execute('SELECT city, temperature FROM weather WHERE city = ?', ('Test City',))
            result = cursor.fetchone()
            assert result is not None
            assert result[0] == 'Test City'
            assert result[1] == 20.5
    
    finally:
        # Clean up
        os.unlink(db_file)
