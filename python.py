from matricesRalas import MatrizRala, GaussJordan
import numpy as np
import pandas as pd
from matricesRalas import *
import csv


papers = pd.read_csv("papers/kaosnum.csv", header=0)
citas = pd.read_csv("papers/K4os.csv", header=0)


def leer_citas():
    archivo_citas = "papers/K4os.csv"
    citas = []
    with open(archivo_citas, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)  # Skip the header row
        for cita, citado in lector:
            citas.append((int(cita), int(citado)))
    return citas


def leer_papers():
    archivo_papers = "papers/kaosnum.csv"
    # Lista para almacenar los datos de los papers

    papers = []

    # Abrir el archivo CSV para leer los datos

    with open(archivo_papers, mode="r", encoding="utf-8") as f:
        # Crear un objeto reader de CSV

        lector = csv.DictReader(f)

        # Recorrer las filas del archivo CSV

        for fila in lector:
            # Añadir cada fila como un diccionario a la lista

            papers.append(
                [fila["id"], fila["titulo"], fila["autores"], fila["anio"]]
            )
    return papers

def genW(lista_citas, lista_papers):
    W = MatrizRala(len(lista_papers), len(lista_papers))
    for citador, citado in lista_citas:
        W[citador, citado] = 1
    return W


def genD(W):
    D = MatrizRala(W.shape[0], W.shape[1])
    for i in W.filas:
        cj = 0
        current_node = W.filas[i].raiz
        while current_node:
            cj += current_node.valor[1]  # Assume valor is a tuple (column_index, value)
            current_node = current_node.siguiente
        if cj > 0:
            D[i, i] = 1 / cj
    return D

def matriz_de_unos(n, m):
    matriz = MatrizRala(n, m)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            matriz[i, j] = 1
    return matriz


def PageRank(d, N, W, D):
    p_t0 = MatrizRala(N, 1)  # Initial equiprobable distribution
    for i in range(N):
        p_t0[i, 0] = 1 / N
    tolerance = 0.00000001
    diferencia = []
    error = 1

    Unos = MatrizRala(N,1)
    for i in range(N):
        Unos[i,0] = 1
    b = ((1 - d) / N) * Unos
    d_W = d * W
    d_WD = d_W @ D

    while error > tolerance:
        # Multiplica la matriz W_D por el vector p_t0 y escala por d

        p_t1 = d_WD @ p_t0
        p_t1 = b + p_t1
        # Calcula el error máximo en esta iteración comparando el nuevo vector de PageRank con el anterior

        error = MatrizRala.diffVectors(p_t1,p_t0)
        diferencia.append(error)

        # Actualiza el vector de PageRank para la próxima iteración

        p_t0 = p_t1
    return p_t0, diferencia

def main():
    
    # Llamar a la función y pasar la ruta al archivo CSV
    lista_citas = leer_citas()
    lista_papers = leer_papers()

    W = genW(lista_citas,lista_papers)
    
    D = genD(W)
    N = len(lista_papers)
    d = 0.85

    page_ranks = PageRank(d, N, W, D)
    
    # Create list of (PageRank score, index)
    lista = [(page_ranks[0][i, 0], i) for i in range(len(lista_papers))]

    # Sort by PageRank score in descending order
    sorted_papers = sorted(lista, key=lambda x: x[0], reverse=True)

    # Print the top 10 papers with podium ranking
    print("Top 10 Papers by PageRank con tolerancia de:0.00000001:")
    for rank, (score, index) in enumerate(sorted_papers[:10], start=1):
        print(f"{rank}. Paper ID: {lista_papers[index][0]}, Title: \"{lista_papers[index][1]}\", Score: {score:.6f}")


if __name__ == "__main__":
    main()
    