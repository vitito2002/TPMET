# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan

class ListaEnlazada:
    def __init__( self ):
        self.raiz = None
        self.longitud = 0
        self.current = self.Nodo(None, self.raiz)

    def insertarFrente( self, valor ):
        # Inserta un elemento al inicio de la lista
        if len(self) == 0:
            return self.push(valor)

        nuevoNodo = self.Nodo( valor, self.raiz )
        self.raiz = nuevoNodo
        self.longitud += 1

        return self

    def insertarDespuesDeNodo( self, valor, nodoAnterior ):
        # Inserta un elemento tras el nodo "nodoAnterior"
        nuevoNodo = self.Nodo( valor, nodoAnterior.siguiente)
        nodoAnterior.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def push( self, valor ):
        # Inserta un elemento al final de la lista
        if self.longitud == 0:
            self.raiz = self.Nodo( valor, None )
        else:
            nuevoNodo = self.Nodo( valor, None )
            ultimoNodo = self.nodoPorCondicion( lambda n: n.siguiente is None )
            ultimoNodo.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def pop( self ):
        # Elimina el ultimo elemento de la lista
        if len(self) == 0:
            raise ValueError("La lista esta vacia")
        elif len(self) == 1:
            self.raiz = None
        else:
            anteUltimoNodo = self.nodoPorCondicion( lambda n: n.siguiente.siguiente is None )
            anteUltimoNodo.siguiente = None

        self.longitud -= 1

        return self

    def nodoPorCondicion( self, funcionCondicion ):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError('No hay nodos en la lista')

        nodoActual = self.raiz
        while not funcionCondicion( nodoActual ):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError('Ningun nodo en la lista satisface la condicion')

        return nodoActual

    def __len__( self ):
        return self.longitud

    def __iter__( self ):
        self.current = self.Nodo( None, self.raiz )
        return self

    def __next__( self ):
        if self.current.siguiente is None:
            raise StopIteration
        else:
            self.current = self.current.siguiente
            return self.current.valor

    def __repr__( self ):
        res = 'ListaEnlazada([ '

        for valor in self:
            res += str(valor) + ' '

        res += '])'

        return res

    class Nodo:
        def __init__( self, valor, siguiente ):
            self.valor = valor
            self.siguiente = siguiente


