"""Construcción de Thompson: AST -> AFN, de forma recursiva."""

from automata import Estado, Automata, EPSILON

OPERADORES = ('|', '_', '*')


def thompson(nodo):
    simbolo = nodo.simbolo

    if simbolo not in OPERADORES:
        inicio, fin = Estado(), Estado()
        inicio.agregar_transicion(simbolo, fin)  # simbolo == EPSILON para el caso 'E?'
        return Automata(inicio, fin)

    if simbolo == '_':
        izq, der = thompson(nodo.izq), thompson(nodo.der)
        izq.aceptacion_unica.agregar_transicion(EPSILON, der.inicio)
        return Automata(izq.inicio, der.aceptacion_unica)

    if simbolo == '|':
        izq, der = thompson(nodo.izq), thompson(nodo.der)
        inicio, fin = Estado(), Estado()
        inicio.agregar_transicion(EPSILON, izq.inicio)
        inicio.agregar_transicion(EPSILON, der.inicio)
        izq.aceptacion_unica.agregar_transicion(EPSILON, fin)
        der.aceptacion_unica.agregar_transicion(EPSILON, fin)
        return Automata(inicio, fin)

    # simbolo == '*'
    hijo = thompson(nodo.izq)
    inicio, fin = Estado(), Estado()
    inicio.agregar_transicion(EPSILON, hijo.inicio)
    inicio.agregar_transicion(EPSILON, fin)
    hijo.aceptacion_unica.agregar_transicion(EPSILON, hijo.inicio)
    hijo.aceptacion_unica.agregar_transicion(EPSILON, fin)
    return Automata(inicio, fin)
