# Docker Deployment for MLRChecker

This document provides instructions for deploying the MLRChecker application using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Google API Key for Gemini (required for the application to function)

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a `.env` file with your Google API key:
   ```bash
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

3. Build and start the Docker container:
   ```bash
   docker-compose up -d
   ```

4. The application will be available at `http://localhost:8003`

5. To check the application logs:
   ```bash
   docker-compose logs -f
   ```

6. To stop the application:
   ```bash
   docker-compose down
   ```

## Configuration

### Environment Variables

The following environment variables can be configured in the `.env` file or directly in the `docker-compose.yml` file:

- `GOOGLE_API_KEY`: Your Google API key for Gemini (required)
- `ANALYSER_A2A_HOST`: Host to bind the server to (default: 0.0.0.0)
- `ANALYSER_A2A_PORT`: Port to run the server on (default: 8003)

### Volumes

The Docker Compose configuration mounts the following volumes:

- `./static:/app/static`: For static files like images and videos uploaded for analysis
- `./temp:/app/temp`: For temporary files created during the analysis process
- `./analysis_results.db:/app/analysis_results.db`: SQLite database file for storing analysis results

These volume mounts ensure that your data persists even if the container is restarted or rebuilt.

## Building the Docker Image Manually

If you want to build the Docker image manually without using Docker Compose:

```bash
docker build -t mlrchecker:latest .
```

Then run the container:

```bash
docker run -d --name mlrchecker \
  -p 8003:8003 \
  -e GOOGLE_API_KEY=your_google_api_key_here \
  -e ANALYSER_A2A_HOST=0.0.0.0 \
  -e ANALYSER_A2A_PORT=8003 \
  -v $(pwd)/static:/app/static \
  -v $(pwd)/temp:/app/temp \
  -v $(pwd)/analysis_results.db:/app/analysis_results.db \
  mlrchecker:latest
```

The Docker image uses Python 3.11 as its base image, which is specified in the Dockerfile.

## Database Management

The application stores analysis results in a SQLite database file (`analysis_results.db`). This file is mounted as a volume to ensure data persistence between container restarts.

### Accessing the Database

You can access the database directly using SQLite tools:

```bash
# Install SQLite if needed
apt-get update && apt-get install -y sqlite3

# Access the database
sqlite3 analysis_results.db

# Inside SQLite shell
.tables
SELECT * FROM analysis_results;
.exit
```

### API Endpoints for Database Management

The application provides several API endpoints for managing the database:

- `GET /api/v1/analysis/{document_id}`: Retrieve a specific analysis result
- `GET /api/v1/analysis`: Retrieve all analysis results
- `DELETE /api/v1/analysis/{document_id}`: Delete a specific analysis result
- `POST /api/v1/reset-database`: Reset the database (drop and recreate the table)

## Health Check

The application includes a health check endpoint at `/api/v1/health`. You can use this to verify that the application is running correctly:

```bash
curl http://localhost:8003/api/v1/health
```

The Docker container is configured with a built-in health check that periodically calls this endpoint to ensure the application is functioning properly.

## Troubleshooting

### Container fails to start

Check the logs for any errors:

```bash
docker-compose logs
```

### API is not accessible

Make sure the container is running and the port is correctly mapped:

```bash
docker ps
```

### Permission issues with volumes

Make sure the directories exist and have the correct permissions:

```bash
mkdir -p static temp
chmod 777 static temp
```
