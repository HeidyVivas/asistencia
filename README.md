# Asistencia — Gestión Inteligente de Asistencias

Asistencia es una solución Django lista para producción diseñada para gestionar asistencias, faltas y excusas en instituciones educativas y organizaciones. Construida con una arquitectura modular, ofrece panel administrativo, APIs REST y un flujo de trabajo claro para docentes, administradores y responsables.

Por qué elegir Asistencia
- **Eficiencia**: Registra asistencias y faltas rápidamente desde interfaces web y APIs.
- **Control completo**: Manejo de excusas, faltas y reglamentos centralizado.
- **Escalable y modular**: Separación de funcionalidades por apps (`asistencias`, `faltas`, `excusas`, `usuarios`, `reglamento`, `asistencia_api`).
- **Listo para integrarse**: Endpoints REST y estructura de serializers para integraciones con otros sistemas.

Características principales
- **Registro y seguimiento** de asistencias por grupos y usuarios.
- **Gestión de faltas** y generación de reportes básicos.
- **Sistema de excusas** con almacenamiento y trazabilidad.
- **Panel administrativo** con vistas y plantillas (`templates/dashboard.html`).
- **APIs** para consumo externo en `asistencia_api`.

Estructura del proyecto
- **Apps principales**: `asistencias`, `faltas`, `excusas`, `usuarios`, `reglamento`, `core`, `asistencia_api`.
- **Base de datos**: `db.sqlite3` (configurable en `asistencia_project/settings.py`).
- **Archivos útiles**: `manage.py`, `requirements.txt`, `templates/`, `static/`.

Instalación rápida
1. Clona el repositorio:

   git clone <url-del-repo>
   cd asistencia

2. Crea un entorno virtual e instala dependencias (Windows PowerShell):

   python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt

3. Aplica migraciones y crea un superusuario:

   python manage.py migrate
   python manage.py createsuperuser

4. Inicia el servidor de desarrollo:

   python manage.py runserver

Uso rápido
- Accede al panel administrativo: `http://127.0.0.1:8000/admin/`.
- Dashboard público/privado en `templates/dashboard.html`.
- Consulta y extiende las APIs en la app `asistencia_api` (revisa `serializers.py` y `views.py`).

Extensión e integración
- Añade nuevas API endpoints creando `serializers` y `views` en `asistencia_api`.
- Integra SSO o servicios externos conectando `usuarios` con tu proveedor de identidad.

Contribución
- Forkea el repo y envía pull requests para nuevas funcionalidades o correcciones.
- Sigue las convenciones existentes y añade tests en las carpetas `tests.py` correspondientes.

Soporte y contacto
- ¿Necesitas una adaptación personalizada, despliegue o soporte? Contáctanos en: comercial@example.com

Licencia
- Este proyecto incluye dependencias y código abierto; añade aquí la licencia que prefieras (por ejemplo, MIT).

Listo para probar

Asistencia está pensado para entrar en producción con mínimas adaptaciones de configuración: personaliza `settings.py`, configura tu base de datos y despliega en el hosting de tu preferencia. Empieza a optimizar la gestión de presencia hoy mismo.
