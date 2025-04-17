import os
from pathlib import Path
from pydub import AudioSegment
from typing import List, Callable, Optional
from flask import current_app

def convert_ogg_to_mp3(directory: Path, progress_callback: Optional[Callable[[int, int], None]] = None) -> List[str]:
    """
    Converts all .ogg files in a directory to .mp3 format.
    
    Args:
        directory (Path): The directory to scan for .ogg files
        progress_callback (Optional[Callable[[int, int], None]]): A callback function to report progress
            The callback receives (current_file_index, total_files)
            
    Returns:
        List[str]: List of converted files
    """
    # Find all .ogg files
    ogg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.ogg'):
                ogg_files.append(os.path.join(root, file))
    
    converted_files = []
    total_files = len(ogg_files)
    
    # Convert each file
    for i, file_path in enumerate(ogg_files):
        try:
            # Report progress if callback provided
            if progress_callback:
                progress_callback(i + 1, total_files)
                
            # Convert the file
            ogg = AudioSegment.from_ogg(file_path)
            mp3_path = file_path.replace('.ogg', '.mp3')
            ogg.export(mp3_path, format="mp3")
            
            # Remove the original file
            os.remove(file_path)
            
            converted_files.append(mp3_path)
        except Exception as e:
            # Log the error but continue with other files
            print(f"Error converting {file_path}: {str(e)}")
    
    return converted_files

def supports_format(file_extension: str) -> bool:
    """
    Check if a file format is supported for conversion.
    
    Args:
        file_extension (str): The file extension to check (e.g., '.ogg', '.wav')
        
    Returns:
        bool: True if the format is supported, False otherwise
    """
    # List of supported formats for conversion to MP3
    supported_formats = ['.ogg', '.wav', '.flac', '.aac', '.m4a']
    return file_extension.lower() in supported_formats

def convert_audio_file(file_path: str, output_format: str = 'mp3') -> str:
    """
    Convert a single audio file to the specified format.
    
    Args:
        file_path (str): Path to the audio file
        output_format (str): Output format (default: 'mp3')
        
    Returns:
        str: Path to the converted file
    """
    file_path = Path(file_path)
    file_extension = file_path.suffix.lower()
    
    if not supports_format(file_extension):
        raise ValueError(f"Unsupported format: {file_extension}")
    
    # Determine the appropriate AudioSegment method based on file extension
    if file_extension == '.ogg':
        audio = AudioSegment.from_ogg(file_path)
    elif file_extension == '.wav':
        audio = AudioSegment.from_wav(file_path)
    elif file_extension == '.flac':
        audio = AudioSegment.from_file(file_path, format="flac")
    elif file_extension in ['.aac', '.m4a']:
        audio = AudioSegment.from_file(file_path, format="aac")
    else:
        # This should not happen due to the supports_format check
        raise ValueError(f"Unsupported format: {file_extension}")
    
    # Create output path
    output_path = str(file_path.with_suffix(f'.{output_format}'))
    
    # Export to the desired format
    audio.export(output_path, format=output_format)
    
    return output_path