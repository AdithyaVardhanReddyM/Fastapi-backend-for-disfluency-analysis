from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List
import subprocess

app = FastAPI()

# Example request body model
class AudioInput(BaseModel):
    audio_file: bytes
    modality: str

# Example response model
class TranscriptionResult(BaseModel):
    transcription_csv: str
    prediction_csv: str

# Example endpoint to handle audio file upload and processing
@app.post("/process_audio/")
async def process_audio(audio_input: AudioInput):
    # Save the audio file
    with open("input.wav", "wb") as audio_file:
        audio_file.write(audio_input.audio_file)

    # Prepare command to run demo.py
    command = [
        "python3",
        "demo.py",
        "--audio_file", "input.wav",
        "--output_file", "pred.csv",
        "--output_trans", "trans.csv",
        "--modality", audio_input.modality
    ]

    # Run the command using subprocess
    subprocess.run(command)

    # Read the generated CSV files
    with open("trans.csv", "r") as trans_file, open("pred.csv", "r") as pred_file:
        transcription_csv = trans_file.read()
        prediction_csv = pred_file.read()

    # Return the CSV contents as response
    return TranscriptionResult(transcription_csv=transcription_csv, prediction_csv=prediction_csv)
