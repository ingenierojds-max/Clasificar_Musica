from fastapi import FastAPI, File, UploadFile
from mutagen import File as MutagenFile
import uvicorn

app = FastAPI()

@app.post("/metadata")
async def get_metadata(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open("temp.mp3", "wb") as f:
            f.write(contents)

        # Usamos MutagenFile para abrir el archivo.
        # 'easy=True' simplifica el acceso a tags comunes.
        audio = MutagenFile("temp.mp3", easy=True)
        
        # Inicializamos metadata como un diccionario vacío si audio o audio.tags es None.
        metadata = dict(audio.tags) if audio and audio.tags else {}
        
        return {"filename": file.filename, "metadata": metadata}
    except Exception as e:
        # Capturamos cualquier excepción que pueda ocurrir durante el procesamiento.
        # Esto podría ser un error al leer el archivo, al usar mutagen, etc.
        # Devolvemos un mensaje de error para depuración.
        return {"filename": file.filename, "error": str(e)}

# Si quieres ejecutar la aplicación localmente para probarla:
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
