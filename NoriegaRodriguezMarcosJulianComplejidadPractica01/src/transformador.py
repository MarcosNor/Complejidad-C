import sys
import os

"""
    transformador: transforma el esquema de codificación propuesto a uno que utilice
    codificación de gráficas como matrices.

    Equipo:
        Luis Gerardo Estrada García (319013832)
        Cielo López Villalba (422050461)
        Dulce Julieta Mora Hernández (319236448)
        Marcos Julián Noriega Rodríguez (319284061)

"""

def es_formato_valido(linea):
    """ Verifica que se pasen 2 elementos separados por un espacio.
    Args:
        linea: Línea en el archivo del ejemplar que contiene los vertices
    """
    elementos = linea.strip().split(" ")
    return len(elementos) == 2

def transformar_archivo(archivo_entrada, archivo_salida):
    """
        Función para transformar el esquema de codificación propuesto
        a uno que utilice codificación de gráficas como matrices.

        Args:
            archivo_entrada: Archivo del que leeremos la gráfica codificada en aristas
            archivo_salida: Nombre que querramos para regresar la matriz
    """

    if not os.path.exists(archivo_entrada):
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        return

    vertices = []
    aristas = []
    matriz_adyacencia = []

    # Leemos el archivo de entrada.
    try:
        with open(archivo_entrada, 'r') as archivo:
            for linea in archivo:
                arista = linea.strip().split(" ")
                if len(arista) != 2:
                    print(f"Formato inválido para aristas en: {linea.strip()}")
                    print(f"Una arista es la unión de dos vértices.")
                    return
                
                v1, v2 = arista[0], arista[1]

                # Omitimos lazos
                if v1 == v2:
                    continue

                # Agregamos los vértices a la lista
                if v1 not in vertices:
                    vertices.append(v1)
                if v2 not in vertices:
                    vertices.append(v2)

                # aristas de la forma 'a b' son igual que 'b a'
                if v1 > v2:
                    v1, v2 = v2, v1

                if f"{v1} {v2}" not in aristas:
                    aristas.append(f"{v1} {v2}")

    except IOError as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Crear una matriz de adyacencia de tamaño n x n
    cantidad_vertices = len(vertices)
    matriz_adyacencia = [[0] * cantidad_vertices for _ in range(cantidad_vertices)]

    # Volvemos a leer el archivo
    try:
        with open(archivo_entrada, 'r') as archivo:
            for linea in archivo:
                arista = linea.strip().split(" ")
                if len(arista) != 2:
                    print(f"Formato inválido para aristas en: {linea.strip()}")
                    print(f"Una arista es la unión de dos vértices.")
                    return

                v1, v2 = arista[0], arista[1]

                indice1 = vertices.index(v1)
                indice2 = vertices.index(v2)

                matriz_adyacencia[indice1][indice2] = 1
                matriz_adyacencia[indice2][indice1] = 1
    except IOError as e:
        print(f"Error al leer el archivo: {e}")
        return


    # Imprimimos los resultados
    print(f"Lista de vértices: {vertices}")
    print(f"Número de vértices: {len(vertices)}")
    print("Lista de aristas: [", ', '.join(aristas), "]")

    # Mostramos la matriz en consola y lo escribimos en el archivo de salida
    print("Matriz de adyacencia:")
    for fila in matriz_adyacencia:
        print(" ".join(map(str, fila)))

    try:
        with open(archivo_salida, 'w') as archivo:
            for fila in matriz_adyacencia:
                archivo.write("".join(map(str, fila)))
        print(f"Matriz guardada correctamente en el archivo: {archivo_salida}")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")


if len(sys.argv) != 3:
    print("Uso: python transformador.py <archivo_entrada> <archivo_salida>")
else:
    archivo_entrada = sys.argv[1]
    archivo_salida = sys.argv[2]

    transformar_archivo(archivo_entrada, archivo_salida)
