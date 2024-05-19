import csv
# Función para leer citas desde el archivo "citas.csv"
def leer_citas():
    archivo_citas = "papers/citas.csv"
    citas = []
    with open(archivo_citas, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)  # Saltar la fila del encabezado
        for cita, citado in lector:
            citas.append((int(cita), int(citado)))
    return citas
def leer_papers():
    archivo_papers = "papers/papers.csv"
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

def main():
    # Leer citas y papers
    lista_citas = leer_citas()
    lista_papers = leer_papers()

    # Crear un diccionario para almacenar el número de citas por paper
    num_citas_por_paper = {}

    # Contar el número de citas por paper
    for cita, citado in lista_citas:
        if citado in num_citas_por_paper:
            num_citas_por_paper[citado] += 1
        else:
            num_citas_por_paper[citado] = 1

    # Crear una lista de tuplas (cantidad de citas, índice del paper)
    citas_por_paper = [(num_citas_por_paper.get(index, 0), index) for index in range(len(lista_papers))]

    # Ordenar la lista de tuplas por la cantidad de citas en orden descendente
    citas_por_paper.sort(reverse=True)

    # Imprimir los top 10 papers con la mayor cantidad de citas
    print("Top 10 Papers por cantidad de citas:")
    for rank, (num_citas, index) in enumerate(citas_por_paper[:10], start=1):
        print(f"{rank}. Paper ID: {lista_papers[index][0]}, Title: \"{lista_papers[index][1]}\", Citations: {num_citas}")

if __name__ == "__main__":
    main()
