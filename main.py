from fastapi import FastAPI, File, UploadFile
from mutagen import File as MutagenFile
import uvicorn
import os  # Importar os para manejo de archivos temporales

app = FastAPI()

@app.post("/metadata")  # Quité la barra diagonal final
async def get_metadata(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.mp3", "wb") as f:
        f.write(contents)

    audio = MutagenFile("temp.mp3", easy=True)
    metadata = dict(audio.tags) if audio and audio.tags else {}
    
    # Eliminar el archivo temporal después de usarlo
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")
        
    return {"filename": file.filename, "metadata": metadata}
