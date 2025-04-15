import yt_dlp
import os

def obtener_carpeta_destino():
    tipos_predefinidos = {
        "1": "peliculas",
        "2": "musica",
        "3": "otro"
    }

    print("\n📁 ¿Qué tipo de contenido vas a descargar?")
    print("1. Películas")
    print("2. Música")
    print("3. Otro")

    opcion = input("📝 Elige una opción (1-3): ").strip()

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
        print(f"✅ Video descargado en la carpeta '{carpeta_destino}'\n")
    except Exception as e:
        print("⚠️ Error durante la descarga:")
        print(e)

def obtener_links():
    print("\n🔗 Ingresa los links uno por uno. Escribe 'fin' para terminar.\n")
    links = []
    while True:
        link = input("🔹 Link: ").strip()
        if link.lower() == "fin":
            break
        elif link:
            links.append(link)
        else:
            print("⚠️ No ingresaste nada.")
    return links

if __name__ == "__main__":
    links = obtener_links()
    if links:
        carpeta = obtener_carpeta_destino()
        for link in links:
            print(f"\n⬇️ Descargando: {link}")
            descargar_video(link, carpeta)
        print("🏁 Todas las descargas han finalizado.")
    else:
        print("❌ No se ingresaron links.")
