import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Menu
import os
import subprocess
import threading
import yt_dlp
import sys
import random
import pygame
import time

TIPOS_CARPETAS = {
    "Películas 🎥": "peliculas",
    "Música 🎶": "musica",
    "Otro 🧹": "otro"
}
canciones_aleatorias = []
indice_actual = 0

class ProgresoDescarga(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("⏳ Descargando...")
        self.geometry("300x100")
        self.resizable(False, False)

        # self.barra = ttk.Progressbar(self, length=250, mode='determinate')
        self.barra = ttk.Progressbar(self, length=250, mode='determinate', maximum=100)

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

def descargar_con_tipo(tipo_seleccionado):
    url = simpledialog.askstring("🔗 URL", "Pega el link del video:")
    if not url:
        return

    if tipo_seleccionado == "Otro 🧹":
        tipo_carpeta = simpledialog.askstring("📁 Carpeta personalizada", "Escribe el nombre de la carpeta:")
        if not tipo_carpeta:
            return
        tipo_carpeta = os.path.join("otro", tipo_carpeta)
    else:
        tipo_carpeta = TIPOS_CARPETAS[tipo_seleccionado]

    os.makedirs(tipo_carpeta, exist_ok=True)
    ventana_progreso = ProgresoDescarga(root)

    def hook(d):
        if d['status'] == 'downloading':
            porcentaje_str = d.get('_percent_str', '0.0%').strip().replace('%', '').replace(',', '.')
            try:
                porcentaje = float(porcentaje_str)
                texto = f"{d['_percent_str']} - {d.get('eta', '?')}s restantes"
                ventana_progreso.actualizar(porcentaje, texto)
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
            mostrar_contenido(tab_actual.get())
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo descargar: {e}")
        finally:
            ventana_progreso.cerrar()

    threading.Thread(target=tarea, daemon=True).start()

def abrir_archivo(ruta):
    try:
        if os.name == 'nt':
            os.startfile(ruta)
        else:
            subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', ruta])
    except Exception as e:
        messagebox.showerror("❌ Error", f"No se pudo abrir: {e}")

def mostrar_contenido(tipo):
    filtro = entrada_filtro.get().lower().strip()

    for item in lista.get_children():
        lista.delete(item)

    rutas = []
    if tipo == "Música 🎶":
        carpeta = TIPOS_CARPETAS[tipo]
        if not os.path.isdir(carpeta):
            return
        FORMATOS_VALIDOS = (".mp3", ".mp4", ".wav", ".m4a")
        rutas = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith(FORMATOS_VALIDOS)]
    elif tipo == "Películas 🎥":
        carpeta = TIPOS_CARPETAS[tipo]
        if not os.path.isdir(carpeta):
            return
        rutas = [os.path.join(carpeta, f) for f in os.listdir(carpeta)]
    elif tipo.startswith("otro/"):
        carpeta = tipo
        if not os.path.isdir(carpeta):
            return
        FORMATOS_VALIDOS = (".mp3", ".mp4", ".wav", ".m4a")
        rutas = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith(FORMATOS_VALIDOS)]

    for archivo in rutas:
        nombre = os.path.basename(archivo)
        if filtro in nombre.lower():  # <-- aquí se aplica el filtro
            lista.insert("", "end", values=(nombre, archivo))

def reproducir_todo_aleatorio():
    global canciones_aleatorias, indice_actual
    carpeta = TIPOS_CARPETAS["Música 🎶"]
    if not os.path.isdir(carpeta):
        messagebox.showinfo("🎵", "No hay canciones para reproducir.")
        return
    FORMATOS_VALIDOS = (".mp3", ".mp4", ".wav", ".m4a")
    canciones_aleatorias = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith(".mp3")]
    if not canciones_aleatorias:
        messagebox.showinfo("🎵", "No hay archivos MP3 en la carpeta.")
        return
    random.shuffle(canciones_aleatorias)
    indice_actual = 0
    iniciar_reproduccion()

