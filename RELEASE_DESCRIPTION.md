# 📦 Transcribe – Notas de la Versión

## 🟢 Versión 1.0.0 – Edición Estable

**Fecha:** 31 de marzo de 2026

---

## 🚀 Resumen del Lanzamiento

Esta actualización consolida a **Transcribe** como una herramienta técnica de reproducción para transcripción, introduciendo mejoras críticas en la seguridad de la interfaz y la estabilidad del sistema de atajos de teclado.

---

## ✨ Cambios destacados

### 🛠️ Interfaz y Experiencia de Usuario (UX)
- **Nuevo Botón "Borrar"**: Se añade un control físico en la barra inferior para limpiar el contenido cargado.
- **Bloqueo Lógico de Seguridad**: Sistema que protege los controles durante la carga de archivos. La interfaz permanece visualmente intacta pero inactiva para evitar errores de concurrencia.
- **Botón de Salida Inmune**: Se garantiza que el botón de cerrar sea siempre funcional, incluso durante procesos de carga pesados.
- **Feedback de Cursor**: El cursor cambia automáticamente a estado de espera cuando la aplicación procesa archivos.

### ⌨️ Sistema de Hotkeys (Teclas Globales)
- **Eliminación de Tecla Supr**: Se ha desactivado la tecla `Suprimir` del sistema de captura global para prevenir borrados accidentales cuando la aplicación está minimizada.
- **Optimización de Elevación**: Mejora en el lanzamiento del servidor de hotkeys para una detección precisa del entorno (Desarrollo vs Producción).

### ⚙️ Mejoras Técnicas
- **Robustez de Configuración**: Corrección de importaciones para asegurar la carga de `settings.py` en entornos empaquetados (.exe).
- **Firma Digital**: Todos los binarios e instaladores cuentan con firma digital SHA256 verificada por Walter Pablo Téllez Ayala.

---

## ⚙️ Detalles de Distribución

- **Empaquetado**: PyInstaller (OneDir).
- **Instalador**: Inno Setup (x64).
- **Compatibilidad**: Windows 10 / 11.

---

## 👨‍💻 Autor

**Walter Pablo Téllez Ayala**
📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com)
