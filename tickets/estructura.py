class Pila:
    """Clase Pila propia sin librerías externas (Política LIFO)."""
    def __init__(self):
        self._elementos = []

    def is_empty(self):
        return len(self._elementos) == 0

    def push(self, dato):
        self._elementos.append(dato)

    def pop(self):
        if self.is_empty():
            return None
        return self._elementos.pop()


class Cola:
    """Clase Cola propia sin librerías externas (Política FIFO)."""
    def __init__(self):
        self._elementos = []

    def is_empty(self):
        return len(self._elementos) == 0

    def enqueue(self, dato):
        self._elementos.append(dato)

    def dequeue(self):
        if self.is_empty():
            return None
        return self._elementos.pop(0)
