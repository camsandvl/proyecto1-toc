# Proyecto No. 1 - Teoría de la Computación

## Integrantes

- Camila Sandoval #24358
- Alejandra Sierra #24405

## Descripción

Dada una expresión regular `r` y una cadena `w`, el programa:

1. Convierte `r` de notación infix a postfix (Shunting Yard).
2. Construye el AFN correspondiente (Algoritmo de Thompson).
3. Convierte el AFN a AFD (Construcción de Subconjuntos).
4. Minimiza el AFD.
5. Simula `w` sobre el AFN, el AFD y el AFD minimizado, indicando si `w ∈ L(r)`.
6. Genera una imagen por cada autómata (AFN, AFD, AFD minimizado).

El símbolo usado para representar épsilon (ε) es `#`, ya que no es una letra
ni un número y tiene muy baja probabilidad de aparecer como símbolo literal
en una expresión regular de prueba.

## Estructura del proyecto

- `regex_ast.py` — tokenización, expansión de `+`/`?`/clases `[...]`,
  inserción de concatenación explícita, Shunting Yard (infix -> postfix) y
  construcción del AST a partir del postfix.
- `automata.py` — representación común de un autómata (`Estado`, `Automata`)
  y las operaciones que comparten AFN y AFD: cerradura épsilon, movimiento y
  simulación. Un AFD es, para estos efectos, un AFN sin transiciones épsilon
  y determinista, por lo que **una sola función `simular` sirve para AFN,
  AFD y AFD minimizado**.
- `thompson.py` — construcción recursiva del AFN a partir del AST.
- `subconjuntos.py` — construcción de subconjuntos (AFN -> AFD).
- `minimizacion.py` — minimización del AFD por particiones (Moore).
- `graficador.py` — dibuja cualquier `Automata` (estado inicial, estados de
  aceptación con doble círculo, transiciones etiquetadas) usando
  `networkx`/`matplotlib`.
- `main.py` — punto de entrada: lee el archivo de expresiones, corre el
  pipeline completo por cada línea y pide la cadena `w` a evaluar.
- `expresiones.txt` — expresiones regulares de ejemplo (una por línea).

## Ejecución

```
pip install -r requirements.txt
python main.py [archivo_expresiones.txt]
```

Si no se indica un archivo, se usa `expresiones.txt` por defecto. Por cada
línea (expresión regular) el programa pedirá la cadena `w` a evaluar y
mostrará el postfix, el alfabeto, la ruta de las imágenes generadas y el
resultado ("si"/"no") de la simulación en el AFN, el AFD y el AFD
minimizado.

Las imágenes se guardan en `salida/expresion_<n>/{afn,afd,afd_min}.png`.
