# Makefile for Weather App
# Use with: make <target>

.PHONY: help install test run docker-build docker-run clean

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  run         - Run the application locally"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run with Docker"
	@echo "  docker-compose - Run with Docker Compose"
	@echo "  clean       - Clean up temporary files"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with Black"

install:
	cd app && pip install -r requirements.txt

install-dev:
	cd app && pip install -r requirements-dev.txt

test:
	cd app && python -m pytest test_app.py -v

run:
	cd app && python app.py

docker-build:
	docker build -t weather-app:latest .

docker-run:
	docker run -p 5000:5000 -e OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY} weather-app:latest

docker-compose:
	docker-compose up --build

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.db" -delete
	find . -type f -name "plot.png" -delete

lint:
	cd app && flake8 *.py

format:
	cd app && black *.py

# Development server with auto-reload
dev:
	cd app && FLASK_DEBUG=true python app.py
