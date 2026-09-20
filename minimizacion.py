"""Minimización de AFD usando el algoritmo table filling."""

from automata import Estado, Automata, obtener_estados


def _destino(estado, simbolo):
    for s, d in estado.transiciones:
        if s == simbolo:
            return d
    return None


def minimizar(afd, alfabeto):
    estados = list(obtener_estados(afd.inicio))

    # La tabla guarda solo la mitad superior: (estado menor, estado mayor).
    tabla = {}
    for i, estado_izquierdo in enumerate(estados):
        for j in range(i + 1, len(estados)):
            estado_derecho = estados[j]
            son_distinguibles = (
                afd.es_aceptacion(estado_izquierdo)
                != afd.es_aceptacion(estado_derecho)
            )
            tabla[(i, j)] = son_distinguibles

    def pareja(estado_1, estado_2):
        """Devuelve la clave ordenada de una pareja de estados."""
        indice_1 = estados.index(estado_1)
        indice_2 = estados.index(estado_2)
        return tuple(sorted((indice_1, indice_2)))

    cambio = True
    while cambio:
        cambio = False
        for (i, j), marcada in list(tabla.items()):
            if marcada:
                continue

            estado_izquierdo = estados[i]
            estado_derecho = estados[j]
            for simbolo in alfabeto:
                destino_izquierdo = _destino(estado_izquierdo, simbolo)
                destino_derecho = _destino(estado_derecho, simbolo)

                if destino_izquierdo is None or destino_derecho is None:
                    if destino_izquierdo != destino_derecho:
                        tabla[(i, j)] = True
                        cambio = True
                        break
                    continue

                if destino_izquierdo == destino_derecho:
                    continue

                if tabla[pareja(destino_izquierdo, destino_derecho)]:
                    tabla[(i, j)] = True
                    cambio = True
                    break

    grupos = []
    estados_visitados = set()
    for i, estado in enumerate(estados):
        if estado in estados_visitados:
            continue

        grupo = {estado}
        for j in range(i + 1, len(estados)):
            if not tabla[(i, j)]:
                grupo.add(estados[j])
        grupos.append(grupo)
        estados_visitados.update(grupo)

    grupo_de = {estado: i for i, grupo in enumerate(grupos) for estado in grupo}
    nuevos_estados = [Estado() for _ in grupos]
    aceptacion = set()
    for i, g in enumerate(grupos):
        representante = next(iter(g))
        if afd.es_aceptacion(representante):
            aceptacion.add(nuevos_estados[i])
        for simbolo, destino in representante.transiciones:
            nuevos_estados[i].agregar_transicion(simbolo, nuevos_estados[grupo_de[destino]])

    return Automata(nuevos_estados[grupo_de[afd.inicio]], aceptacion)
