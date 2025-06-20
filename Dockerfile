FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add missing dependencies that are used but not in requirements.txt
RUN pip install --no-cache-dir uvicorn fastapi pydantic python-multipart

# Copy project files
COPY . .

# Create a directory for temporary files
RUN mkdir -p /app/temp

# Expose the port the app runs on
EXPOSE 8003

# Command to run the application
CMD ["python", "-m", "agents.analyser_agent"]
