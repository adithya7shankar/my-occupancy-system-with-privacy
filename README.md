# Facial Recognition and Occupancy Tracking System

This project is a facial recognition and occupancy tracking system designed to monitor and track the occupancy of a building or space by detecting faces and using clothing as a signature when faces are not detected.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Docker Containerization](#docker-containerization)
- [Development in a Dev Container](#development-in-a-dev-container)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Facial Recognition**: Uses machine learning models to detect faces.
- **Occupancy Tracking**: Tracks the number of people in a space by detecting faces and clothing.
- **Database Management**: Stores occupancy data in a SQLite database.
- **Docker Containerization**: The project is containerized for easy setup and deployment.

## Project Structure
```plaintext
.
├── database_setup.py       # Script to set up the SQLite database
├── main.py                 # Main script for running the system
├── requirements.txt        # Python dependencies
├── testing-functions.py    # Additional functions for testing
├── building_occupancy.db   # SQLite database file
├── config.yaml             # Configuration file for the project
├── Dockerfile              # Dockerfile for containerizing the application
├── devcontainer.json       # VSCode dev container configuration
