# RandomFile

A Flask web application for browsing and serving audio files from a directory structure. RandomFile allows you to browse your audio collection, play files directly in the browser, and convert audio files to MP3 format.

## Features

- Browse directories and audio files through a web interface
- Play MP3 files directly in the browser
- Get random MP3 files from directories
- Convert audio files (OGG, WAV, FLAC, AAC, M4A) to MP3 format
- Secure path validation to prevent directory traversal
- Rate limiting for API endpoints
- Security headers including Content Security Policy

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/randomFile.git
   cd randomFile
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the application:
   - Set environment variables (optional):
     ```
     # On Windows
     set FLASK_CONFIG=development
     set BASE_PATH=path/to/your/audio/files
     set SECRET_KEY=your-secret-key
     
     # On macOS/Linux
     export FLASK_CONFIG=development
     export BASE_PATH=path/to/your/audio/files
     export SECRET_KEY=your-secret-key
     ```

## Usage

### Running the Application

1. Start the development server:
   ```
   python app.py
   ```

2. For production deployment, use Gunicorn:
   ```
   gunicorn "randomfile:create_app()"
   ```

3. Access the application in your web browser at `http://localhost:5000/browse/`

### API Endpoints

#### Browse Files

- **URL**: `/browse/[path]`
- **Method**: GET
- **Description**: Browse files and directories at the specified path
- **Example**: `/browse/music/rock`

#### Get Random Audio File

- **URL**: `/audio/[path]`
- **Method**: GET
- **Description**: Get a random MP3 file from the specified path
- **Example**: `/audio/music/rock`

#### Get Specific Audio File

- **URL**: `/audio/[path]?static=true`
- **Method**: GET
- **Description**: Get a specific MP3 file at the specified path
- **Example**: `/audio/music/rock/song.mp3?static=true`

#### Convert Audio Files

- **URL**: `/convert`
- **Method**: POST
- **Description**: Convert audio files in a directory to MP3 format
- **Request Body**:
  ```json
  {
    "directory": "music/rock",
    "format": "mp3"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Converted 5 files",
    "converted_files": [
      "music/rock/song1.mp3",
      "music/rock/song2.mp3"
    ]
  }
  ```

## Configuration

The application supports different configuration environments:

- **Development**: Debug mode enabled, detailed error messages
- **Testing**: For running tests
- **Production**: Optimized for production use

Configuration options:

- `BASE_PATH`: Path to the directory containing audio files
- `SECRET_KEY`: Secret key for session security
- `HTTPS_ENABLED`: Enable HTTPS security headers (default: False)
- `WTF_CSRF_ENABLED`: Enable CSRF protection (default: True)

## Project Structure

```
randomFile/
├── app.py                  # Application entry point
├── randomfile/             # Main package
│   ├── __init__.py         # Application factory
│   ├── config.py           # Configuration settings
│   ├── security.py         # Security features
│   ├── routes/             # Route handlers
│   │   ├── __init__.py
│   │   ├── main.py         # Main routes
│   │   └── audio.py        # Audio-related routes
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── file_utils.py   # File handling utilities
│       └── audio_utils.py  # Audio conversion utilities
├── templates/              # HTML templates
│   ├── browse.html         # File browser template
│   └── error.html          # Error page template
├── static/                 # Static files
│   └── favicon.ico         # Favicon
├── data/                   # Audio files directory
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Security

The application implements several security features:

- Path validation to prevent directory traversal attacks
- Content Security Policy headers
- CSRF protection for forms
- Rate limiting for API endpoints
- XSS protection headers
- MIME type sniffing protection

## License

This project is licensed under the MIT License - see the LICENSE file for details.