# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 
import numpy as np

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
        # COMPLETAR:
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]
        pass
    
    def __setitem__( self, Idx, v ):
        # COMPLETAR:
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        pass

    def __mul__( self, k ):
        # COMPLETAR:
        # Esta funcion implementa el producto matriz-escalar -> A * k
        pass
    
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa la suma de matrices -> A + B
        pass
    
    def __sub__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        pass
    
    def __matmul__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
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
A = np.array([[2, -1,6],
              [2, -1,6],
              [2, -1,6]])

B = np.array([[0],
              [0],
              [0]])

solution = GaussJordan(A, B)
print("La solución del sistema es:")
print(solution)




