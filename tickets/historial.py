class NodoDoble:
    """Nodo de una lista doblemente enlazada."""
    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None


class HistorialComentarios:
    """Lista doblemente enlazada de comentarios, propia, sin librerías externas."""
    def __init__(self, comentarios):
        self._nodos = []
        nodo_previo = None
        for comentario in comentarios:
            nodo = NodoDoble(comentario)
            if nodo_previo:
                nodo_previo.siguiente = nodo
                nodo.anterior = nodo_previo
            self._nodos.append(nodo)
            nodo_previo = nodo
        self._actual = self._nodos[0] if self._nodos else None

    def actual(self):
        """Devuelve el comentario en la posición actual."""
        return self._actual.dato if self._actual else None

    def anterior(self):
        """Mueve la posición actual un nodo hacia atrás, si existe."""
        if self._actual and self._actual.anterior:
            self._actual = self._actual.anterior
        return self.actual()

    def siguiente(self):
        """Mueve la posición actual un nodo hacia adelante, si existe."""
        if self._actual and self._actual.siguiente:
            self._actual = self._actual.siguiente
        return self.actual()

    def hay_anterior(self):
        """Equivale a has_previous() del Paginator."""
        return bool(self._actual and self._actual.anterior)

    def hay_siguiente(self):
        """Equivale a has_next() del Paginator."""
        return bool(self._actual and self._actual.siguiente)

    def agregar_al_final(self, dato):
        """Agrega un comentario nuevo al final, sin perder la posición actual."""
        nuevo = NodoDoble(dato)
        if self._nodos:
            ultimo = self._nodos[-1]
            ultimo.siguiente = nuevo
            nuevo.anterior = ultimo
        else:
            self._actual = nuevo
        self._nodos.append(nuevo)