class MatrizRala:
    def __init__( self, M, N ):
        self.filas = {}
        self.shape = (M, N)

    def __getitem__( self, Idx ):
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]
        # tupla m= filas y n = columnas
        m,c = Idx
        if m in self.filas:
            fila = self.filas[m]
            actual = fila.raiz
            while actual is not None:
                if actual.valor[0] == c:
                    return actual.valor[1]
                actual = actual.siguiente
        return 0

    def __setitem__(self, Idx, v):
        # Esta función implementa la asignación durante indexación (Idx es una tupla (m,n)) -> A[m,n] = v
        m, c = Idx # m filas, c columnas
    
        if m in self.filas:
            fila = self.filas[m]
            actual = fila.raiz
            anterior = None
            while actual is not None:
                if actual.valor[0] == c:
                    # Si la columna ya existe en la fila, actualizamos el valor
                    if v == 0:
                    # Si el valor es cero, eliminamos el nodo
                        if anterior is None:
                            fila.raiz = actual.siguiente
                        else:
                            anterior.siguiente = actual.siguiente
                    # Si la fila está vacía después de eliminar el nodo, eliminamos la fila
                        if fila.raiz is None:
                            del self.filas[m]    
                    else:
                        actual.valor = (c, v)
                        return
                elif actual.valor[0] > c and v != 0:
                    # Si encontramos una columna mayor que la que buscamos, insertamos el nuevo valor antes
                    nuevo_nodo = ListaEnlazada.Nodo((c, v), actual)
                    if anterior is None:
                        fila.raiz = nuevo_nodo
                    else:
                        anterior.siguiente = nuevo_nodo
                        nuevo_nodo.siguiente = actual  # Actualizamos el puntero siguiente del nuevo nodo
                    return
                anterior = actual
                actual = actual.siguiente
            # Si la columna no existe en la fila, la insertamos al final de la fila
            fila.insertarDespuesDeNodo((c, v), anterior)  # Pasamos el valor y el nodo anterior
        else:
            # Si la fila no existe, creamos una nueva fila con el valor asignado
            fila = ListaEnlazada()
            fila.push((c, v))
            self.filas[m] = fila


    def __mul__(self, k):
        # Esta función implementa el producto matriz-escalar -> A * k
        matriz_resultado = MatrizRala(self.shape[0], self.shape[1])
        for i in (self.filas):
                actual = self.filas[i].raiz
                while actual is not None:
                    valor = self[i,actual.valor[0]] * k
                    if valor != 0:
                        matriz_resultado[i,actual.valor[0]] = valor  # Asignar el valor multiplicado a la matriz resultante
                    actual = actual.siguiente
        return matriz_resultado

    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__(self, other):
        # Verifica que las matrices tengan la misma forma
        if self.shape != other.shape:
            raise ValueError("Las matrices deben tener la misma forma para ser sumadas.")

        # Crea una matriz resultante con los mismos tamaños que las matrices de entrada
        result = MatrizRala(self.shape[0], self.shape[1])

        # Itera sobre las filas
        for i in self.filas:
            # Verifica si la fila i está presente en other
            if i in other.filas:
                current_self = self.filas[i].raiz
                current_other = other.filas[i].raiz
                # Itera sobre los elementos de la fila i en self y other
                while current_self is not None or current_other is not None:
                    if current_self is None:
                        # Si no hay más elementos en self, copia los elementos restantes de other
                        result[i, current_other.valor[0]] = current_other.valor[1]
                        current_other = current_other.siguiente
                    elif current_other is None:
                        # Si no hay más elementos en other, copia los elementos restantes de self
                        result[i, current_self.valor[0]] = current_self.valor[1]
                        current_self = current_self.siguiente
                    elif current_self.valor[0] == current_other.valor[0]:
                        # Si los elementos tienen la misma columna, suma los valores
                        suma = current_self.valor[1] + current_other.valor[1]
                        if suma != 0:
                            result[i, current_self.valor[0]] = suma
                        current_self = current_self.siguiente
                        current_other = current_other.siguiente
                    elif current_self.valor[0] < current_other.valor[0]:
                        # Si el índice de columna de self es menor que el de other, copia el elemento de self
                        result[i, current_self.valor[0]] = current_self.valor[1]
                        current_self = current_self.siguiente
                    else:
                        # Si el índice de columna de other es menor que el de self, copia el elemento de other
                        result[i, current_other.valor[0]] = current_other.valor[1]
                        current_other = current_other.siguiente
            else:
                # Si la fila está presente en self pero no en other, copia los elementos de self
                current_self = self.filas[i].raiz
                while current_self is not None:
                    result[i, current_self.valor[0]] = current_self.valor[1]
                    current_self = current_self.siguiente

        # Copia los elementos de other que no están presentes en self
        for i in other.filas:
            if i not in self.filas:
                current_other = other.filas[i].raiz
                while current_other is not None:
                    result[i, current_other.valor[0]] = current_other.valor[1]
                    current_other = current_other.siguiente

        return result

    def __sub__(self, other):
        # Verifica que las matrices tengan la misma forma
        if self.shape != other.shape:
            raise ValueError("Las matrices deben tener la misma forma para ser restadas.")

        # Crea una matriz resultante inicializada como una matriz rala de la misma forma que las matrices de entrada
        result = MatrizRala(self.shape[0], self.shape[1])

        result = self + (-1 * other)

        return result


    def __matmul__( self, other ):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise Exception

        if self.shape[1] != other.shape[0]:
            raise Exception

        # Se crea una nueva matriz rala 'res' con el número de filas de la primera matriz (self)
        # y el número de columnas de la segunda matriz (other).
        res = MatrizRala(self.shape[0], other.shape[1])

        # Iterar solo sobre los elementos no nulos en la primera matriz (self).
        for i in self.filas:
            # Se verifica si la fila 'i' está presente en self.
            if i in self.filas:
                current_row = self.filas[i].raiz  # Puntero al inicio de la fila 'i' en self.
                while current_row is not None:
                    k = current_row.valor[0]  # Índice de columna en self que corresponde al índice de fila en other.
                    # Si la fila 'k' está presente en other.
                    if k in other.filas:
                        current_col = other.filas[k].raiz  # Puntero al inicio de la fila 'k' en other.
                        while current_col is not None:
                            j = current_col.valor[0]  # Índice de columna en other.
                            # Multiplicar y añadir al elemento correspondiente en res.
                            res[i, j] += self[i, k] * other[k, j]
                            current_col = current_col.siguiente  # Avanzar al siguiente nodo en la fila 'k' de other.
                    current_row = current_row.siguiente  # Avanzar al siguiente nodo en la fila 'i' de self.

        # Devolver la matriz resultante 'res' que contiene el producto matricial de self y other.
        return res


    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '

            res += ']\n'

        res += '])'

        return res

