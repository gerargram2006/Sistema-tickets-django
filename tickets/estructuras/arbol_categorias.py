class NodoGenerico:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

def mostrar(nodo, nivel=0):
    print("  " * nivel + nodo.nombre)
    for hijo in nodo.hijos:
        mostrar(hijo, nivel + 1)

def construir_arbol(categorias):
    raiz = NodoGenerico("Categorías")
    
    # 1. Crear mapa id -> NodoGenerico
    nodos_dict = {c.id: NodoGenerico(c.nombre) for c in categorias}
    
    # 2. Conectar nodos hijos con sus padres
    for c in categorias:
        nodo_actual = nodos_dict[c.id]
        if c.padre_id is None:
            raiz.agregar_hijo(nodo_actual)
        else:
            padre_nodo = nodos_dict.get(c.padre_id)
            if padre_nodo:
                padre_nodo.agregar_hijo(nodo_actual)
                
    return raiz