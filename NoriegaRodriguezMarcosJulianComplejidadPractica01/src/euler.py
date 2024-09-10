import sys
import os

"""
    euler: Realiza los ejercicios anteriores (codifica y transforma la gráfica),
    y con la matriz de adyacencias verifica que la gráfica tenga una ruta euleriana.

    Equipo:
        Luis Gerardo Estrada García (319013832)
        Cielo López Villalba (422050461)
        Dulce Julieta Mora Hernández (319236448)
        Marcos Julián Noriega Rodríguez (319284061)

"""

def transformar_archivo(archivo_entrada):
    """
        Función para transformar el esquema de codificación propuesto
        a uno que utilice codificación de gráficas como matrices.

        Args:
            archivo_entrada: Archivo del que leeremos la gráfica codificada en aristas
    """
    if not os.path.exists(archivo_entrada):
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        return

    vertices = []
    aristas = []
    matriz_adyacencia = []

    try:
        with open(archivo_entrada, 'r') as archivo:
            for linea in archivo:
                arista = linea.strip().split(" ")
                if len(arista) != 2:
                    print(f"Formato inválido para aristas en: {linea.strip()}")
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
                    return

                v1, v2 = arista[0], arista[1]

                indice1 = vertices.index(v1)
                indice2 = vertices.index(v2)

                matriz_adyacencia[indice1][indice2] = 1
                matriz_adyacencia[indice2][indice1] = 1

    except IOError as e:
        print(f"Error al leer el archivo: {e}")
        return

    return vertices, aristas, matriz_adyacencia

# Calcular el grado de cada vértice.
def grado_vertices(matriz_adyacencia):
    """
        Calcula el grado de cada vértice en la gráfica.

        Args:
            matriz_adyacencia: Matriz de adyacencia de la gráfica transformada

        Returns:
            list: Lista con los grados de cada vértice.
    """
    return [sum(fila) for fila in matriz_adyacencia]

# Verificar si la gráfica tiene un ruta Euleriana.
def ruta_euleriana(vertices, matriz_adyacencia):
    """
        Determina si la gráfica tiene una ruta Euleriana o un ciclo Euleriano, dependiendo
        del número de vértices que tienen grado impar, si hay más de dos vértices
        con grado impar, automáticamente la rechaza.

        Args:
            vertices: Lista de vértices de la gráfica.
            matriz_adyacencia: Matriz de adyacencia de la gráfica.

        Returns:
            Indica si tiene una ruta Euleriana o ciclo
    """
    grados = grado_vertices(matriz_adyacencia)
    impares = [i for i, grado in enumerate(grados) if grado % 2 != 0]

    if len(impares) == 0:
        return "SI, tiene una ruta Euleriana", None #si esto sucede, es ademásun ciclo Euleriano.
    elif ((len(impares) == 2) or (len(impares) == 1)):
        return "SI, tiene una ruta Euleriana", impares
    else:
        return "NO, no tiene una ruta Euleriana", None

def vertices_mayor_grado(vertices, matriz_adyacencia):
    """
        Encuentra los vértices con el mayor grado en la gráfica.

        Args:
            vertices: Lista de vértices.
            matriz_adyacencia: Matriz de adyacencia de la gráfica.

        Retorna:
            Vértices de mayor grado y su grado.
    """
    grados = grado_vertices(matriz_adyacencia)
    max_grado = max(grados)
    vertices_mayores_grado = [vertices[i] for i, grado in enumerate(grados) if grado == max_grado]
    return vertices_mayores_grado, max_grado

# Algoritmo para encontrar una ruta Euleriana.
def encontrar_ruta_euleriana(vertices, matriz_adyacencia, inicio):
    """
    Algoritmo para encontrar la ruta euleriana de forma recursiva, en la cual partimos del
    primer vértice de la matriz, encontramos alguna adyacencia con otro vertice, borramos
    la primer arista y seguimos recursivamente sobre cada vertice
    Si hay vértices con grado impar intentará iniciar por estos vértices.

    Args:
        vertices: Lista de vértices.
        matriz_adyacencia: Matriz de adyacencia de la gráfica.
        inicio: vértice de donde empezamos la ruta
    """
    matriz_aux = [fila[:] for fila in matriz_adyacencia]
    ruta = []

    def recorrer(v):
        for u in range(len(vertices)):
            if matriz_aux[v][u] > 0:
                matriz_aux[v][u] -= 1
                matriz_aux[u][v] -= 1
                recorrer(u)
        ruta.append(v)

    recorrer(inicio)
    ruta = [vertices[v] for v in ruta]
    return ruta[::-1]

def informacion_grafica(archivo_entrada):
    """
        Función principal para mostrar la información de la gráfica.
        Args:
            Archivo con la gráfica decodificada
    """
    vertices, aristas, matriz_adyacencia = transformar_archivo(archivo_entrada)

    if vertices and aristas and matriz_adyacencia:
        print(f"Número de Vértices: {len(vertices)}")
        print(f"Número de Aristas: {len(aristas)}")

        vertice_mayor, grado_mayor = vertices_mayor_grado(vertices, matriz_adyacencia)
        print(f"Vértice(s) de mayor grado: {vertice_mayor} (grado {grado_mayor})")

        resultado_euleriano, impares = ruta_euleriana(vertices, matriz_adyacencia)
        print(f"¿La gráfica tiene una ruta euleriana? {resultado_euleriano}")

        if resultado_euleriano.startswith("SI"):
            inicio = impares[0] if impares else 0
            ruta = encontrar_ruta_euleriana(vertices, matriz_adyacencia, inicio)
            print(f"Ruta Euleriana: {' -> '.join(ruta)}")

if len(sys.argv) != 2:
    print("Uso: python euler.py <archivo_entrada> ")
else:
    archivo_entrada = sys.argv[1]
    informacion_grafica(archivo_entrada)

