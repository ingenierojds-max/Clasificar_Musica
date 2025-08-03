from fastapi import FastAPI, File, UploadFile
from mutagen import File as MutagenFile
import uvicorn

app = FastAPI()

@app.post("/metadata")
async def get_metadata(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.mp3", "wb") as f:
        f.write(contents)

    audio = MutagenFile("temp.mp3", easy=True)
    metadata = dict(audio.tags) if audio and audio.tags else {}
    return {"filename": file.filename, "metadata": metadata}
