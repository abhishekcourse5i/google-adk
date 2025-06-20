# MLRChecker

MLRChecker is a tool that analyzes Instagram posts, video ads, and websites against specific guidelines using Google ADK.

## Getting Started

### Prerequisites

- Python 3.11+
- Google ADK
- Required Python packages (install using `pip install -r requirements.txt`)
- A valid `.env` file with your API keys (see `.envexample` for reference)

### Running the Server

#### Start the API Server:

```bash
python -m agents.analyser_agent
```

This will start a server at `http://localhost:8003` by default. The host and port can be configured using the `ANALYSER_A2A_HOST` and `ANALYSER_A2A_PORT` environment variables.

#### Run with Google ADK UI:

1. First comment and uncomment the changes in `analyser_agent/agent.py`
2. Run the following command:

```bash
adk web
```

#### Environment Setup:

Create a `.env` file in the project root with the following content:

```
GOOGLE_API_KEY="your_google_api_key_here"
ANALYSER_A2A_HOST="0.0.0.0"  # Use 127.0.0.1 for local access only
ANALYSER_A2A_PORT=8003
```

## API Endpoints

The MLRChecker provides the following API endpoints:

- `GET /api/v1/health` - Health check endpoint
- `POST /api/v1/analyze` - Unified endpoint to analyze Instagram posts, video ads, and websites
- `GET /api/v1/analysis/{document_id}` - Retrieve a specific analysis result
- `GET /api/v1/analysis` - Retrieve all analysis results
- `DELETE /api/v1/analysis/{document_id}` - Delete a specific analysis result
- `POST /api/v1/reset-database` - Reset the database

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## Features

- **Unified Analysis Endpoint**: A single endpoint that automatically detects and processes different content types
- **Instagram Post Analysis**: Analyze Instagram posts against guidelines
- **Video Ad Analysis**: Analyze video ads against guidelines
- **Website Analysis**: Analyze websites against guidelines
- **Database Storage**: All analysis results are stored in a SQLite database for easy retrieval
- **Docker Support**: Easy deployment using Docker and Docker Compose

## Docker Deployment

For easy deployment using Docker, please refer to [README.docker.md](README.docker.md).

### Quick Docker Start

```bash
# Create .env file with your Google API key
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env

# Build and start the Docker container
docker-compose up -d
```

The application will be available at `http://localhost:8003`.
