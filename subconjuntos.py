"""Construcción de subconjuntos: AFN -> AFD."""

from automata import Estado, Automata, cerradura_epsilon, mover


def construir_afd(afn, alfabeto):
    inicial = frozenset(cerradura_epsilon({afn.inicio}))
    estados_afd = {inicial: Estado()}
    aceptacion = set()
    if afn.aceptacion & inicial:
        aceptacion.add(estados_afd[inicial])

    pendientes = [inicial]
    while pendientes:
        actual = pendientes.pop()
        for simbolo in alfabeto:
            destino = frozenset(cerradura_epsilon(mover(actual, simbolo)))
            if not destino:
                continue  # sin transicion valida -> AFD parcial (no requiere estado trampa)

            if destino not in estados_afd:
                estados_afd[destino] = Estado()
                if afn.aceptacion & destino:
                    aceptacion.add(estados_afd[destino])
                pendientes.append(destino)

            estados_afd[actual].agregar_transicion(simbolo, estados_afd[destino])

    return Automata(estados_afd[inicial], aceptacion)
