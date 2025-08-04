from fastapi import FastAPI, UploadFile, File
from mutagen import File as AudioFile
import os
import tempfile

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API funcionando"}

@app.post("/metadata/")
async def get_metadata(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    audio = AudioFile(tmp_path)
    os.remove(tmp_path)

    if audio is None:
        return {"error": "Formato de archivo no compatible o corrupto"}

    metadata = {
        "mime": audio.mime,
        "info": str(audio.info),
        "tags": dict(audio.tags) if audio.tags else {}
    }
    return metadata


