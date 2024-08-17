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
```

## Installation
Clone the Repository:
```bash
git clone https://github.com/adithya7shankar/your-repo-name.git
cd your-repo-name
```
Install Dependencies:
```bash
pip install -r requirements.txt
```
Set Up the Database:
Run the database setup script to create the necessary tables:

```bash
python database_setup.py
```
## Usage
To start the system, run the main script:

```bash
python main.py
```
The system will begin monitoring the space, detecting faces, and tracking occupancy.

## Configuration
The config.yaml file contains configuration options for the project. You can adjust settings such as the detection thresholds, database paths, and more.

## Docker Containerization
The project includes a Dockerfile for containerization. To build and run the Docker container:

Build the Docker Image:

```bash
docker build -t occupancy-tracking .
```
Run the Docker Container:

```bash
docker run -d -p 8080:8080 occupancy-tracking
```
## Development in a Dev Container
This project also includes a devcontainer.json file, allowing you to develop within a Docker container using Visual Studio Code. This setup includes Python and Jupyter extensions for a streamlined development experience.

To get started with the dev container:

Open the project in Visual Studio Code.
You will be prompted to reopen the project in a dev container. Click "Reopen in Container."
The dev container will be built and launched, providing a consistent development environment.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
