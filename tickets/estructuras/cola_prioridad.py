class MinHeap:
    def __init__(self):
        self.datos = []

    def __len__(self):
        return len(self.datos)

    def esta_vacio(self):
        return len(self.datos) == 0

    def insertar(self, valor):
        self.datos.append(valor)
        self._flotar(len(self.datos) - 1)

    def obtener_minimo(self):
        return self.datos[0] if self.datos else None

    def extraer_minimo(self):
        if not self.datos:
            return None
        minimo = self.datos[0]
        ultimo = self.datos.pop()
        if self.datos:
            self.datos[0] = ultimo
            self._hundir(0)
        return minimo

    def _flotar(self, i):
        while i > 0:
            padre = (i - 1) // 2
            if self.datos[i] < self.datos[padre]:
                self.datos[i], self.datos[padre] = self.datos[padre], self.datos[i]
                i = padre
            else:
                break

    def _hundir(self, i):
        n = len(self.datos)
        while True:
            menor = i
            izq, der = 2 * i + 1, 2 * i + 2
            if izq < n and self.datos[izq] < self.datos[menor]:
                menor = izq
            if der < n and self.datos[der] < self.datos[menor]:
                menor = der
            if menor == i:
                break
            self.datos[i], self.datos[menor] = self.datos[menor], self.datos[i]
            i = menor


def cola_urgentes(tickets):
    """Crea un MinHeap con (-prioridad, id, titulo) por cada ticket."""
    cola = MinHeap()
    for t in tickets:
        cola.insertar((-t.prioridad(), t.id, t.titulo))
    return cola


def primeros(cola, k):
    """Saca hasta k tickets de la cola, del más urgente al menos urgente."""
    resultado = []
    while len(resultado) < k and not cola.esta_vacio():
        clave, ticket_id, titulo = cola.extraer_minimo()
        resultado.append({"id": ticket_id, "titulo": titulo, "prioridad": -clave})
    return resultado