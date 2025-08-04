from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from mutagen import File as MutagenFile

app = FastAPI()

@app.post("/metadata/")
async def get_metadata(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.mp3", "wb") as f:
        f.write(contents)
    audio = MutagenFile("temp.mp3", easy=True)
    if not audio:
        return JSONResponse(content={"error": "No se pudieron leer los metadatos"}, status_code=400)
    metadata = dict(audio.tags or {})
    return {"metadata": metadata}