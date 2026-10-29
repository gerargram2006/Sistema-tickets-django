class NodoExpresion:
    """Nodo de un árbol binario de expresión."""

    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

    def evaluar(self):
        if self.izquierdo is None and self.derecho is None:
            return int(self.valor)

        izquierda = self.izquierdo.evaluar()
        derecha = self.derecho.evaluar()
        if self.valor == "*":
            return izquierda * derecha
        if self.valor == "+":
            return izquierda + derecha
        raise ValueError(f"Operador desconocido: {self.valor}")


def construir_arbol_postfijo(tokens):
    pila = []
    operadores = {"+", "*"}

    for token in tokens:
        token = str(token)
        if token in operadores:
            if len(pila) < 2:
                raise ValueError("La expresión postfija está incompleta")
            derecho = pila.pop()
            izquierdo = pila.pop()
            pila.append(NodoExpresion(token, izquierdo, derecho))
        else:
            pila.append(NodoExpresion(token))

    if len(pila) != 1:
        raise ValueError("La expresión postfija contiene elementos de más")
    return pila.pop()


def calcular_prioridad(impacto, peso_categoria, dias_abierto):
    """Calcula impacto × peso + días usando postfijo y un árbol de expresión."""
    tokens = [impacto, peso_categoria, "*", dias_abierto, "+"]
    raiz = construir_arbol_postfijo(tokens)
    return raiz.evaluar(), " ".join(str(token) for token in tokens)
