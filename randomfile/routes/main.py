from flask import Blueprint, render_template, current_app, abort, request, redirect, url_for, flash
from pathlib import Path
import os

from randomfile.utils.file_utils import (
    get_files_and_dirs, get_path_parts, PathValidationError,
    add_file, delete_file, move_file, create_directory,
    get_directory_tree
)

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route("/browse/<path:subpath>")
@main_bp.route("/browse/")
def browse(subpath=None):
    """
    Returns a list of all .mp3 files in a directory including subdirectories.

    Args:
        subpath (str, optional): Subdirectory to browse. Defaults to None.

    Returns:
        str: Rendered HTML template
    """
    base_path = current_app.config['BASE_PATH']
    path = Path(f"{base_path}/{subpath}" if subpath else base_path).resolve()

    try:
        # Get files and directories for the current path (for backward compatibility)
        files = get_files_and_dirs(path)
        path_parts = get_path_parts(path)

        # Get the complete directory tree starting from the base path
        directory_tree = get_directory_tree(Path(base_path))

        return render_template(
            "browse.html",
            files=files,
            path_parts=path_parts,
            directory_tree=directory_tree,
            current_path=str(os.path.relpath(path, base_path)) if path != base_path else ""
        )
    except PathValidationError as e:
        # Return a 403 Forbidden error with a custom error message
        return abort(403, description=str(e))
    except Exception as e:
        # Return a 500 Internal Server Error for unexpected errors
        current_app.logger.error(f"Error in browse route: {str(e)}")
        return abort(500, description="An unexpected error occurred")


@main_bp.route("/upload", methods=["POST"])
def upload_file():
    # TODO: Look into this
    """
    Upload a file to the specified directory.

    Returns:
        Redirect to the browse page
    """
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.referrer or url_for('main.browse'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.referrer or url_for('main.browse'))

    subpath = request.form.get('subpath', '')
    base_path = current_app.config['BASE_PATH']
    directory_path = Path(f"{base_path}/{subpath}").resolve() if subpath else Path(base_path)

    success, error = add_file(directory_path, file)

    if success:
        flash('File uploaded successfully', 'success')
    else:
        flash(f'Error uploading file: {error}', 'error')

    return redirect(url_for('main.browse', subpath=subpath))


@main_bp.route("/delete", methods=["POST"])
def delete_file_route():
    # TODO: Look into this
    """
    Delete a file.

    Returns:
        Redirect to the browse page
    """
    file_path = request.form.get('file_path', '')
    if not file_path:
        flash('No file specified', 'error')
        return redirect(request.referrer or url_for('main.browse'))

    base_path = current_app.config['BASE_PATH']
    full_path = Path(f"{base_path}/{file_path}").resolve()

    success, error = delete_file(full_path)

    if success:
        flash('File deleted successfully', 'success')
    else:
        flash(f'Error deleting file: {error}', 'error')

    # Get the directory part of the file path
    directory = os.path.dirname(file_path)
    return redirect(url_for('main.browse', subpath=directory))


@main_bp.route("/move", methods=["POST"])
def move_file_route():
    # TODO: Look into this
    """
    Move a file to a different directory.

    Returns:
        Redirect to the browse page
    """
    file_path = request.form.get('file_path', '')
    destination = request.form.get('destination', '')

    if not file_path:
        flash('No file specified', 'error')
        return redirect(request.referrer or url_for('main.browse'))

    if not destination:
        flash('No destination specified', 'error')
        return redirect(request.referrer or url_for('main.browse'))

    base_path = current_app.config['BASE_PATH']
    full_file_path = Path(f"{base_path}/{file_path}").resolve()
    full_destination = Path(f"{base_path}/{destination}").resolve()

    success, error = move_file(full_file_path, full_destination)

    if success:
        flash('File moved successfully', 'success')
    else:
        flash(f'Error moving file: {error}', 'error')

    # Get the directory part of the file path
    directory = os.path.dirname(file_path)
    return redirect(url_for('main.browse', subpath=directory))


@main_bp.route("/create_directory", methods=["POST"])
def create_directory_route():
    # TODO: Look into this
    """
    Create a new directory.

    Returns:
        Redirect to the browse page
    """
    parent_path = request.form.get('parent_path', '')
    dir_name = request.form.get('dir_name', '')

    if not dir_name:
        flash('No directory name specified', 'error')
        return redirect(request.referrer or url_for('main.browse'))

    base_path = current_app.config['BASE_PATH']
    full_parent_path = Path(f"{base_path}/{parent_path}").resolve() if parent_path else Path(base_path)

    success, error = create_directory(full_parent_path, dir_name)

    if success:
        flash('Directory created successfully', 'success')
    else:
        flash(f'Error creating directory: {error}', 'error')

    return redirect(url_for('main.browse', subpath=parent_path))


@main_bp.errorhandler(403)
def forbidden_error(e):
    """Custom error handler for 403 errors."""
    return render_template('error.html',
                           error_code=403,
                           error_message="Forbidden",
                           error_description=str(e)), 403


@main_bp.errorhandler(404)
def not_found_error(e):
    """Custom error handler for 404 errors."""
    return render_template('error.html',
                           error_code=404,
                           error_message="Not Found",
                           error_description="The requested resource could not be found"), 404


@main_bp.errorhandler(500)
def internal_error(e):
    """Custom error handler for 500 errors."""
    return render_template('error.html',
                           error_code=500,
                           error_message="Internal Server Error",
                           error_description="An unexpected error occurred"), 500
