import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Los imports de la app van después de django.setup()
from tickets.cola import crear_ticket, asignar_siguiente_ticket, deshacer_ultimo_cambio
from tickets.models import Usuario


if __name__ == "__main__":
    datos = [
        ("Error en inicio de sesión de usuario",
         "El usuario ingresa credenciales correctas y el sistema muestra contraseña incorrecta"),
        ("No se pueden adjuntar archivos al ticket",
         "El botón Adjuntar no responde y el ticket se guarda sin el archivo"),
        ("Correo de confirmación no llega",
         "Tras registrarse, el usuario no recibe el correo de verificación"),
        ("Lentitud en el panel de tickets",
         "La lista tarda más de 10 segundos en cargar con muchos registros"),
    ]

    print("--- CREANDO 4 TICKETS (ENQUEUE) ---")
    for titulo, descripcion in datos:
        ticket = crear_ticket(titulo, descripcion)
        print(f"Encolado -> {ticket}")

    print("\n--- CREANDO 4 AGENTES ---")
    agentes = []
    for nombre in ["Ana", "Luis", "Carlos", "Marta"]:
        agente, _ = Usuario.objects.get_or_create(
            email=f"{nombre.lower()}@soporte.com", defaults={"nombre": nombre}
        )
        agentes.append(agente)
        print(f"Agente -> {agente}")

    print("\n--- ASIGNANDO EN ORDEN (DEQUEUE) ---")
    asignados = []
    for i, agente in enumerate(agentes):
        ticket = asignar_siguiente_ticket(agente)
        asignados.append(ticket)
        print(f"Asignación {i + 1} -> {ticket} | agente: {ticket.agente_asignado}")

    print("\n--- COLA VACÍA ---")
    print(f"Siguiente asignación -> {asignar_siguiente_ticket(agentes[0])}")

    print("\n--- APLICANDO DESHACER (UNDO) ---")
    deshacer_ultimo_cambio(asignados[0])
    print(f"Resultado tras deshacer: {asignados[0]}")
