import yt_dlp
import os

def obtener_carpeta_destino():
    tipos_predefinidos = {
        "1": "peliculas",
        "2": "porno",
        "3": "musica",
        "4": "otro"
    }

    print("\n📁 ¿Qué tipo de contenido vas a descargar?")
    print("1. Películas")
    print("2. Porno")
    print("3. Música")
    print("4. Otro")

    opcion = input("📝 Elige una opción (1-4): ").strip()

    if opcion == "4":
        nueva = input("🆕 Escribe el nombre de la nueva carpeta: ").strip()
        if nueva:
            carpeta = nueva
        else:
            print("⚠️ No escribiste ningún nombre. Usando carpeta 'otro'")
            carpeta = "otro"
    elif opcion in tipos_predefinidos:
        carpeta = tipos_predefinidos[opcion]
    else:
        print("❌ Opción no válida. Usando carpeta 'otro'")
        carpeta = "otro"

    os.makedirs(carpeta, exist_ok=True)
    return carpeta

def descargar_video(url, carpeta_destino):
    opciones = {
        'format': 'best',
        'outtmpl': f'{carpeta_destino}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        print(f"✅ Video descargado en la carpeta '{carpeta_destino}'")
    except Exception as e:
        print("⚠️ Error durante la descarga:")
        print(e)

if __name__ == "__main__":
    url = input("🔗 Ingresa la URL del video de YouTube: ").strip()
    if url:
        carpeta = obtener_carpeta_destino()
        descargar_video(url, carpeta)
    else:
        print("❌ No ingresaste una URL.")
