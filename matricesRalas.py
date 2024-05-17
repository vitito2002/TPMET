# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 

import numpy as np
import pandas as pd

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
        fila, columna = Idx
        if fila not in self.filas or columna not in self.filas[fila]:
            return 0
        else:
            return self.filas[fila][columna]
        pass
    
    def __setitem__( self, Idx, v ):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        fila, columna = Idx
        if fila not in self.filas:
            self.filas[fila] = {}
        self.filas[fila][columna] = v
        pass

    def __mul__( self, k ):
        # Esta funcion implementa el producto matriz-escalar -> A * k
        result = MatrizRala(*self.shape)
        for fila in self.filas:
            result.filas[fila] = {columna: self.filas[fila][columna] * k for columna in self.filas[fila]}
        return result
        pass
    
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # Esta funcion implementa la suma de matrices -> A + B
        if self.shape != other.shape:
            raise ValueError("Las dimensiones de las matrices son diferentes y no se pueden sumar.")

        result = MatrizRala(*self.shape)
        for fila in range(self.shape[0]):
            for columna in range(self.shape[1]):
                result[(fila, columna)] = self[(fila, columna)] + other[(fila, columna)]
        return result
        pass
    
    def __sub__( self, other ):
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        if self.shape != other.shape:
            raise ValueError("Las dimensiones de las matrices son diferentes y no se pueden restar.")
        
        return self + (-1 * other)
        pass
    
    def __matmul__( self, other ):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación.")
        
        result = MatrizRala(self.shape[0], other.shape[1])
        for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                for k in range(self.shape[1]):
                    result[(i, j)] += self[(i, k)] * other[(k, j)]
        return result
        pass                

        
    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '
            
            res += ']\n'

        res += '])'

        return res



def GaussJordan(A, B):

    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado

    """
    Función que resuelve un sistema de ecuaciones lineales Ax = B utilizando el algoritmo de Gauss-Jordan.
    """
    # Concatenar A y B horizontalmente para formar una única matriz extendida
    extended_matrix = np.hstack((A.astype(float), B.astype(float)))

    # Iniciar el proceso de reducción de Gauss-Jordan
    pivot_col = 0
    n_rows, n_cols = extended_matrix.shape
    for row in range(n_rows):
        if pivot_col >= n_cols - 1:
            return extended_matrix[:, -1].reshape(-1, 1)  # Devolver la solución x

        row_pivot = row
        while abs(extended_matrix[row_pivot][pivot_col]) < 1e-5:
            row_pivot += 1
            if row_pivot == n_rows:
                row_pivot = row
                pivot_col += 1
                if n_cols - 1 == pivot_col:
                    return extended_matrix[:, -1].reshape(-1, 1)  # Devolver la solución x
            else:
                extended_matrix[[row_pivot, row]] = extended_matrix[[row, row_pivot]]

        pivot = extended_matrix[row][pivot_col]
        extended_matrix[row] = [mrx / float(pivot) for mrx in extended_matrix[row]]

        for other_row in range(n_rows):
            if other_row != row:
                below_pivot = extended_matrix[other_row][pivot_col]
                extended_matrix[other_row] = [iv - below_pivot * rv for rv, iv in zip(extended_matrix[row], extended_matrix[other_row])]
        pivot_col += 1

    return extended_matrix[:, -1].reshape(-1, 1)  # Devolver la solución x

# Ejemplo de uso
A = np.array([[1, -5,],
              [3, 7,]
              ])

B = np.array([[-2],
              [-2],
              ])

solution = GaussJordan(A, B)
print("La solución del sistema es:")
print(solution)




