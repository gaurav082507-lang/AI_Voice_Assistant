import subprocess
import uuid


def text_speech(response: str, model_path: str = "en_US-lessac-medium.onnx") -> str:
    """Convert text to speech with Piper and return the path to the generated WAV file."""
    output_file = f"response_{uuid.uuid4().hex}.wav"

    subprocess.run(
        ["piper", "--model", model_path, "--output_file", output_file],
        input=response.encode(),
        check=True,
    )
    return output_file
