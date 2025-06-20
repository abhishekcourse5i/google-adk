# MLRChecker API Documentation

This document provides information on how to use the MLRChecker API endpoint for analyzing Instagram posts, videos, and websites, and managing analysis results in the database.

## Base URL

```
http://localhost:8003/api/v1
```

The port (8003) can be configured using the `ANALYSER_A2A_PORT` environment variable.

## Authentication

Currently, the API does not require authentication.

## Endpoints

### Health Check

Check if the API is running.

```
GET /health
```

#### Response

```json
{
  "status": "healthy"
}
```

### Analyze Content

Unified endpoint to analyze content (Instagram post, video, or website).

```
POST /analyze
```

#### Request

This endpoint accepts form data with file upload support. You can send the following parameters:

Fields:
- `document_name` (optional): Name of the document to analyze
- `session_id` (optional): Session identifier for stateful interactions
- `context` (optional): Additional context for the request as a JSON string
- `url` (optional): URL of the website to analyze - required if no file is uploaded
- `file_type` (optional): Type of the file (image or video)
- `guidelines` (optional): Guidelines for the analysis
- `file` (optional): File to upload (image or video) - required if URL is not provided

**Note:** You must provide either a `file` upload or a `url`, but not both.

**Content Type Detection:**
- If you upload a file, the system will automatically detect if it's an image (Instagram post) or video based on the file extension.
- Image extensions supported: .jpg, .jpeg, .png, .gif, .bmp, .tiff
- Video extensions supported: .mp4, .mov, .avi, .wmv, .flv, .mkv

#### Example Requests

**For Instagram Post Analysis with File Upload:**

Using cURL:

```bash
curl -X POST "http://localhost:8003/api/v1/analyze" \
  -F "file=@/path/to/local/instagram_post.jpg" \
  -F "guidelines=These are the guidelines for Instagram posts..." \
  -F "context={}"
```

Using Python with requests:

```python
import requests

url = "http://localhost:8003/api/v1/analyze"
files = {
    'file': open('/path/to/local/instagram_post.jpg', 'rb')
}
data = {
    'guidelines': 'These are the guidelines for Instagram posts...',
    'context': '{}'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**For Video Analysis with File Upload:**

Using cURL:

```bash
curl -X POST "http://localhost:8003/api/v1/analyze" \
  -F "file=@/path/to/local/video.mp4" \
  -F "guidelines=These are the guidelines for video ads..." \
  -F "context={}"
```

Using Python with requests:

```python
import requests

url = "http://localhost:8003/api/v1/analyze"
files = {
    'file': open('/path/to/local/video.mp4', 'rb')
}
data = {
    'guidelines': 'These are the guidelines for video ads...',
    'context': '{}'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**For Website Analysis:**

Using cURL:

```bash
curl -X POST "http://localhost:8003/api/v1/analyze" \
  -F "url=https://example.com" \
  -F "guidelines=These are the guidelines for websites..." \
  -F "context={}"
```

Using Python with requests:

```python
import requests

url = "http://localhost:8003/api/v1/analyze"
data = {
    'url': 'https://example.com',
    'guidelines': 'These are the guidelines for websites...',
    'context': '{}'
}

response = requests.post(url, data=data)
print(response.json())
```

#### Response

```json
{
  "message": "Analysis result text here...",
  "status": "success",
  "data": {
    "raw_events": [...]
  },
  "session_id": "optional-session-id"
}
```

### Get Analysis Result

Retrieve a specific analysis result from the database by document ID.

```
GET /analysis/{document_id}
```

#### Response

```json
{
  "document_id": "unique-document-id",
  "document_name": "example.jpg",
  "upload_time": "2025-06-20 14:00:00",
  "status": "Approved",
  "score": 0.85,
  "file_type": "image/jpeg",
  "file_url": "https://example.com/image.jpg",
  "suggestions": ["Suggestion 1", "Suggestion 2"],
  "conflicts": ["Conflict 1"],
  "guidelines": "Guidelines used for analysis",
  "summary": "Summary of the document content"
}
```

### Get All Analysis Results

Retrieve all analysis results from the database.

```
GET /analysis
```

#### Response

```json
[
  {
    "document_id": "unique-document-id-1",
    "document_name": "example1.jpg",
    "upload_time": "2025-06-20 14:00:00",
    "status": "Approved",
    "score": 0.85,
    "file_type": "image/jpeg",
    "file_url": "https://example.com/image1.jpg",
    "suggestions": ["Suggestion 1", "Suggestion 2"],
    "conflicts": ["Conflict 1"],
    "guidelines": "Guidelines used for analysis",
    "summary": "Summary of the document content"
  },
  {
    "document_id": "unique-document-id-2",
    "document_name": "example2.jpg",
    "upload_time": "2025-06-20 13:00:00",
    "status": "Rejected",
    "score": 0.45,
    "file_type": "image/jpeg",
    "file_url": "https://example.com/image2.jpg",
    "suggestions": ["Suggestion 3", "Suggestion 4"],
    "conflicts": ["Conflict 2", "Conflict 3"],
    "guidelines": "Guidelines used for analysis",
    "summary": "Summary of the document content"
  }
]
```

### Delete Analysis Result

Delete a specific analysis result from the database.

```
DELETE /analysis/{document_id}
```

#### Response

```json
{
  "status": "success",
  "message": "Analysis result deleted for document ID: unique-document-id"
}
```

### Reset Database

Reset the database by dropping and recreating the analysis_results table.

```
POST /reset-database
```

#### Response

```json
{
  "status": "success",
  "message": "Database reset successfully"
}
```

## Error Handling

In case of an error, the API will return a response with a status of "error" and an error message:

```json
{
  "message": "Error message here...",
  "status": "error",
  "data": {
    "error_type": "ExceptionType"
  },
  "session_id": "optional-session-id"
}
```

## Running the API Server

To start the API server, run the following command from the project root:

```bash
python -m agents.analyser_agent
```

The server will start on the host and port specified in the environment variables `ANALYSER_A2A_HOST` and `ANALYSER_A2A_PORT`, defaulting to `127.0.0.1:8003` if not specified.

## Database Storage

When you submit content for analysis using the `/analyze` endpoint, the results are automatically stored in a SQLite database with the following schema:

- `document_id`: Unique identifier for the document (generated automatically if not provided)
- `document_name`: Name of the document
- `upload_time`: Timestamp when the document was uploaded
- `status`: Status of the analysis (Reject/Approved) - automatically set to "Approved" if score > 90, otherwise "Reject"
- `score`: Score of the analysis
- `file_type`: Type of the file
- `file_url`: URL to the file or path to the uploaded file
- `suggestions`: List of suggestions (stored as JSON)
- `conflicts`: List of conflicts (stored as JSON)
- `guidelines`: Guidelines used for analysis (stored as JSON)
- `summary`: Summary of the document content

The database file is located at the project root as `analysis_results.db`.

## Docker Usage

When using Docker, uploaded files are saved to the `/app/static` directory in the container, which is mapped to the `./static` directory on the host as defined in the `docker-compose.yml` file. This ensures that uploaded files are persisted even if the container is restarted.

The SQLite database file is also persisted through a volume mount, ensuring that analysis results are preserved between container restarts.
