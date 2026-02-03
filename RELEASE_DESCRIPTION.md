# 📦 Transcribe – Release Notes

## 🟢 Versión 1.0 – Primera versión estable

**Fecha de lanzamiento:** 2 de febrero de 2026

### 🚀 Descripción general

Transcribe es una **aplicación de escritorio portable desarrollada en Python** que permite **transcribir audio a texto** de manera rápida, confiable y con un enfoque profesional para usuarios finales. Esta versión está diseñada para ser **totalmente portable**, **compatible con Windows 10 y 11**, y funciona sin necesidad de instalar Python, gracias al entorno virtual incluido y al empaquetado de scripts VBScript.

---

### ✨ Novedades de esta versión

* ✅ **Versión portable completa**: Se puede mover a cualquier carpeta sin romper el acceso directo ni la ejecución.
* 🔐 **Scripts firmados digitalmente**: Todos los scripts principales (`Iniciar.vbs`, `Transcribe.vbs`, `Instalar_acceso_directo.ps1`) cuentan con firma digital válida y timestamp, garantizando seguridad y confianza en Windows.
* 🖥️ **Compatibilidad con rutas dinámicas**: Uso de rutas relativas para que el usuario pueda ubicar la carpeta en cualquier lugar del sistema.
* 🎯 **Automatización de accesos directos**: Se crea el acceso directo en el escritorio automáticamente, con icono personalizado.
* 🪟 **Ejecución silenciosa de la app**: La aplicación principal se ejecuta en segundo plano sin abrir ventanas de consola.
* 📂 **Validación de entorno**: Mensajes claros si falta el entorno virtual o archivos críticos, evitando errores inesperados.
* 📄 **Documentación completa**: README y RELEASE_DESCRIPTION incluidas, detallando instalación, ejecución y funcionalidades.
* 🌐 Internacionalización (i18n)

---

### ⚡ Detalles técnicos

* **Lenguaje:** Python 3.11
* **UI:** Python + Tkinter
* **Scripts auxiliares:** VBScript (`.vbs`) y PowerShell (`.ps1`)
* **Empaquetado:** Portable con entorno virtual (`venv`)
* **Seguridad:** Firma digital con timestamp aplicada automáticamente
* **Compatibilidad:** Windows 10 y 11

---

### 📂 Estructura de archivos

```
Transcribe
│
├── bin/             # Archivos binarios auxiliares
├── config/          # Configuración general
├── core/            # Lógica principal de transcripción
├── gui/             # Interfaz de usuario
├── images/          # Recursos gráficos
├── utils/           # Funciones auxiliares
├── venv/            # Entorno virtual portable
├── hotkey_server.py # Servidor de hotkeys (opcional)
├── Iniciar.vbs      # Lanzador principal
├── Transcribe.vbs   # Lanzador alternativo
├── Instalar_acceso_directo.ps1 # Script de creación de acceso directo
├── README.md
├── RELEASE_DESCRIPTION.md
├── requirements.txt
└── ui_main.py       # Script principal de la aplicación
```

---

### 📌 Recomendaciones de uso

1. Extraer la carpeta en cualquier ubicación del sistema.
2. Crear el entorno virtual:

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

3. Ejecutar `Iniciar.vbs` para crear el acceso directo y lanzar la aplicación.
4. El acceso directo en el escritorio apunta automáticamente al script correcto, usando rutas relativas.
5. No se requiere instalación de Python ni dependencias adicionales.

---

### 🛠️ Mejoras futuras

* Integración de servicios de transcripción en la nube para mayor precisión.
* Registro de historial de transcripciones.
* Función de exportación a distintos formatos de texto.
* Posible migración a interfaz más moderna con WPF o PyQt.

---

### 👨‍💻 Autor

**Walter Pablo Téllez Ayala**
📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com)

---
