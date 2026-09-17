"""Dibuja cualquier Automata (AFN o AFD) como grafo: estado inicial, estados
de aceptación (doble círculo) y transiciones etiquetadas."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from automata import obtener_estados, EPSILON

ETIQUETAS = {EPSILON: 'ε'}


def _niveles_bfs(inicio, estados):
    """Nivel = distancia BFS desde el inicio; ubica el grafo de izquierda a derecha."""
    nivel = {inicio: 0}
    orden = [inicio]
    cola = [inicio]
    while cola:
        actual = cola.pop(0)
        for _, destino in actual.transiciones:
            if destino not in nivel:
                nivel[destino] = nivel[actual] + 1
                orden.append(destino)
                cola.append(destino)
    for e in estados:
        if e not in nivel:
            nivel[e] = max(nivel.values(), default=0) + 1
            orden.append(e)
    return nivel, orden


def _posiciones(inicio, estados):
    nivel, orden = _niveles_bfs(inicio, estados)
    columnas = {}
    for e in orden:
        columnas.setdefault(nivel[e], []).append(e)

    posiciones = {}
    for x, columna in columnas.items():
        n = len(columna)
        for j, e in enumerate(columna):
            posiciones[e] = (x, (n - 1) / 2 - j)
    return posiciones, columnas


def dibujar_automata(automata, titulo, archivo):
    estados = obtener_estados(automata.inicio)

    grafo = nx.DiGraph()
    grafo.add_nodes_from(estados)

    etiquetas_arista = {}
    for e in estados:
        for simbolo, destino in e.transiciones:
            texto = ETIQUETAS.get(simbolo, simbolo)
            clave = (e, destino)
            if clave not in etiquetas_arista:
                etiquetas_arista[clave] = texto
                grafo.add_edge(e, destino)
            elif texto not in etiquetas_arista[clave].split(','):
                etiquetas_arista[clave] += f",{texto}"

    posiciones, columnas = _posiciones(automata.inicio, estados)

    ancho = max(8, len(columnas) * 2.2)
    alto = max(5, max(len(c) for c in columnas.values()) * 1.4)
    fig, ax = plt.subplots(figsize=(ancho, alto))

    aceptacion = [e for e in grafo.nodes if automata.es_aceptacion(e)]
    normales = [e for e in grafo.nodes if e not in aceptacion]

    nx.draw_networkx_nodes(grafo, posiciones, nodelist=normales, node_color="#a8d5ff",
                            node_size=1200, edgecolors="black", ax=ax)
    nx.draw_networkx_nodes(grafo, posiciones, nodelist=aceptacion, node_color="#a8ffb0",
                            node_size=1200, edgecolors="black", ax=ax)
    if aceptacion:
        nx.draw_networkx_nodes(grafo, posiciones, nodelist=aceptacion, node_color="none",
                                node_size=1550, edgecolors="black", ax=ax)

    nx.draw_networkx_labels(grafo, posiciones, labels={e: str(e) for e in grafo.nodes}, ax=ax)
    nx.draw_networkx_edges(grafo, posiciones, connectionstyle="arc3,rad=0.15",
                            arrowstyle="-|>", arrowsize=15, node_size=1200, ax=ax)
    nx.draw_networkx_edge_labels(grafo, posiciones, edge_labels=etiquetas_arista, ax=ax, font_size=9,
                                  connectionstyle="arc3,rad=0.15")

    x0, y0 = posiciones[automata.inicio]
    ax.annotate("inicio", xy=(x0 - 0.55, y0), xytext=(x0 - 1.4, y0),
                arrowprops=dict(arrowstyle="-|>"), fontsize=9, va="center")

    xs = [x for x, _ in posiciones.values()]
    ys = [y for _, y in posiciones.values()]
    ax.set_xlim(min(xs) - 1.6, max(xs) + 0.6)
    ax.set_ylim(min(ys) - 0.6, max(ys) + 0.6)

    ax.set_title(titulo)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