def iniciar_reproduccion():
    global canciones_aleatorias, indice_actual

    def reproducir():
        global indice_actual
        pygame.mixer.init()
        while indice_actual < len(canciones_aleatorias):
            archivo = canciones_aleatorias[indice_actual]
            try:
                nombre = os.path.basename(archivo)
                cancion_actual_label.config(text=f"🎵 Sonando ahora: {nombre}")
                pygame.mixer.music.stop()
                pygame.mixer.music.load(archivo)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.5)
            except Exception as e:
                messagebox.showerror("❌ Error", f"No se pudo reproducir: {e}")
            indice_actual += 1
        pygame.mixer.quit()
        cancion_actual_label.config(text="🎵 Reproducción finalizada")

    threading.Thread(target=reproducir, daemon=True).start()

def siguiente_cancion():
    global indice_actual
    if not canciones_aleatorias or indice_actual >= len(canciones_aleatorias) - 1:
        cancion_actual_label.config(text="🎵 No hay más canciones.")
        return
    indice_actual += 1
    pygame.mixer.music.stop()
    iniciar_reproduccion()

def cancion_anterior():
    global indice_actual
    if not canciones_aleatorias or indice_actual >= len(canciones_aleatorias) - 1:
        cancion_actual_label.config(text="🎵 No hay más canciones.")
        return
    indice_actual -= 1
    pygame.mixer.music.stop()
    iniciar_reproduccion()  

root = tk.Tk()
root.title("🎵 Descargador Multicarpeta")
root.geometry("800x700")

tab_actual = tk.StringVar(value="Música 🎶")


entrada_filtro = tk.Entry(root, width=50)
entrada_filtro.pack(pady=5)
entrada_filtro.bind("<Return>", lambda event: mostrar_contenido(tab_actual.get()))
entrada_filtro.bind("<KeyRelease>", lambda e: mostrar_contenido(tab_actual.get()))
tk.Button(root, text="🔍 Buscar", command=lambda: mostrar_contenido(tab_actual.get())).pack()


frame_tabla = tk.Frame(root)
frame_tabla.pack()

scroll = tk.Scrollbar(frame_tabla)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

lista = ttk.Treeview(frame_tabla, columns=("Nombre", "Ruta"), show="headings", yscrollcommand=scroll.set, height=20)
lista.heading("Nombre", text="🔹 Archivo")
lista.heading("Ruta", text="🔹 Ruta")
lista.column("Nombre", width=200)
lista.column("Ruta", width=450)
lista.pack(side=tk.LEFT)

scroll.config(command=lista.yview)

lista.bind("<Double-Button-1>", lambda e: abrir_archivo(lista.item(lista.focus(), "values")[1]))

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

for tipo in TIPOS_CARPETAS:
    tk.Button(frame_botones, text=f"⬇️ {tipo}", command=lambda t=tipo: descargar_con_tipo(t)).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="🎲 Reproducir Todo Aleatoriamente", command=reproducir_todo_aleatorio).pack(pady=10)
tk.Button(root, text="⏭️ Canción Anterior", command=cancion_anterior).pack()
tk.Button(root, text="⏭️ Siguiente Canción", command=siguiente_cancion).pack()


menu_tabs = tk.Menu(root)

submenu = tk.Menu(menu_tabs, tearoff=0)

for tipo in ["Música 🎶", "Películas 🎥"]:
    menu_tabs.add_command(label=tipo, command=lambda t=tipo: (tab_actual.set(t), mostrar_contenido(t)))


if os.path.isdir("otro"):
    for subcarpeta in os.listdir("otro"):
        ruta = os.path.join("otro", subcarpeta)
        if os.path.isdir(ruta):
            submenu.add_command(label=subcarpeta, command=lambda s=subcarpeta: (tab_actual.set(f"otro/{s}"), mostrar_contenido(f"otro/{s}")))


menu_tabs.add_cascade(label="Otro 🧹", menu=submenu)

root.config(menu=menu_tabs)

mostrar_contenido("Música 🎶")
# Mostrar la canción actual
cancion_actual_label = tk.Label(root, text="🎵 Nada sonando por ahora", font=("Arial", 12, "bold"))
cancion_actual_label.pack()

agradecimiento = tk.Label(root, text="🌟 ¡Gracias por usar esta app! Hecha con amor y beats. 🎶\nSi esto alegró tu día, ya valió la pena. ❤️", fg="gray", font=("Arial", 10, "italic"))
agradecimiento.pack(pady=10)

root.mainloop()
