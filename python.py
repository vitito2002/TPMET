from matricesRalas import MatrizRala, GaussJordan
import numpy as np
import pandas as pd
from matricesRalas import *
import csv


papers = pd.read_csv("papers/papers.csv", header=0)
citas = pd.read_csv("papers/citas.csv", header=0)


def leer_citas():
    archivo_citas = "papers/citas.csv"
    citas = []
    with open(archivo_citas, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)
        for cita, citado in lector:
            citas.append((int(cita), int(citado)))
    return citas


def leer_papers():
    archivo_papers = "papers/papers.csv"
    papers = []

    with open(archivo_papers, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            papers.append(
                [fila["id"], fila["titulo"], fila["autores"], fila["anio"]]
            )
    return papers

def genW(lista_citas, lista_papers):
    W = MatrizRala(len(lista_papers), len(lista_papers))
    for citate, cita in lista_citas:
        W[citate, cita] = 1
    return W

def genD(W):
    D = MatrizRala(W.shape[0], W.shape[1])
    for i in W.filas:
        contador = 0
        curr = W.filas[i].raiz
        while curr:
            contador = contador+ curr.valor[1]
            curr = curr.siguiente
        if contador > 0:
            D[i, i] = 1 / contador
    return D

def PageRank(d, N, W, D):
    p_t0 = MatrizRala(N, 1)  # Initial equiprobable distribution
    for i in range(N):
        p_t0[i, 0] = 1 / N
    tolerance = 0.01
    diferencia = []
    error = 1

    Unos = MatrizRala(N,1)
    for i in range(N):
        Unos[i,0] = 1
    b = ((1 - d) / N) * Unos
    d_W = d * W
    d_WD = d_W @ D

    while error > tolerance:
        p_t1 = d_WD @ p_t0
        p_t1 = b + p_t1
        error = MatrizRala.diffVectors(p_t1,p_t0)
        diferencia.append(error)
        p_t0 = p_t1
    return p_t0, diferencia

def main():
    lista_citas = leer_citas()
    lista_papers = leer_papers()
    W = genW(lista_citas,lista_papers)
    D = genD(W)
    N = len(lista_papers)
    d = 0.85
    page_ranks = PageRank(d, N, W, D)
    lista = [(page_ranks[0][i, 0], i) for i in range(len(lista_papers))]
    sorted_papers = sorted(lista, key=lambda x: x[0], reverse=True)
    print("Top 10 papers con mayor impacto de:0.00000001:")
    for rank, (score, index) in enumerate(sorted_papers[:10], start=1):
        print(f"{rank}. ID: {lista_papers[index][0]}, Titulo: \"{lista_papers[index][1]}\", Impacto: {score:.6f}")


if __name__ == "__main__":
    main()
    