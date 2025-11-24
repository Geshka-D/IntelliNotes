# Installation Guide

This guide provides detailed instructions for setting up and running IntelliNotes.

## System Requirements

- **Python**: Version 3.8 or higher (Python 3.12 recommended)
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB available
- **Disk Space**: At least 500MB for dependencies

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Geshka-D/IntelliNotes.git
cd IntelliNotes
```

### 2. Set Up Python Virtual Environment

Creating a virtual environment is **highly recommended** to isolate project dependencies.

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

You should see `(venv)` prefix in your terminal prompt when the virtual environment is activated.

### 3. Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - Modern web framework
- Uvicorn - ASGI server
- Pydantic - Data validation
- Jinja2 - Template engine
- python-docx - Word document handling
- reportlab - PDF generation
- pytest - Testing framework
- And other dependencies

### 4. Verify Installation

Check that the installation was successful:

```bash
python -c "import fastapi, uvicorn; print('Installation successful!')"
```

## Running the Application

### Start the Server

From the project root directory, run:

```bash
python main.py
```

The application will start on http://127.0.0.1:8000

### Expected Output

When the server starts successfully, you should see:

```
INFO:     Will watch for changes in these directories: ['/path/to/IntelliNotes']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using StatReload
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Access the Application

Open your web browser and navigate to:

- **Main API**: http://127.0.0.1:8000/
- **Interactive API Docs (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc

### Stopping the Server

To stop the server, press `CTRL+C` in the terminal.

## Troubleshooting

### Virtual Environment Not Activating

**Windows PowerShell Error**: If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/macOS Permission Error**: Make sure the activate script is executable:
```bash
chmod +x venv/bin/activate
```

### Port Already in Use

If port 8000 is already in use, you can specify a different port by editing `main.py`:

```python
uvicorn.run("backend.main:app", host="127.0.0.1", port=8001, reload=True)
```

### Import Errors

If you encounter import errors:
1. Ensure your virtual environment is activated
2. Verify all dependencies are installed: `pip list`
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Database Issues

The application automatically initializes the database on startup. If you encounter database-related errors:
1. Check that you have write permissions in the project directory
2. Delete any existing database files and restart the application

## Development Mode

The application runs in development mode by default, with:
- **Auto-reload**: File changes automatically restart the server
- **Debug mode**: Detailed error messages
- **API documentation**: Interactive docs available

## Running Tests

To verify everything is working correctly:

```bash
pytest
```

For verbose output:
```bash
pytest -v
```

To run specific tests:
```bash
pytest tests/test_api.py
```

## Next Steps

After successful installation:
1. Explore the API documentation at http://127.0.0.1:8000/docs
2. Review the [Architecture Guide](architecture.md)
3. Check the [API Endpoints documentation](api_endpoints.md)
4. Start developing or testing features

## Deactivating the Virtual Environment

When you're done working on the project:

```bash
deactivate
```
