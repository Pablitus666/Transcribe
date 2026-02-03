# 🎙️ Transcribe

Transcribe es una aplicación de escritorio desarrollada en **Python (Tkinter)** orientada a la **transcripción** profesional de **audio** y **video**, pensada como una suite portable para Windows, estable, ligera y firmada digitalmente.

El proyecto está diseñado para ofrecer una experiencia sólida al usuario final: sin dependencias frágiles en producción, con compatibilidad DPI, ejecutable firmado y un sistema de lanzamiento portable que inspira confianza.

---
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=flat&logo=windows&logoColor=white)
![Language](https://img.shields.io/badge/language-Python-3776AB?style=flat&logo=python&logoColor=white)
![UI](https://img.shields.io/badge/UI-Tkinter-FFDD54?style=flat)
![Packaging](https://img.shields.io/badge/packaged%20with-PyInstaller-4B8BBE?style=flat)
![Executable](https://img.shields.io/badge/output-.exe-5C2D91?style=flat)
![Status](https://img.shields.io/badge/status-stable-brightgreen?style=flat)
![Security](https://img.shields.io/badge/code%20signing-signed-success?style=flat)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)
![Transcription](https://img.shields.io/badge/transcription-real--time-blue?style=flat)
![DPI](https://img.shields.io/badge/DPI-aware-success?style=flat)
![Development](https://img.shields.io/badge/dev%20mode-drag%20%26%20drop-lightgrey?style=flat)

---

![Social Preview](images/Preview.png)

---

## 🎯 Objetivo del proyecto

Transcribe nace con el objetivo de ofrecer una herramienta simple, confiable y profesional para convertir grabaciones de audio y video en texto, manteniendo una arquitectura limpia, una interfaz clara y un enfoque 100 % portable en Windows.

El proyecto evita soluciones pesadas o inestables y prioriza la seguridad, la experiencia del usuario y las buenas prácticas de distribución.

---

## ✨ Características principales

* 🎙️ Transcripción de audio y video a texto
* ⌨️ Control mediante teclas rápidas F1, F2, F3 y F4 para reproducción y navegación
* 📂 Soporte para múltiples formatos (WAV, MP3, MP4, MKV, entre otros)
* 🖼️ Interfaz escalable según DPI (HiDPI / 4K)
* 🎨 Uso de iconografía HD escalable y elementos gráficos modernos
* 🧠 Separación clara entre UI, configuración y utilidades
* 🪟 Ventana centrada y tamaño fijo
* 🔏 Firma digital de los scripts y ejecutables
* 📦 Ejecutable .exe portable (no requiere Python)
* 🚫 Eliminación de dependencias inestables en producción

---

## 🖼️ Interfaz

* Diseño limpio y profesional
* Selección directa de archivos de audio o video
* Controles de reproducción (retroceder, reproducir, detener, avanzar)
* Slider de ganancia de decibeles
* Slider de volumen
* Escalado automático según la resolución del sistema
* Escalado automático según resolución del sistema

---

## 🧱 Arquitectura del proyecto

```
Transcribe
│
├── app
│ ├── config.py # Configuración global (colores, tamaños, AppID)
│ ├── ui_main.py # Punto de entrada de la interfaz
│ ├── utils.py # Utilidades y helpers de transcripción
│
├── gui # Componentes de la interfaz gráfica
├── core # Módulos de soporte (DPI, hotkeys, etc.)
├── images # Recursos gráficos HD
├── venv # Entorno virtual (desarrollo)
├── Iniciar.vbs # Lanzador principal portable
├── Transcribe.vbs # Lanzador alternativo
├── Instalar_acceso_directo.ps1 # Instalador de acceso directo
├── requirements.txt
└── main.spec # Configuración de PyInstaller
```

---

## 📷 Capturas de pantalla

<p align="center">
  <img src="images/screenshot.png?v=2" alt="Vista previa de la aplicación" width="600"/>
</p>

---

## 🧠 Detalles técnicos destacados

* DPI Awareness activado para evitar imágenes borrosas
* Escalado automático de iconos e interfaz según factor de resolución
* Detección automática del entorno:
  * 🧪 Desarrollo → Drag & Drop habilitado
  * 📦 Producción (.exe) → Drag & Drop deshabilitado
* Sistema de hotkeys ejecutado con elevación controlada en Windows
* Ejecutable y scripts firmados digitalmente para mayor confianza en Windows
* Sistema de lanzamiento portable mediante Iniciar.vbs y Transcribe.vbs

---

## 🚀 Ejecución

* Descarga la última versión estable desde GitHub Releases:

👉 Descargar desde GitHub Releases:
https://github.com/Pablitus666/Transcribe/releases

Pasos:

  * Descarga el archivo .zip desde Releases

  * Extrae el contenido 

  * Ejecuta Transcribe.exe

  * No requiere Python instalado ni dependencias externas

## Opción 2: Ejecución en desarrollo

  * cd Transcribe

  * crear el entorno virtual:

```
py -3.11 -m venv venv

```
  * activar el entorno virtual:

```
.\venv\Scripts\Activate.ps1

```
  * Instalar dependencias:

```
pip install -r requirements.txt

```
  * Ejecutar script principal:

```
python ui_main.py

```
---

## 📦 Estado del proyecto

- ✔️ Estable 
- ✔️ Portable y listo para uso real
- ✔️ Enfoque profesional 
- ✔️ Compatible con Windows 10 / 11

---

## 🔮 Posibles mejoras futuras

* Soporte para múltiples archivos de audio simultáneos
* Historial de archivos procesados
* Migración opcional a CustomTkinter para interfaz más moderna

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

---

## 🤝 Contribuciones

Las contribuciones, sugerencias y mejoras son bienvenidas.  
Si encuentras un problema o tienes una idea, no dudes en abrir un *issue* o *pull request*.

---

## 👨‍💻 Autor

Proyecto creado con enfoque en **calidad, estabilidad y buenas prácticas**.

*   **Nombre:** Pablo Téllez
*   **Contacto:** pharmakoz@gmail.com

---

⚖️ Nota legal

---

Este software está destinado al uso legítimo sobre grabaciones de audio de las cuales el usuario tenga autorización. El autor no se responsabiliza por el uso indebido de la herramienta.