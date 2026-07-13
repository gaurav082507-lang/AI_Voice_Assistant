import os
from pydub import AudioSegment


def audio_preprocess(file_path: str) -> str:
    """Convert an audio file to 16kHz mono WAV for Whisper, and return the new path."""
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)

    file_name, _ = os.path.splitext(file_path)
    final_file = file_name + "_processed.wav"
    audio.export(final_file, format="wav")
    return final_file
