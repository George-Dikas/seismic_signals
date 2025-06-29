# Use a slim Python image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy dependency 
COPY requirements.txt .

# Install dependencies
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app inside container's working directory /app 
COPY . .

# Set default command
CMD ["python", "main.py"]