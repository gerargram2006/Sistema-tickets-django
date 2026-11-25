from .grafo import Grafo


def red_de_areas(areas):
    """Construye un grafo dirigido con las áreas y sus derivaciones."""
    lista_areas = list(areas)
    nombres = [area.nombre for area in lista_areas]
    grafo = Grafo(nombres, dirigido=True)
    for area in lista_areas:
        for destino in area.deriva_a.all():
            if destino.nombre in grafo.indices:
                grafo.agregar_arista(area.nombre, destino.nombre)
    return grafo
