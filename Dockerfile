# Use Selenium base image with Chrome + driver pre-installed
FROM selenium/standalone-chrome:118.0

# Install Python
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8080

# Start with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
