"""Expresión regular (infix) -> tokens -> postfix (Shunting Yard) -> AST.

Basado en el algoritmo de Shunting Yard implementado en LAB2-ToC/lab3-toc.
"""

from automata import EPSILON

PRECEDENCIA = {'|': 1, '_': 2, '*': 3}
CONCAT = '_'  # operador interno de concatenación (no se usa '.' porque puede aparecer como literal)


def tokenizar(regex):
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == '\\' and i + 1 < len(regex):
            tokens.append(regex[i + 1])  # caracter escapado -> símbolo literal de longitud 1
            i += 2
        elif c == '[':
            fin = regex.index(']', i)
            clase = regex[i + 1:fin]
            tokens.append('(')
            for j, ch in enumerate(clase):
                if j > 0:
                    tokens.append('|')
                tokens.append(ch)
            tokens.append(')')
            i = fin + 1
        else:
            tokens.append(c)
            i += 1
    return tokens


def es_operando(tok):
    return tok not in ('|', '(', ')', '*', '+', '?', CONCAT)


def extraer_ultima_expresion(tokens):
    if not tokens:
        raise ValueError("No hay una expresion valida antes de '+' o '?'")

    fin = len(tokens) - 1
    ultimo = tokens[fin]

    if ultimo == ')':
        parentesis = 0
        inicio = fin
        while inicio >= 0:
            tok = tokens[inicio]
            if tok == ')':
                parentesis += 1
            elif tok == '(':
                parentesis -= 1
                if parentesis == 0:
                    return inicio, tokens[inicio:fin + 1]
            inicio -= 1
        raise ValueError("Parentesis desbalanceados al expandir '+' o '?'")

    if ultimo in ('|', '(', CONCAT, '*', '+', '?'):
        raise ValueError("El operador '+' o '?' no tiene una expresion valida a la izquierda")

    return fin, [ultimo]


def expandir_extensiones(tokens):
    """E+ -> EE* ; E? -> (E|EPSILON)."""
    resultado = []
    for tok in tokens:
        if tok in ('+', '?'):
            inicio, expresion = extraer_ultima_expresion(resultado)
            if tok == '+':
                resultado = resultado[:inicio] + expresion + expresion + ['*']
            else:
                resultado = resultado[:inicio] + ['('] + expresion + ['|', EPSILON, ')']
        else:
            resultado.append(tok)
    return resultado


def insertar_concatenacion(tokens):
    resultado = []
    for i, tok in enumerate(tokens):
        resultado.append(tok)
        if i + 1 < len(tokens):
            siguiente = tokens[i + 1]
            fin_expresion = es_operando(tok) or tok in (')', '*')
            inicio_expresion = es_operando(siguiente) or siguiente == '('
            if fin_expresion and inicio_expresion:
                resultado.append(CONCAT)
    return resultado


def shunting_yard(tokens):
    salida, pila = [], []

    for tok in tokens:
        if es_operando(tok):
            salida.append(tok)
        elif tok == '(':
            pila.append(tok)
        elif tok == ')':
            while pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()
        else:
            while pila and pila[-1] != '(' and PRECEDENCIA[pila[-1]] >= PRECEDENCIA[tok]:
                salida.append(pila.pop())
            pila.append(tok)

    while pila:
        salida.append(pila.pop())

    return salida


def convertir(regex):
    """(postfix_tokens, postfix_str) para una expresión regular en infix."""
    tokens = insertar_concatenacion(expandir_extensiones(tokenizar(regex)))
    postfix_tokens = shunting_yard(tokens)
    return postfix_tokens, ''.join(postfix_tokens)


def alfabeto_de_regex(regex):
    """Símbolos (no operadores) distintos que aparecen en la expresión regular."""
    return {tok for tok in tokenizar(regex) if es_operando(tok)}


class Nodo:
    def __init__(self, simbolo, izq=None, der=None):
        self.simbolo = simbolo
        self.izq = izq
        self.der = der


def construir_arbol(postfix_tokens):
    """Apila operandos; cada operador desapila sus hijos y apila el nodo resultante."""
    pila = []
    for tok in postfix_tokens:
        if tok in ('|', '_'):
            der, izq = pila.pop(), pila.pop()
            pila.append(Nodo(tok, izq, der))
        elif tok == '*':
            pila.append(Nodo(tok, pila.pop()))
        else:
            pila.append(Nodo(tok))
    return pila[0]
