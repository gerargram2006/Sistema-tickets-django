class CategoriaTicket:
    """Nodo de un árbol general (no binario) de categorías de tickets."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.subcategorias = []

    def agregar_subcategoria(self, subcategoria):
        self.subcategorias.append(subcategoria)


def recorrer_categorias(nodo, nivel=0):
    """Imprime el árbol completo con sangría según el nivel, recursivamente."""
    print("  " * nivel + "- " + nodo.nombre)
    for subcategoria in nodo.subcategorias:
        recorrer_categorias(subcategoria, nivel + 1)