def GaussJordan(A, b):
    if A.shape[0] != b.shape[0]:
        raise ValueError("Los tamaños de b y A no son compatibles")

    # Crear la matriz aumentada
    M = MatrizRala(A.shape[0], A.shape[1] + 1)
    for i in A.filas:
        actual = A.filas[i].raiz
        while actual is not None:
            M[i, actual.valor[0]] = actual.valor[1]
            actual = actual.siguiente

    for i in b.filas:
        M[i, A.shape[1]] = b[i, 0]

    for i in range(A.shape[0]):
        # Hacer pivote en M[i, i]
        if M[i, i] == 0: # si mi pivote es 0
            for k in range(i + 1, A.shape[0]): #intercambio filas hasta que pivote != 0
                if M[k, i] != 0:
                    for j in range(A.shape[1] + 1):
                        M[i, j], M[k, j] = M[k, j], M[i, j]
                    break
            if M[i, i] == 0:
                if M[i, A.shape[1]] == 0:
                    raise ValueError("El sistema tiene infinitas soluciones.")
                else:
                    raise ValueError("El sistema no tiene solución.")

        # Dividir fila i por M[i, i] para que el pivote sea 1
        divisor = M[i, i]
        actual = M.filas[i].raiz
        while actual != None:
            actual.valor = (actual.valor[0], actual.valor[1]/divisor)
            actual = actual.siguiente

        # Hacer ceros en la columna del pivote para todas las filas excepto la fila i
        for k in M.filas:
            if k != i:
                factor = M[k,i]
                for j in range(A.shape[1] + 1):     #no puedo iterar por filas porque a los 0s tambien se les debe restar
                    M[k, j] -= factor * M[i, j]

    # Comprobar si el sistema tiene solución
    for i in M.filas:
        actual = M.filas[i].raiz
        suma = 0
        while actual != None:
            if actual.valor[0] != M.shape[0]:
                suma = suma + actual.valor[1]
            actual = actual.siguiente
        if suma == 0 and M[i, A.shape[1]] != 0:
            raise ValueError("El sistema no tiene solución.")

    pivot_count = sum(1 for i in range(min(A.shape[0], A.shape[1])) if M[i, i] != 0) #debo recorrer por shape porque en todas las posiciones debe haber un pivote
    if pivot_count < A.shape[1]:
        raise ValueError("El sistema tiene infinitas soluciones debido a las variables libres.")

    x = MatrizRala(A.shape[0], 1) #extraemos el vector solucion
    for i in M.filas:
        x[i,0] = M[i, A.shape[1]]
    return x

def suma_constante_matriz(matriz, constante):
    # Suma de una constante a cada elemento
    result = MatrizRala(matriz.shape)
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            result[i, j] = matriz[i, j] + constante
    return result


def multiplicar_matriz_vector(matriz, vector):
    resultado = [0] * len(vector)
    for i in range(len(vector)):
        suma = 0
        for j in range(len(vector)):
            suma += matriz[i, j] * vector[j]
        resultado[i] = suma
    return resultado
