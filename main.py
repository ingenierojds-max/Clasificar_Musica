from fastapi import FastAPI, File, UploadFile
from mutagen.mp3 import MP3
import os

app = FastAPI()

@app.post("/metadata")
async def get_metadata(file: UploadFile = File(...)):
    temp_filename = "temp.mp3"
    contents = await file.read()
    with open(temp_filename, "wb") as f:
        f.write(contents)

    audio = MP3(temp_filename)
    os.remove(temp_filename)

    return {
        "filename": file.filename,
        "duration_seconds": round(audio.info.length, 2),
        "bitrate": audio.info.bitrate
    }
