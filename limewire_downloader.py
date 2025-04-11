import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import subprocess
import threading
import yt_dlp
import sys
import json
import random
import pygame
import time

TIPOS_CARPETAS = {
    "Películas 🎥": "peliculas",
    "Música 🎶": "musica",
    "Otro 🧩": "otro"
}

# --- INTERFAZ DE PROGRESO ---
class ProgresoDescarga(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("⏳ Descargando...")
        self.geometry("300x100")
        self.resizable(False, False)

        self.barra = ttk.Progressbar(self, length=250, mode='determinate')
        self.barra.pack(pady=10)

        self.label = tk.Label(self, text="Iniciando descarga...")
        self.label.pack()

    def actualizar(self, porcentaje, texto=None):
        self.barra['value'] = porcentaje
        if texto:
            self.label.config(text=texto)
        self.update_idletasks()

    def cerrar(self):
        self.destroy()

# Descargar según tipo de archivo
def descargar_con_tipo(tipo_seleccionado):
    url = simpledialog.askstring("🔗 URL", "Pega el link del video:")
    if not url:
        return

    if tipo_seleccionado == "Otro 🧩":
        tipo_carpeta = simpledialog.askstring("📁 Carpeta personalizada", "Escribe el nombre de la carpeta:")
        if not tipo_carpeta:
            return
    else:
        tipo_carpeta = TIPOS_CARPETAS[tipo_seleccionado]

    os.makedirs(tipo_carpeta, exist_ok=True)
    ventana_progreso = ProgresoDescarga(root)

    def hook(d):
        if d['status'] == 'downloading':
            porcentaje = d.get('_percent_str', '0.0%').strip().replace('%', '')
            texto = f"{d['_percent_str']} - {d.get('eta', '?')}s restantes"
            try:
                ventana_progreso.actualizar(float(porcentaje), texto)
            except:
                pass
        elif d['status'] == 'finished':
            ventana_progreso.actualizar(100, "✅ ¡Descarga completa!")

    def tarea():
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                categories = info.get('categories', [])
                is_music = 'Music' in categories or info.get('genre') == 'Music'

            if is_music:
                opciones = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{tipo_carpeta}/%(title)s.%(ext)s',
                    'quiet': True,
                    'progress_hooks': [hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            else:
                opciones = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': f'{tipo_carpeta}/%(title)s.%(ext)s',
                    'quiet': True,
                    'progress_hooks': [hook],
                    'merge_output_format': 'mp4',
                }

            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])

            messagebox.showinfo("✅ Descargado", f"Guardado en '{tipo_carpeta}'")
            actualizar_lista()
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo descargar: {e}")
        finally:
            ventana_progreso.cerrar()

    threading.Thread(target=tarea, daemon=True).start()

# Mostrar solo música
def actualizar_lista(filtro=""):
    for item in lista.get_children():
        lista.delete(item)
    if not os.path.isdir("musica"):
        return
    for archivo in os.listdir("musica"):
        if filtro.lower() in archivo.lower():
            nombre, _ = os.path.splitext(archivo)
            if " - " in nombre:
                artista, cancion = nombre.split(" - ", 1)
            else:
                artista, cancion = "Desconocido", nombre
            lista.insert("", "end", values=(cancion.strip(), artista.strip()))

# Filtrar lista
def filtrar_lista(event=None):
    filtro = entrada_filtro.get()
    actualizar_lista(filtro)

# Abrir archivo
def abrir_archivo(event):
    item = lista.focus()
    if item:
        nombre_archivo = lista.item(item, "values")[0]
        for archivo in os.listdir("musica"):
            if nombre_archivo in archivo:
                ruta = os.path.abspath(os.path.join("musica", archivo))
                try:
                    if os.name == 'nt':
                        os.startfile(ruta)
                    else:
                        subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', ruta])
                except Exception as e:
                    messagebox.showerror("❌ Error", f"No se pudo abrir: {e}")
                break

# Reproducción aleatoria
def reproducir_todo_aleatorio():
    if not os.path.isdir("musica"):
        messagebox.showinfo("🎧", "No hay canciones para reproducir.")
        return

    archivos = [os.path.join("musica", f) for f in os.listdir("musica") if f.lower().endswith(".mp3")]
    if not archivos:
        messagebox.showinfo("🎧", "No hay archivos MP3 en la carpeta.")
        return

    random.shuffle(archivos)

    def reproducir():
        pygame.mixer.init()
        for archivo in archivos:
            try:
                pygame.mixer.music.load(archivo)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.5)
            except Exception as e:
                messagebox.showerror("❌ Error", f"No se pudo reproducir: {e}")
        pygame.mixer.quit()

    threading.Thread(target=reproducir, daemon=True).start()
# --- INTERFAZ PRINCIPAL ---
root = tk.Tk()
root.title("🎵 Descargador Multicarpeta")
root.geometry("600x600")

# Entrada de filtro
entrada_filtro = tk.Entry(root, width=50)
entrada_filtro.pack(pady=5)
entrada_filtro.bind("<KeyRelease>", filtrar_lista)

# Lista estilo tabla con scroll
frame_tabla = tk.Frame(root)
frame_tabla.pack()

scroll = tk.Scrollbar(frame_tabla)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

lista = ttk.Treeview(frame_tabla, columns=("Canción", "Artista"), show="headings", yscrollcommand=scroll.set, height=20)
lista.heading("Canción", text="🎵 Canción")
lista.heading("Artista", text="🎤 Artista")
lista.column("Canción", width=300)
lista.column("Artista", width=250)
lista.pack(side=tk.LEFT)

scroll.config(command=lista.yview)
lista.bind("<Double-Button-1>", abrir_archivo)

# Botones de tipo
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

for tipo in TIPOS_CARPETAS:
    boton = tk.Button(frame_botones, text=f"⬇️ {tipo}", command=lambda t=tipo: descargar_con_tipo(t))
    boton.pack(side=tk.LEFT, padx=10)

# Botón de reproducción aleatoria
boton_reproducir_aleatorio = tk.Button(root, text="🎲 Reproducir Todo Aleatoriamente", command=reproducir_todo_aleatorio)
boton_reproducir_aleatorio.pack(pady=10)

# Mensaje de agradecimiento
agradecimiento = tk.Label(
    root,
    text="🌟 ¡Gracias por usar esta app! Hecha con amor y beats. 🎶\n"
         "Si esto alegró tu día, ya valió la pena. ❤️",
    fg="gray",
    font=("Arial", 10, "italic")
)
agradecimiento.pack(pady=10)

# Iniciar con lista actual
actualizar_lista()

# Ejecutar app
root.mainloop()
