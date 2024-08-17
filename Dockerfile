## Use an official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to avoid user prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-opencv \
    libopencv-dev \
    build-essential \
    cmake \
    git \
    curl \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    libboost-all-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY app/requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY app/ .

# Run database setup (if necessary)
RUN python3 database_setup.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python3", "main.py"]
