# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for Python and C extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*



# Copy service account key
COPY statux-pubsub-key.json /app/statux-pubsub-key.json

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/statux-pubsub-key.json"

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt

RUN python3 -m spacy download en_core_web_sm
RUN python3 setupEmailWatch.py

# Expose the port the app runs on
EXPOSE 8080

# Command to run your application
CMD ["python", "app.py"]