# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Prevent prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies, including Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    # Add Google's official GPG key
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    # Set up the repository
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    # Install Google Chrome
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]