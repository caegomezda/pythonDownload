# 🎵 YouTube Downloader con Interfaz Gráfica

Este es un pequeño programa hecho en **Python** que permite descargar **videos o música desde YouTube** a través de una **interfaz gráfica sencilla**. Utiliza la biblioteca `yt-dlp` para realizar las descargas y `tkinter` para la interfaz de usuario.

---

## ✅ Requisitos

Antes de usar este programa, asegúrate de tener lo siguiente:

- ✅ Python 3.7 o superior instalado en tu PC.
- ✅ Acceso a una consola (CMD, Terminal o PowerShell).
- ✅ Conexión a internet para descargar los videos.

---

## 🧩 Instalación de dependencias

Este programa requiere `yt-dlp`, una poderosa herramienta para descargas desde YouTube y otras plataformas.

Para instalarla, abre tu terminal y ejecuta:

```bash
pip install yt-dlp

▶️ Cómo ejecutar el programa

    📥 Descarga o clona este repositorio en tu computadora.

    📂 Abre una terminal y navega hasta la carpeta del proyecto.

    ▶️ Ejecuta el programa con:

python main.py

    ⚠️ Si tu archivo se llama distinto (por ejemplo descargador.py), reemplaza main.py por el nombre correcto.

🖼️ Interfaz de Usuario

Cuando ejecutes el programa, verás una ventana con:

    🔗 Campo de enlace: pega aquí la URL del video de YouTube.

    ⬇️ Botón "Descargar": inicia la descarga.

    📊 Barra de progreso: muestra en tiempo real cómo va la descarga.

    📣 Mensajes de estado: te indican si todo va bien, si terminó o si hubo un error.

🔧 ¿Qué hace este programa?

    🎶 Detecta si el contenido es música (categoría "Music") y lo descarga como archivo .mp3.

    📹 Si no es música, descarga el video en formato .mp4 con la mejor calidad disponible.

    📈 Muestra una barra de progreso en tiempo real.

    📁 Guarda los archivos en una carpeta llamada descargas/ automáticamente.

✨ Personalización

Puedes adaptar el comportamiento del programa fácilmente:

    🗂️ Ruta de descarga: cambia la variable carpeta_destino en el código si deseas otra ubicación.

    🎛️ Formato de descarga: puedes forzar siempre audio o video modificando las opciones de yt-dlp.

❓ Problemas comunes
Problema	Solución
❌ Error al importar yt_dlp	Asegúrate de haber ejecutado pip install yt-dlp.
❌ El botón no hace nada	Verifica que hayas pegado una URL válida de YouTube.
❌ La barra se queda en gris	Revisa que el hook de progreso esté funcionando correctamente.
❌ El programa se cierra solo	Ábrelo desde la terminal para poder ver si aparece algún mensaje de error.
📁 Estructura del Proyecto

proyecto_descargador/
├── main.py          # Código principal (interfaz + lógica de descarga)
├── README.md        # Este archivo con la explicación
└── descargas/       # Carpeta donde se guardan los archivos descargados

💡 Sugerencia: Crear un .EXE (Windows)

Puedes convertir este programa en un archivo ejecutable .exe para compartirlo fácilmente con otros usuarios que no tienen Python.

pip install pyinstaller
pyinstaller --onefile main.py

Esto generará un archivo ejecutable en la carpeta /dist.
📬 Contacto

¿Ideas, dudas o mejoras? ¡Este proyecto es completamente abierto!
Está comentado y pensado para que cualquier persona pueda adaptarlo a sus necesidades sin complicaciones.

¡Gracias por usar esta app!
