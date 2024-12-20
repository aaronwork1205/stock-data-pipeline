# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid some prompts during the installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required dependencies
RUN apt-get update && \
    apt-get install -y \
    python3.8 \
    python3-pip \
    python3-dev \
    libmysqlclient-dev \
    && apt-get clean

# Set up a working directory
WORKDIR /app

# Install Python packages
RUN pip3 install --upgrade pip
RUN pip3 install yfinance mysql-connector-python pandas tqdm configparser

# Copy your application code into the container
COPY . /app
# Set the default command to run the Python script (if you have a specific entry point script)
CMD ["python3", "data-python/data-get.py"]
CMD ["python3", "db-python/connect.py"]
