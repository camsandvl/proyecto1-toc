"""Punto de entrada: por cada expresion regular r del archivo de entrada,
construye su AFN (Thompson), su AFD (subconjuntos) y su AFD minimizado,
genera las graficas correspondientes y simula una cadena w en los tres.
"""

import os
import sys

from regex_ast import convertir, construir_arbol, alfabeto_de_regex
from automata import simular
from thompson import thompson
from subconjuntos import construir_afd
from minimizacion import minimizar
from graficador import dibujar_automata

CARPETA_SALIDA = "salida"


def procesar_regex(indice, regex):
    postfix_tokens, postfix_str = convertir(regex)
    ast = construir_arbol(postfix_tokens)
    afn = thompson(ast)

    alfabeto = alfabeto_de_regex(regex)
    afd = construir_afd(afn, alfabeto)
    afd_min = minimizar(afd, alfabeto)

    carpeta = os.path.join(CARPETA_SALIDA, f"expresion_{indice}")
    os.makedirs(carpeta, exist_ok=True)
    dibujar_automata(afn, f"AFN (Thompson): {regex}", os.path.join(carpeta, "afn.png"))
    dibujar_automata(afd, f"AFD (subconjuntos): {regex}", os.path.join(carpeta, "afd.png"))
    dibujar_automata(afd_min, f"AFD minimizado: {regex}", os.path.join(carpeta, "afd_min.png"))

    print(f"\nExpresion {indice}: {regex}")
    print(f"  Postfix: {postfix_str}")
    print(f"  Alfabeto: {sorted(alfabeto)}")
    print(f"  Graficas guardadas en: {carpeta}")

    cadena = input(f"  Ingrese la cadena w para evaluar contra '{regex}': ")

    for nombre, automata in (("AFN", afn), ("AFD", afd), ("AFD minimizado", afd_min)):
        pertenece = simular(automata, cadena)
        print(f"  {nombre}: {'si' if pertenece else 'no'}")


def main():
    archivo = sys.argv[1] if len(sys.argv) > 1 else "expresiones.txt"

    with open(archivo, "r", encoding="utf-8") as f:
        lineas = [linea.rstrip("\n") for linea in f if linea.strip()]

    for i, regex in enumerate(lineas, start=1):
        procesar_regex(i, regex)


if __name__ == "__main__":
    main()
