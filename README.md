# IntelliNotes (LectureNotesAI)

An intelligent note-taking application that leverages AI for transcription and summarization of lecture content.

## Project Structure

This repository contains a full project skeleton for IntelliNotes:
- **backend**: FastAPI web application
- **nlp_engine**: Transcription & summarization capabilities
- **frontend**: Static templates and UI
- **database**: Database models and connections
- **scripts**: Utility scripts for setup
- **tests**: Test suites
- **docs**: Documentation

## Prerequisites

- Python 3.8 or higher (tested with Python 3.12)
- pip (Python package manager)

## Installation & Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/Geshka-D/IntelliNotes.git
   cd IntelliNotes
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - On Windows (Command Prompt):
     ```cmd
     venv\Scripts\activate.bat
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Run the application using:
```bash
python main.py
```

The FastAPI backend server will start on `http://127.0.0.1:8000`

You should see output similar to:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using StatReload
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Accessing the Application

- **API Root**: http://127.0.0.1:8000/
- **API Documentation (Swagger UI)**: http://127.0.0.1:8000/docs
- **Alternative API Documentation (ReDoc)**: http://127.0.0.1:8000/redoc

## API Endpoints

- `POST /lectures/upload` - Upload lecture content
- `GET /notes/` - List all notes
- `GET /notes/{id}` - Get a specific note
- `POST /users/` - User management

For detailed API documentation, visit the Swagger UI at http://127.0.0.1:8000/docs after starting the server.

## Running Tests

To run the test suite:
```bash
pytest
```

## Development

The application runs in development mode with auto-reload enabled. Any changes to the Python files will automatically restart the server.

To stop the server, press `CTRL+C` in the terminal.

## Additional Documentation

For more detailed information, see:
- [Installation Guide](docs/installation.md)
- [Architecture](docs/architecture.md)
- [API Endpoints](docs/api_endpoints.md)
