# Sistema-tickets-django

Proyecto de portafolio de Estructuras de Datos y Algoritmos (Tecsup), desarrollado con Django.

## Iniciar en Windows (PowerShell)

Ejecuta estos comandos desde la carpeta del proyecto:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py runserver
```

Abre http://127.0.0.1:8000/ en el navegador. Para detener el servidor, presiona `Ctrl+C`.

Si el entorno `venv` ya existe y las dependencias estan instaladas, normalmente solo necesitas ejecutar:

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Ejecuta `migrate` despues de descargar cambios que incluyan nuevas migraciones. Esto actualiza la base SQLite (`db.sqlite3`) para que coincida con los modelos de Django.

## Asignar un agente a un ticket

En el formulario de crear o editar un ticket, selecciona el agente encargado. La lista muestra los agentes registrados en **Usuarios** del panel `/admin/`. Si el ticket aun no tiene responsable, puedes dejar la opcion **Sin asignar**.
