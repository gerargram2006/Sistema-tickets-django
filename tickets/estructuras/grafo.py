class Grafo:
    """Grafo representado mediante matriz de adyacencia."""

    def __init__(self, nombres, dirigido=True):
        self.nombres = list(nombres)
        self.dirigido = dirigido
        self.indices = {nombre: i for i, nombre in enumerate(self.nombres)}
        n = len(self.nombres)
        self.matriz = [[0] * n for _ in range(n)]

    def agregar_arista(self, origen, destino):
        i = self.indices[origen]
        j = self.indices[destino]
        self.matriz[i][j] = 1
        if not self.dirigido:
            self.matriz[j][i] = 1

    def mostrar(self):
        encabezado = " ".join(f"{n[:3]:>3}" for n in self.nombres)
        print(f"    {encabezado}")
        for i, nombre in enumerate(self.nombres):
            fila = " ".join(f"{v:>3}" for v in self.matriz[i])
            print(f"{nombre[:3]:<3} {fila}")

    def vecinos(self, nombre):
        i = self.indices[nombre]
        return [self.nombres[j] for j, val in enumerate(self.matriz[i]) if val == 1]

    def grado(self, nombre):
        i = self.indices[nombre]
        return sum(self.matriz[i])

    def grado_entrada(self, nombre):
        i = self.indices[nombre]
        return sum(self.matriz[fila][i] for fila in range(len(self.nombres)))
