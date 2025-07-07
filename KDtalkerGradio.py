"""
Video Avatar Generator using Gradio Client API with Dynamic Audio Selection
Requirements:
- gradio_client (pip install gradio-client)
"""

import os
import subprocess
import platform
from gradio_client import Client, handle_file

def get_newest_audio_file(directory):
    """Find most recent audio file in a directory (.wav by default)"""
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Directory does not exist: {directory}")
    
    allowed_extensions = ('.wav', '.mp3')  # Add more formats if needed
    files = []
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in allowed_extensions):
            files.append(file_path)
    
    if not files:
        raise FileNotFoundError(f"No audio files found in {directory}")
    
    return max(files, key=os.path.getmtime)

def open_video_automatically(file_path):
    try:
         if platform.system() == "Windows":
            os.startfile(file_path)

    except Exception as e:
        print(f"Error opening video: {e}")

def main():
    # Configuration - Modify these paths to match your setup
    source_image_path = r'avatar.jpg'
    audio_output_dir = r'c:\pinokio\api\alltalk-tts.git\app\outputs'
    
    try:
        # Initialize client with the correct endpoint URL
        client = Client("http://127.0.0.1:7860/")
        
        # Get newest audio file from specified directory
        latest_audio_path = get_newest_audio_file(audio_output_dir)
        print(f"Using audio file: {latest_audio_path}")
        
        # Call prediction API with handled files
        result = client.predict(
            source_image=handle_file(source_image_path),
            driven_audio=handle_file(latest_audio_path),
            api_name="/gradio_infer"
        )
        
        if 'video' in result and result['video']:
            print(f"Video generated successfully at: {result['video']}")
            open_video_automatically(result['video'])
        else:
            print("Failed to generate video. Check API response:")
            print(result)
            
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
