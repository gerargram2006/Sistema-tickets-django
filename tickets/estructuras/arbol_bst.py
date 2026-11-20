import random


class NodoBST:
    """Nodo de un árbol binario de búsqueda para indexar tickets por id."""

    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
        self.izq = None
        self.der = None


def insertar(raiz, codigo, nombre):
    """Inserta un par (codigo, nombre) en el BST y devuelve la raíz."""
    if raiz is None:
        return NodoBST(codigo, nombre)
    if codigo < raiz.codigo:
        raiz.izq = insertar(raiz.izq, codigo, nombre)
    elif codigo > raiz.codigo:
        raiz.der = insertar(raiz.der, codigo, nombre)
    else:
        raiz.nombre = nombre
    return raiz


def buscar_con_pasos(raiz, codigo):
    """Busca un código en el BST imprimiendo cada nodo visitado y devuelve los pasos."""
    pasos = 0
    actual = raiz
    while actual is not None:
        pasos += 1
        print(f"  revisa {actual.codigo}")
        if codigo == actual.codigo:
            return pasos
        elif codigo < actual.codigo:
            actual = actual.izq
        else:
            actual = actual.der
    return pasos


def altura(raiz):
    """Calcula la altura del árbol binario de búsqueda."""
    if raiz is None:
        return 0
    return 1 + max(altura(raiz.izq), altura(raiz.der))


def construir_indice(tickets, mezclar=True):
    """Construye un índice BST a partir de los tickets (id, titulo)."""
    parejas = [(t.id, t.titulo) for t in tickets]
    if mezclar:
        random.shuffle(parejas)
    raiz = None
    for codigo, nombre in parejas:
        raiz = insertar(raiz, codigo, nombre)
    return raiz
