import whisper
import json
from pathlib import Path

def get_this_stt(audio_path: str):
    model = whisper.load_model("turbo")

    audio_path = Path(audio_path)
    print("----------------------------")
    print(audio_path)

    result = whisper.transcribe(
        model=model,
        audio=str(audio_path)
    )

    output_dir = Path("transcriptions")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{audio_path.stem}.json"

    print("----------------------------")
    print("Dumping JSON...")
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    return result["text"]