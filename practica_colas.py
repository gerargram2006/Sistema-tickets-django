from tickets.estructura import Pila

class Ticket:
    """Representa un ticket del sistema con historial de estados."""
    def __init__(self, id_ticket, titulo, estado_inicial="Abierto"):
        self.id_ticket = id_ticket
        self.titulo = titulo
        self.estado_actual = estado_inicial
        self._historial_estados = Pila()

    def cambiar_estado(self, nuevo_estado):
        """Apila el estado anterior antes de asignar el nuevo estado."""
        self._historial_estados.push(self.estado_actual)
        self.estado_actual = nuevo_estado
    def __str__(self):
        """Representación legible del ticket al hacer print(ticket)."""
        return f"[{self.id_ticket}] {self.titulo} - Estado: {self.estado_actual}"


def deshacer_ultimo_cambio(ticket):
    """Usa pop() sobre la pila para devolver el ticket a su estado anterior."""
    estado_anterior = ticket._historial_estados.pop()
    if estado_anterior is None:
        print("No hay estados anteriores para deshacer.")
        return False

    ticket.estado_actual = estado_anterior
    return True


# =======================================================
# EJECUCIÓN Y PRUEBA CON DATOS DEL EQUIPO
# =======================================================
if __name__ == "__main__":
    # Ticket personalizado del equipo
    ticket_1 = Ticket("TCK-001", "Error en inicio de sesión de usuario")

    print("--- ESTADO INICIAL ---")
    print(ticket_1, "\n")

    print(f"--- REGISTRANDO 3 CAMBIOS DE ESTADO ---")
    ticket_1.cambiar_estado("En progreso")
    print(f"Cambio 1 -> {ticket_1}")
    ticket_1.cambiar_estado("En revisión")
    print(f"Cambio 2 -> {ticket_1}")
    ticket_1.cambiar_estado("Resuelto")
    print(f"Cambio 3 -> {ticket_1}\n")

    print(f"--- APLICANDO DESHACER (UNDO) ---")
    deshacer_ultimo_cambio(ticket_1)
    print(f"Resultado tras deshacer 1 cambio: {ticket_1.estado_actual}")
