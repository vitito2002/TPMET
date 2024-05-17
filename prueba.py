def imprimir_matriz(matriz):
    for fila in matriz:
        print(' '.join(f'{num:>8.4f}' if isinstance(num, float) else f'{num:>8}' for num in fila))
    print()

def gauss_jordan_con_respuestas(matriz):
    num_filas = len(matriz)
    num_columnas = len(matriz[0])
    
    for i in range(num_filas):
        max_row = max(range(i, num_filas), key=lambda r: abs(matriz[r][i]))
        matriz[i], matriz[max_row] = matriz[max_row], matriz[i]

        pivot = matriz[i][i]
        for j in range(i, num_columnas):
            matriz[i][j] /= pivot
        imprimir_matriz(matriz)
        
        for k in range(num_filas):
            if k != i:
                factor = matriz[k][i]
                for j in range(i, num_columnas):
                    matriz[k][j] -= factor * matriz[i][j]
        imprimir_matriz(matriz)

    respuestas = [fila[-1] for fila in matriz]
    for idx, valor in enumerate(respuestas, start=1):
        print(f'x{idx} = {valor:.4f}')

# Preguntar al usuario el número de variables/ecuaciones
num_variables = int(input('¿Cuántas variables deseas resolver? '))

# Construir la matriz basada en la entrada del usuario
matriz = []
print(f'Introduce los coeficientes y el término independiente para cada ecuación:')
for i in range(num_variables+1):
    fila = list(map(float, input(f'Ecuación {i+1}: ').split()))
    matriz.append(fila)

gauss_jordan_con_respuestas(matriz)