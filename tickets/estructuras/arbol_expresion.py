# tickets/estructuras/arbol_expresion.py

# 1. NODO: una pieza del árbol
class NodoExpresion:
    def __init__(self, valor):
        self.valor = valor        # número, variable u operador
        self.izquierdo = None     # hijo izquierdo
        self.derecho = None       # hijo derecho


# 2. CONSTRUIR: convierte el texto postfijo en un árbol
def construir_postfija(texto):
    pila = []
    for token in texto.split():
        nodo = NodoExpresion(token)
        if token in ("+", "-", "*", "/"):
            nodo.derecho = pila.pop()     # el último que entró es el derecho
            nodo.izquierdo = pila.pop()   # el anterior es el izquierdo
        pila.append(nodo)
    return pila.pop()


# 3. EVALUAR: recorre el árbol y calcula el resultado
def evaluar_con_variables(nodo, valores):
    # Caso base: es una hoja (no tiene hijos)
    if nodo.izquierdo is None and nodo.derecho is None:
        if nodo.valor.isdigit():
            return int(nodo.valor)       # número: "2" -> 2
        return valores[nodo.valor]       # variable: "impacto" -> su valor

    # Paso recursivo: evaluar izquierda y derecha
    izq = evaluar_con_variables(nodo.izquierdo, valores)
    der = evaluar_con_variables(nodo.derecho, valores)

    # Aplicar el operador
    if nodo.valor == "+":
        return izq + der
    if nodo.valor == "-":
        return izq - der
    if nodo.valor == "*":
        return izq * der
    if nodo.valor == "/":
        return izq / der