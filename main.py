from fastapi import FastAPI, File, UploadFile
from mutagen import File as MutagenFile
import uvicorn
import os

app = FastAPI()

@app.post("/metadata")
async def get_metadata(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.mp3", "wb") as f:
        f.write(contents)

    audio = MutagenFile("temp.mp3", easy=True)
    metadata = dict(audio.tags) if audio and audio.tags else {}
    
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")
        
    return {"filename": file.filename, "metadata": metadata}

# Asegúrate de que esta parte esté indentada correctamente
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # ← 4 espacios o un tab antes
