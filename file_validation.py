from pathlib import Path

def validate_file(audio_path: str):
    # File path
    path = Path(audio_path)
    print(path)

    # Check if the file exists
    if path.exists():
        return True
    else:
        return False