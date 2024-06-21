from simpleai.search import (CspProblem,
                             backtrack,
                             min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             HIGHEST_DEGREE_VARIABLE,
                             LEAST_CONSTRAINING_VALUE)
from itertools import combinations, permutations, product

FRASCOS = ()
DOMINIOS = {}
SEGMENTOS = []


def cantidad_color(variables, values):
    # Debe haber 4 porciones de color entre todos los frascos
    dictionary = {}

    for color in values:
        if color in dictionary:
            dictionary[color] += 1
        else:
            dictionary[color] = 1

    for key, value in dictionary.items():
        if value != 4:
            return False

    return True


def color_al_fondo(variables, values):
    # Ningun color puede comenzar con todos sus segmentos en el fondo
    dictionary = {}
    for indice in range(len(set(values))):
        for n, segmento in enumerate(variables):
            if segmento == (indice, 0):
                if values[n] in dictionary:
                    dictionary[values[n]] += 1
                else:
                    dictionary[values[n]] = 1
            else:
                continue

    for key, value in dictionary.items():
        if value == 4:
            return False
    return True


def frascos_ady(variables, values):
    # Si dos frascos son adyacentes, deben compartir al menos un color
    colores1, colores2 = convertir_a_frasco(values)
    return any(color in colores1 for color in colores2)


def frascos_ady_colores_dif(variables, values):
    # No puede haber mas de 6 colores diferentes entre frascos adyacentes
    colores1, colores2 = convertir_a_frasco(values)
    return len(set(list(colores1)+list(colores2))) <= 6


def frascos_iguales(variables, values):
    # No puede haber dos frascos exactamente iguales
    val1, val2 = convertir_a_frasco(values)
    return val1 != val2


def frasco_resuelto(variables, values):
    return len(set(values)) != 1


def generar_restricciones(SEGMENTOS):
    # Generamos la lista de restricciones para el problema
    restricciones = []

    restricciones.append((SEGMENTOS, color_al_fondo))
    restricciones.append((SEGMENTOS, cantidad_color))

    frascos = convertir_a_frasco(SEGMENTOS)
    for frasco in frascos:
        restricciones.append(((tuple(frasco)), frasco_resuelto))

    for x in range(len(frascos) - 1):
        combinacion = tuple(list(frascos[x]) + list(frascos[x+1]))
        restricciones.append((combinacion, frascos_ady))
        restricciones.append((combinacion, frascos_ady_colores_dif))

    for variable1, variable2 in combinations(frascos, 2):
        combinacion = tuple(list(variable1) + list(variable2))
        restricciones.append((combinacion, frascos_iguales))

    return restricciones


def generar_segmentos(colores):
    SEGMENTOS = []
    for frasco in range(len(colores)):
        for segmento in range(4):
            SEGMENTOS.append((frasco, segmento))

    return SEGMENTOS


def convertir_a_frasco(segmentos):
    lista_frascos = []
    for x in range(0, len(segmentos), 4):
        lista_frascos.append((segmentos[x], segmentos[x+1], segmentos[x+2], segmentos[x+3]))

    return lista_frascos


def generar_dominios(segmentos, colores, contenido_parcial):
    # El dominio de los segmentos son todos los colores
    for seg in segmentos:
        DOMINIOS[seg] = colores

    # El contenido parcial sobreescribe el dominio
    for n, contenido in enumerate(contenido_parcial):
        nroSeg = 0
        for color in contenido:
            DOMINIOS[(n, nroSeg)] = tuple([color])
            nroSeg += 1

    return DOMINIOS


def armar_nivel(colores, contenidos_parciales):
    SEGMENTOS = generar_segmentos(colores)
    DOMINIOS = generar_dominios(SEGMENTOS, colores, list(contenidos_parciales))

    restricciones = generar_restricciones(SEGMENTOS)

    problem = CspProblem(SEGMENTOS, DOMINIOS, restricciones)
    solution = tuple(min_conflicts(problem).values())

    return tuple(convertir_a_frasco(solution))


if __name__ == "__main__":
    colores = ("rojo", "verde", "azul", "celeste")
    contenidos_parciales = (('rojo','rojo'),)

    solucion = armar_nivel(colores, contenidos_parciales)
    print("solucion:")
    print(solucion)

    colores = ("rojo", "verde", "azul", "celeste")
    contenidos_parciales = (('rojo','rojo'),)

    solucion = armar_nivel(colores, contenidos_parciales)
    print("solucion:")
    print(solucion)
