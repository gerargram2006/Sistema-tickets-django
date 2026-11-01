# Sistema de Gestión de Tickets de Soporte

Proyecto del portafolio de Estructuras de Datos y Algoritmos (Tecsup), desarrollado con Django.

## Integrantes

- Hugo Flores Merma
- Gerar Camma
- Samuel Llallacachi Salhua

## Cómo ejecutar

```bash
python -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python manage.py makemigrations
venv/bin/python manage.py migrate
venv/bin/python manage.py runserver
```

En Windows, activa el entorno y usa `venv\Scripts\python.exe` en lugar de `venv/bin/python`.

Abre http://127.0.0.1:8000/ para iniciar sesión. Panel administrativo: http://127.0.0.1:8000/admin/.

## Usuarios y roles de prueba

Crea los usuarios desde `/admin/` y agrégalos a los grupos `Cliente` o `Agente`. Se recomienda al menos un usuario por grupo. También asigna `peso=3` a la categoría crítica `Hardware`.

## Preguntas Semana 10

### a) ¿Qué son hojas y qué son nodos internos en la expresión de permisos?

Hojas: `Q(estado="abierto")`, `Q(impacto__gte=4)` y `Q(categoria__peso__gte=3)`. Nodos internos: `AND` (raíz) y `OR` (hijo derecho de la raíz).

### b) ¿Por qué la postfija facilita el cálculo y evita depender de precedencia o paréntesis?

La postfija no necesita paréntesis ni precedencia, el árbol se construye con una sola pasada usando una pila, y la fórmula es texto fácil de cambiar sin tocar el código.

## Cómo ejecutar el proyecto

1. Crear el entorno virtual:
   python -m venv venv

2. Activarlo:
   - Linux / Mac: source venv/bin/activate
   - Windows: venv\Scripts\activate

3. Instalar Django:
   pip install django

4. Crear la base de datos:
   python manage.py migrate

5. Crear los usuarios de prueba:
   python manage.py crear_usuarios

6. Iniciar el servidor:
   python manage.py runserver

7. Abrir en el navegador: http://127.0.0.1:8000/

## Usuarios de prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| Cliente | cliente_prueba | Cliente123! |
| Agente | agente_prueba | Agente123! |
| Administrador | admin | Admin123! |