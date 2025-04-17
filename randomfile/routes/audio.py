from flask import Blueprint, send_file, current_app, abort, request, jsonify
from pathlib import Path
import os

from randomfile.utils.file_utils import get_random_file, validate_path, PathValidationError
from randomfile.utils.audio_utils import convert_ogg_to_mp3, supports_format, convert_audio_file
from randomfile import limiter

# Create blueprint
audio_bp = Blueprint('audio', __name__)

@audio_bp.route("/audio/<path:subpath>")
@audio_bp.route("/audio")
@limiter.limit("100 per day")
def random_file(subpath=None):
    """
    Returns a random .mp3 file from a directory including subdirectories.

    Args:
        subpath (str, optional): Subdirectory to search in. Defaults to None.

    Returns:
        Response: Audio file response
    """
    base_path = current_app.config['BASE_PATH']
    path = Path(f"{base_path}/{subpath}" if subpath else base_path).resolve()

    # Check if a static parameter is provided (for direct file access)
    static = request.args.get('static', 'false').lower() == 'true'

    if static and subpath:
        # Serve a specific file
        file_path = Path(f"{base_path}/{subpath}").resolve()

        # Validate the file path
        is_valid, error = validate_path(file_path.parent)
        if not is_valid:
            return abort(403, description=error)

        if not file_path.exists() or not file_path.is_file():
            return abort(404, description="File not found")

        # Check if the file is an MP3
        if file_path.suffix.lower() != '.mp3':
            return abort(400, description="Only MP3 files are supported")

        return send_file(file_path, mimetype="audio/mp3")

    # Get a random file
    try:
        random_mp3 = get_random_file(path)

        if not random_mp3:
            return abort(404, description="No MP3 files found in the specified directory")

        return send_file(random_mp3, mimetype="audio/mp3", as_attachment=True)
    except PathValidationError as e:
        return abort(403, description=str(e))
    except Exception as e:
        current_app.logger.error(f"Error in random_file route: {str(e)}")
        return abort(500, description="An unexpected error occurred")

@audio_bp.route("/convert", methods=['POST'])
@limiter.limit("10 per hour")
def convert_files():
    """
    API endpoint to convert audio files to MP3.

    Expected JSON payload:
    {
        "directory": "path/to/directory",  # Optional, defaults to base path
        "format": "mp3"                    # Optional, defaults to mp3
    }

    Returns:
        JSON response with conversion results
    """
    data = request.get_json() or {}
    base_path = current_app.config['BASE_PATH']

    # Get directory from request or use the base path
    directory = data.get('directory', '')
    directory_path = Path(f"{base_path}/{directory}").resolve() if directory else base_path

    # Validate the directory
    is_valid, error = validate_path(directory_path)
    if not is_valid:
        return jsonify({"error": error}), 403

    try:
        # Convert files
        converted_files = convert_ogg_to_mp3(directory_path)

        return jsonify({
            "success": True,
            "message": f"Converted {len(converted_files)} files",
            "converted_files": converted_files
        })
    except Exception as e:
        current_app.logger.error(f"Error in convert_files route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@audio_bp.errorhandler(400)
def bad_request_error(e):
    """Custom error handler for 400 errors."""
    return jsonify({"error": str(e)}), 400

@audio_bp.errorhandler(403)
def forbidden_error(e):
    """Custom error handler for 403 errors."""
    return jsonify({"error": str(e)}), 403

@audio_bp.errorhandler(404)
def not_found_error(e):
    """Custom error handler for 404 errors."""
    return jsonify({"error": "Not found"}), 404

@audio_bp.errorhandler(500)
def internal_error(e):
    """Custom error handler for 500 errors."""
    return jsonify({"error": "Internal server error"}), 500
