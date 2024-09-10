import sys
import os

"""
    Codificador: Esquema de codificación para ejemplares de la forma:
        Ejemplar: Una gráfica G = (V, E)
    
    Toma un archivo .txt (archivo) en el cual estará representada una gráfica y la codifica para
    guardar los vértices y aristas en listas.

    Equipo:
        Luis Gerardo Estrada García (319013832)
        Cielo López Villalba (422050461)
        Dulce Julieta Mora Hernández (319236448)
        Marcos Julián Noriega Rodríguez (319284061)

"""

def codificar(archivo):
    """Lee el archivo que se pasó como argumento y guarda los vértices y aristas en ua lista"""

    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        return

    vertices = []
    aristas = []

    # Leemos el archivo de entrada.
    try:
        with open(archivo, 'r') as archivo_entrada:
            for linea in archivo_entrada:
                arista = linea.strip().split(" ")
                if len(arista) != 2:
                    print(f"Formato inválido para aristas en: {linea.strip()}")
                    print(f"Una arista es la unión de dos vértices.")
                    return

                # Separamos la arista en dos valores
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

    print("Lista de aristas: [", ', '.join(aristas), "]")
    print(f"Número de vértices: {len(vertices)}")
    print(f"Lista de vértices: {vertices}")

# Verifica si se pasa un archivo como argumento
if len(sys.argv) != 2:
    print("Para ejecutar: python codificador.py <archivo>")
else:
    codificar(sys.argv[1])
