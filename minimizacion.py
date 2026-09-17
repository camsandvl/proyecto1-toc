"""Minimización de AFD por particiones (Moore / table filling)."""

from automata import Estado, Automata, obtener_estados


def _destino(estado, simbolo):
    for s, d in estado.transiciones:
        if s == simbolo:
            return d
    return None


def minimizar(afd, alfabeto):
    estados = list(obtener_estados(afd.inicio))

    grupos = [g for g in (
        {e for e in estados if not afd.es_aceptacion(e)},
        {e for e in estados if afd.es_aceptacion(e)},
    ) if g]
    grupo_de = {e: i for i, g in enumerate(grupos) for e in g}

    cambio = True
    while cambio:
        nuevos_grupos = []
        for g in grupos:
            firmas = {}
            for e in g:
                firma = tuple(grupo_de.get(_destino(e, simbolo), -1) for simbolo in alfabeto)
                firmas.setdefault(firma, set()).add(e)
            nuevos_grupos.extend(firmas.values())

        cambio = len(nuevos_grupos) != len(grupos)
        grupos = nuevos_grupos
        grupo_de = {e: i for i, g in enumerate(grupos) for e in g}

    nuevos_estados = [Estado() for _ in grupos]
    aceptacion = set()
    for i, g in enumerate(grupos):
        representante = next(iter(g))
        if afd.es_aceptacion(representante):
            aceptacion.add(nuevos_estados[i])
        for simbolo, destino in representante.transiciones:
            nuevos_estados[i].agregar_transicion(simbolo, nuevos_estados[grupo_de[destino]])

    return Automata(nuevos_estados[grupo_de[afd.inicio]], aceptacion)
