# AGENTS.md — Sistema de Tickets Django

## Stack y cómo levantar el servidor

- Django 6.1.1, configuración en `config/settings.py`, punto de entrada `manage.py` (raíz).
- App única: `tickets`. Base de datos SQLite (`db.sqlite3`).
- No hay `pytest`; los tests son `django.test.TestCase` en `tickets/tests.py`.

Desde la raíz del proyecto:

```bash
# 1. Crear y activar entorno virtual (Linux/Mac)
python -m venv venv
source venv/bin/activate

# 2. Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones (requerido antes de runserver)
python manage.py makemigrations tickets
python manage.py migrate

# 5. Servidor
python manage.py runserver
# http://127.0.0.1:8000/  (panel admin: /admin/)
```

## Comandos ejecutables de alto valor

| Propósito | Comando |
|-----------|---------|
| Correr todos los tests | `python manage.py test tickets` |
| Correr un solo test | `python manage.py test tickets.TicketAgentAssignmentTests.test_new_ticket_form_lists_agents_and_assigns_selected_agent` |
| Crear migraciones | `python manage.py makemigrations tickets` |
| Aplicar migraciones | `python manage.py migrate` |
| Revisar errores sin servidor | `python manage.py check` |
| Crear superuser | `python manage.py createsuperuser` |

Orden cuando toca modelos: `makemigrations` → `migrate` → `runserver`.

## Arquitectura y convención no obvia

- Todas las vistas de `tickets/views.py` llevan `@login_required`. Sin sesión, redirige a `login` (vía `django.contrib.auth.urls` bajo `cuentas/`).
- Templates viven en `tickets/templates/tickets/`. `lista.html` hace `{% extends "tickets/base.html" %}`, por lo que `base.html` **debe estar dentro de `tickets/templates/tickets/`** (no un nivel arriba). Si se mueve, `TemplateDoesNotExist`.
- Sintaxis de plantillas Django: dentro de `{% if %}` el operador `==` **necesita espacios alrededor** (`{% if x == "y" %}`). Sin espacios Django falla al parsear (`Could not parse the remainder`).
- Roles: grupos `Cliente` y `Agente`. Los superusuarios cuentan como agente. Los agentes ven **todos los tickets** ordenados por fecha de creación (más recientes primero). Los clientes ven solo sus propios tickets con filtro opcional por estado.
- `Ticket.prioridad()` evalúa la fórmula postfija `"impacto peso * dias +"` desde `tickets/estructuras/arbol_expresion.py` (`construir_postfija` / `evaluar_con_variables`). No tocar sin entender la notación postfija.
- Los usuarios de prueba (`cliente_prueba`, `agente_prueba`, `admin`) **no se crean con un comando `crear_usuarios`** (ese comando no existe en el repo). Círlos desde `/admin/` y agréguelos a los grupos `Cliente` o `Agente`.

## Qué NO asumir

- No hay `.env`, ni variables de entorno secretas, ni CI configurado. `DEBUG = True` y `SECRET_KEY` están hardcodeados en `config/settings.py` (solo desarrollo).
- No hay lint, formatter ni typecheck configurados en el repo.
- No hay tests de integración ni servicios externos requeridos (sqlite embebido, email por consola).
