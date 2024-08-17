# Facial Recognition and Occupancy Tracking System



### 1. Introduction
The goal of this project is to develop an occupancy tracking system that accurately logs the entry and exit of individuals within a monitored area. The system employs a combination of facial recognition and clothing-based identification to enhance reliability, particularly in scenarios where facial recognition alone may not suffice due to occlusions or camera angle limitations.

### 2. Problem Statement
Traditional occupancy tracking systems primarily rely on facial recognition to identify and track individuals. However, in environments where people's faces may be obscured or when multiple people share similar facial features, the accuracy of these systems can be compromised. The challenge addressed in this project is to augment facial recognition with a secondary method—clothing-based identification—allowing the system to maintain accurate tracking even when faces are not visible.

### 3. Objectives
Primary Objective: Develop a system that logs the entry and exit of individuals based on facial recognition.
Secondary Objective: Implement a fallback method using clothing-based identification to recognize individuals when faces are not visible.
Tertiary Objective: Integrate both recognition methods into a robust occupancy tracking system that logs real-time data into a database.
### 4. Methodology
The project involves several stages, each focusing on key components of the overall system:

#### 4.1 Facial Recognition
Library Used: face_recognition
Functionality: The system uses the face_recognition library to detect and encode facial features from camera feeds. Each individual's face encoding is stored and compared with previously detected faces to determine if the individual is entering or exiting the area.
#### 4.2 Clothing-Based Identification
Model Used: Pre-trained MobileNetV2 model from TensorFlow/Keras
Feature Extraction: The system uses MobileNetV2 to extract features from the clothing of detected individuals. These features are then used to create a unique "signature" for each person.
Comparison Method: The clothing signatures are compared using cosine similarity. If a match is found within a predefined threshold, the system recognizes the individual based on their clothing.
#### 4.3 Integration
Database Management: SQLite is used to store occupancy data, including signatures, entry times, and exit times.
Processing Pipeline: The system processes video frames, first attempting facial recognition. If no face is detected, it falls back to clothing-based recognition. The occupancy status is updated in the database based on the results.
### 5. Implementation Details
- **Programming Language**: Python
- **Libraries**: face_recognition, TensorFlow, Keras, OpenCV, SQLite, scikit-learn, imagehash.

## Table of Contents
- [Features](#Features)
- [Project Structure](#project-structure)
- [Installation](#Installation)
- [Usage](#Usage)
- [Configuration](#Configuration)
- [Docker Containerization](#Docker-containerization)
- [Development in a Dev Container](#Development-in-a-dev-container)
- [Contributing](#Contributing)
- [License](#License)

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
