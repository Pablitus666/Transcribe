# 📦 Transcribe – Release Notes

## 🟢 Versión 2.0.0 – Reescritura completa en Python (Breaking Change)

**Fecha de lanzamiento:** 2 de febrero de 2026

---

## ⚠️ Aviso importante (Breaking Change)

A partir de la **versión 2.0**, Transcribe fue **reescrito completamente en Python** y **ya no utiliza VBScript** ni distribución portable manual.

La implementación anterior basada en VBScript se conserva únicamente bajo el tag:

```
v1.0-vbscript
```

---

## 🚀 Descripción general

**Transcribe 2.0** es una **aplicación de escritorio para Windows** que permite **transcribir audio a texto** de forma rápida, confiable y profesional.

Esta versión introduce una **distribución moderna basada en instalador**, con **ejecutables firmados digitalmente**, integración nativa con Windows y una experiencia de usuario más robusta.

No requiere Python instalado ni configuraciones manuales.

---

## ✨ Novedades principales

* 🧠 **Reescritura completa en Python**
* ⌨️ **Hotkeys nativos** (sin scripts externos)
* 📦 **Distribución mediante instalador (Inno Setup)**
* 🔐 **Ejecutables firmados digitalmente**
* 🖥️ **Instalación automática en Program Files**
* 🚀 **Inicio rápido y ejecución estable**
* ❌ **Eliminación total de VBScript**
* 🧹 **Arquitectura más limpia y mantenible**

---

## 🔐 Seguridad y firma digital

* `Transcribe.exe` → firmado digitalmente
* `Transcribe_Setup.exe` → firmado digitalmente
* Certificado autofirmado (válido para desarrollo)
* Windows puede mostrar advertencia leve al instalar (esperado)

---

## ⚙️ Detalles técnicos

* **Lenguaje:** Python 3.11
* **UI:** Python + Tkinter
* **Hotkeys:** Implementación nativa
* **Empaquetado:** PyInstaller
* **Instalador:** Inno Setup
* **Firma:** Authenticode (certificado de desarrollo)
* **Compatibilidad:** Windows 10 y Windows 11 (64-bit)

---

## 📦 Distribución

### Archivo incluido en este Release

```
Transcribe_Setup.zip
```

Contenido del ZIP:

```
Transcribe_Setup.exe
```

### Instalación

1. Descargar `Transcribe_Setup.zip`
2. Extraer el archivo
3. Ejecutar `Transcribe_Setup.exe`
4. Seguir el asistente de instalación
5. Acceso directo creado automáticamente

---

## ❌ Cambios respecto a versiones anteriores

* Eliminado:

  * VBScript (`.vbs`)
  * Entorno virtual manual
  * Ejecución portable
  * Configuración manual de dependencias
* Ya no es necesario:

  * Instalar Python
  * Ejecutar scripts auxiliares
  * Configurar rutas manualmente

---

## 🛠️ Mejoras futuras

* Integración de servicios de transcripción en la nube
* Historial de transcripciones
* Exportación a múltiples formatos
* Interfaz gráfica más moderna (PyQt / WPF)
* Certificado EV para eliminar advertencias de Windows

---

## 👨‍💻 Autor

**Walter Pablo Téllez Ayala**

📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com)
