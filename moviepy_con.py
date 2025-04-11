import os
import subprocess

# Ruta a la carpeta con los videos
carpeta = r"C:\Users\HP\code\pythonScripts\videoDowloader\musica"

# Asegúrate de que ffmpeg esté instalado y disponible en el PATH
for archivo in os.listdir(carpeta):
    if archivo.endswith(".mp4"):
        ruta_video = os.path.join(carpeta, archivo)
        nombre_sin_ext = os.path.splitext(archivo)[0]
        ruta_audio = os.path.join(carpeta, nombre_sin_ext + ".mp3")

        comando = ["ffmpeg", "-i", ruta_video, "-q:a", "0", "-map", "a", ruta_audio]
        subprocess.run(comando, shell=True)

print("✅ Conversión completa.")
