class MaxHeap:
    """Max-heap propio: el mayor valor siempre queda en la raíz."""
    def __init__(self):
        self.datos = []

    def esta_vacio(self):
        return len(self.datos) == 0

    def construir(self, lista):
        """Arma el heap desde una lista, hundiendo desde el último padre."""
        self.datos = list(lista)
        for i in range(len(self.datos) // 2 - 1, -1, -1):
            self._hundir(i)

    def extraer_maximo(self):
        if not self.datos:
            return None
        maximo = self.datos[0]
        ultimo = self.datos.pop()
        if self.datos:
            self.datos[0] = ultimo
            self._hundir(0)
        return maximo

    def _hundir(self, i):
        n = len(self.datos)
        while True:
            mayor = i
            izq, der = 2 * i + 1, 2 * i + 2
            if izq < n and self.datos[izq] > self.datos[mayor]:
                mayor = izq
            if der < n and self.datos[der] > self.datos[mayor]:
                mayor = der
            if mayor == i:
                break
            self.datos[i], self.datos[mayor] = self.datos[mayor], self.datos[i]
            i = mayor


def heap_sort(lista):
    """Ordena de mayor a menor extrayendo repetidamente el máximo del heap."""
    heap = MaxHeap()
    heap.construir(lista)
    resultado = []
    while not heap.esta_vacio():
        resultado.append(heap.extraer_maximo())
    return resultado


def ranking_agentes(agentes):
    """Ranking de agentes por tickets resueltos, ordenado con heap_sort."""
    datos = [(a.tickets_resueltos.count(), a.username) for a in agentes]
    ordenados = heap_sort(datos)

    ranking = []
    puesto = 1
    for resueltos, nombre in ordenados:
        ranking.append({"puesto": puesto, "agente": nombre, "resueltos": resueltos})
        puesto += 1
    return ranking