import os
import shutil
from pathlib import Path
from flask import current_app
import random
from typing import Dict, List, Tuple, Optional, Union, Any

class PathValidationError(Exception):
    """Exception raised for path validation errors."""
    pass

def validate_path(path: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate if a path is safe to access.

    Args:
        path (Path): The path to validate

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing (is_valid, error_message)
    """
    base_path = current_app.config['BASE_PATH']

    # Check if the path is a subdirectory of base_path
    try:
        if not path.is_relative_to(base_path):
            return False, "Path is outside of allowed directory"
    except AttributeError:
        # For Python < 3.9 that doesn't have is_relative_to
        try:
            path.relative_to(base_path)
        except ValueError:
            return False, "Path is outside of allowed directory"

    # Check if the path exists
    if not path.exists():
        return False, "Path does not exist"

    # Check if the path is a directory
    if not path.is_dir():
        return False, "Path is not a directory"

    return True, None

def get_files_and_dirs(path: Path) -> Dict[str, List[str]]:
    """
    Get all files and directories in a path.

    Args:
        path (Path): The path to scan

    Returns:
        Dict[str, List[str]]: A dictionary with 'dirs' and 'files' keys
    """
    base_path = current_app.config['BASE_PATH']
    is_valid, error = validate_path(path)

    if not is_valid:
        raise PathValidationError(error)

    result = {"dirs": [], "files": []}

    for item in path.iterdir():
        if item.is_dir():
            result["dirs"].append(str(os.path.relpath(item, base_path)))
        elif item.is_file() and item.suffix.lower() == '.mp3':
            result["files"].append(str(os.path.relpath(item, base_path)))

    # Sort the lists for a better user experience
    result["dirs"].sort()
    result["files"].sort()

    return result

def get_random_file(path: Path) -> Optional[Path]:
    """
    Get a random MP3 file from a directory including subdirectories.

    Args:
        path (Path): The path to search in

    Returns:
        Optional[Path]: Path to a random MP3 file or None if no files are found
    """
    is_valid, error = validate_path(path)

    if not is_valid:
        raise PathValidationError(error)

    files = []

    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                files.append(Path(os.path.join(root, filename)))

    if not files:
        return None

    return random.choice(files)

def get_path_parts(path: Path) -> List[str]:
    """
    Get the path parts for breadcrumb navigation.

    Args:
        path (Path): The path to split

    Returns:
        List[str]: List of path parts
    """
    base_path = current_app.config['BASE_PATH']
    rel_path = os.path.relpath(path, base_path)

    if rel_path == '.':
        return []

    return rel_path.split(os.sep)

def add_file(directory_path: Path, file) -> Tuple[bool, Optional[str]]:
    """
    Save an uploaded file to the specified directory.

    Args:
        directory_path (Path): The directory to save the file to
        file: The file object from the request

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing (success, error_message)
    """
    is_valid, error = validate_path(directory_path)

    if not is_valid:
        return False, error

    try:
        # Save the file
        file_path = directory_path / file.filename
        file.save(file_path)
        return True, None
    except Exception as e:
        return False, str(e)

def delete_file(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Delete a file.

    Args:
        file_path (Path): The path to the file to delete

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing (success, error_message)
    """
    base_path = current_app.config['BASE_PATH']

    # Check if the file is within the base path
    try:
        if not file_path.is_relative_to(base_path):
            return False, "Path is outside of allowed directory"
    except AttributeError:
        # For Python < 3.9 that doesn't have is_relative_to
        try:
            file_path.relative_to(base_path)
        except ValueError:
            return False, "Path is outside of allowed directory"

    # Check if the file exists
    if not file_path.exists():
        return False, "File does not exist"

    # Check if it's a file (not a directory)
    if not file_path.is_file():
        return False, "Path is not a file"

    try:
        # Delete the file
        file_path.unlink()
        return True, None
    except Exception as e:
        return False, str(e)

def move_file(file_path: Path, destination_dir: Path) -> Tuple[bool, Optional[str]]:
    """
    Move a file to a different directory.

    Args:
        file_path (Path): The path to the file to move
        destination_dir (Path): The destination directory

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing (success, error_message)
    """
    base_path = current_app.config['BASE_PATH']

    # Check if the file is within the base path
    try:
        if not file_path.is_relative_to(base_path):
            return False, "Source path is outside of allowed directory"
    except AttributeError:
        # For Python < 3.9 that doesn't have is_relative_to
        try:
            file_path.relative_to(base_path)
        except ValueError:
            return False, "Source path is outside of allowed directory"

    # Check if the destination is within the base path
    try:
        if not destination_dir.is_relative_to(base_path):
            return False, "Destination path is outside of allowed directory"
    except AttributeError:
        # For Python < 3.9 that doesn't have is_relative_to
        try:
            destination_dir.relative_to(base_path)
        except ValueError:
            return False, "Destination path is outside of allowed directory"

    # Check if the file exists
    if not file_path.exists():
        return False, "File does not exist"

    # Check if it's a file (not a directory)
    if not file_path.is_file():
        return False, "Source path is not a file"

    # Check if the destination directory exists
    if not destination_dir.exists():
        return False, "Destination directory does not exist"

    # Check if the destination is a directory
    if not destination_dir.is_dir():
        return False, "Destination path is not a directory"

    try:
        # Move the file
        destination_file = destination_dir / file_path.name
        shutil.move(str(file_path), str(destination_file))
        return True, None
    except Exception as e:
        return False, str(e)

def create_directory(parent_dir: Path, dir_name: str) -> Tuple[bool, Optional[str]]:
    """
    Create a new directory.

    Args:
        parent_dir (Path): The parent directory
        dir_name (str): The name of the new directory

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing (success, error_message)
    """
    is_valid, error = validate_path(parent_dir)

    if not is_valid:
        return False, error

    try:
        # Create the directory
        new_dir = parent_dir / dir_name
        new_dir.mkdir(exist_ok=False)
        return True, None
    except FileExistsError:
        return False, "Directory already exists"
    except Exception as e:
        return False, str(e)

def get_directory_tree(path: Path) -> Dict[str, Any]:
    """
    Get the complete directory structure recursively.

    Args:
        path (Path): The root path to scan

    Returns:
        Dict[str, Any]: A nested dictionary representing the directory structure
    """
    base_path = current_app.config['BASE_PATH']
    is_valid, error = validate_path(path)

    if not is_valid:
        raise PathValidationError(error)

    result = {"name": os.path.basename(path) or "Root", "path": str(os.path.relpath(path, base_path)), "type": "directory", "children": []}

    # Get all items in the directory
    for item in path.iterdir():
        if item.is_dir():
            # Recursively get the structure for subdirectories
            child_dir = get_directory_tree(item)
            result["children"].append(child_dir)
        elif item.is_file() and item.suffix.lower() == '.mp3':
            # Add files to the children list
            rel_path = str(os.path.relpath(item, base_path))
            result["children"].append({
                "name": item.name,
                "path": rel_path,
                "type": "file"
            })

    # Sort children by type (directories first) and then by name
    result["children"].sort(key=lambda x: (0 if x["type"] == "directory" else 1, x["name"].lower()))

    return result
