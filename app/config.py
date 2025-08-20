"""
Configuration classes for different environments
"""
import os
from datetime import timedelta


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    DATABASE_FILE = os.environ.get('DATABASE_FILE') or 'weather_data.db'
    
    # Flask configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # API configuration
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', 10))
    MAX_CITY_LENGTH = int(os.environ.get('MAX_CITY_LENGTH', 50))
    
    # Plotting configuration
    PLOT_MAX_ENTRIES = int(os.environ.get('PLOT_MAX_ENTRIES', 10))
    STATIC_FOLDER = 'static'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_FILE = ':memory:'  # Use in-memory database for tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
