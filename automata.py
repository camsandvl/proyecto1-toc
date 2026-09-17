"""Representación común de autómatas finitos (AFN y AFD) y las operaciones
que ambos comparten: cerradura épsilon, movimiento y simulación."""

EPSILON = '#'  # símbolo que representa a epsilon en todo el proyecto


class Estado:
    contador = 0

    def __init__(self):
        self.id = Estado.contador
        Estado.contador += 1
        self.transiciones = []  # lista de (simbolo, estado_destino)

    def agregar_transicion(self, simbolo, destino):
        self.transiciones.append((simbolo, destino))

    def __repr__(self):
        return f"q{self.id}"


class Automata:
    """Sirve tanto para un AFN (un solo estado de aceptación) como para un
    AFD (uno o más estados de aceptación); ambos comparten Estado y las
    funciones de cerradura/movimiento/simulación de este módulo."""

    def __init__(self, inicio, aceptacion):
        self.inicio = inicio
        self.aceptacion = aceptacion if isinstance(aceptacion, (set, frozenset)) else {aceptacion}

    @property
    def aceptacion_unica(self):
        return next(iter(self.aceptacion))

    def es_aceptacion(self, estado):
        return estado in self.aceptacion


def obtener_estados(inicio):
    """Todos los estados alcanzables desde 'inicio'."""
    visitados = set()
    pila = [inicio]
    while pila:
        estado = pila.pop()
        if estado in visitados:
            continue
        visitados.add(estado)
        for _, destino in estado.transiciones:
            if destino not in visitados:
                pila.append(destino)
    return visitados


def cerradura_epsilon(estados):
    """Estados alcanzables usando cero o más transiciones epsilon. Para un
    AFD (sin transiciones epsilon) esto no hace nada, por lo que la misma
    función sirve para AFN y AFD."""
    cerradura = set(estados)
    pila = list(estados)
    while pila:
        estado = pila.pop()
        for simbolo, destino in estado.transiciones:
            if simbolo == EPSILON and destino not in cerradura:
                cerradura.add(destino)
                pila.append(destino)
    return cerradura


def mover(estados, simbolo):
    """Estados alcanzables consumiendo exactamente 'simbolo'."""
    siguientes = set()
    for estado in estados:
        for etiqueta, destino in estado.transiciones:
            if etiqueta == simbolo:
                siguientes.add(destino)
    return siguientes


def simular(automata, cadena):
    """Simula cualquier Automata (AFN o AFD) con la cadena dada.

    Al no tener transiciones epsilon un AFD, cerradura_epsilon es un no-op
    sobre sus estados, así que el mismo recorrido sirve para ambos casos.
    """
    actuales = cerradura_epsilon({automata.inicio})
    for simbolo in cadena:
        actuales = cerradura_epsilon(mover(actuales, simbolo))
        if not actuales:
            return False
    return any(automata.es_aceptacion(e) for e in actuales)
