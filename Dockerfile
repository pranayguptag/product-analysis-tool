# Use official Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (Chrome + driver + fonts)
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set display for headless
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8080

# Run Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
