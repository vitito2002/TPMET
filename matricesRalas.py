# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 

import numpy as np
import pandas as pd

# Supongamos que D es una matriz diagonal representada como un vector
class MatrizDiagonal:
    def __init__(self, diagonal):
        self.diagonal = diagonal
        self.shape = (len(diagonal), len(diagonal))

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
        m, n = Idx
        if m in self.filas:
            fila = self.filas[m]
            nodo_curr = fila.raiz
            while nodo_curr:
                columna, valor = nodo_curr.valor
                if columna == n:
                    return valor
                nodo_curr = nodo_curr.siguiente
        return 0

    
    def __setitem__( self, Idx, v ):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        m, n = Idx
        if m not in self.filas:
            fila_extra = ListaEnlazada()
            fila_extra.insertarFrente((n,v))
            self.filas[m] = fila_extra
        else:
            fila = self.filas[m]
            nodo_curr = fila.raiz
            nodo_previo = None
            while nodo_curr:
                columna = nodo_curr.valor[0]
                if columna==n:
                    nodo_curr.valor = (n,v)
                    return
                elif columna > n:
                    if not nodo_previo:
                        fila.insertarFrente((n,v))
                    else:
                        fila.insertarDespuesDeNodo((n,v),nodo_previo)
                    return
                nodo_previo = nodo_curr
                nodo_curr = nodo_curr.siguiente
            fila.push((n,v))
            

    def __mul__( self, k ):
        # Esta funcion  implementa el producto matriz-escalar -> A * k
        result = MatrizRala(*self.shape)
        for fila,lista in self.filas.items():
            nodo_curr = lista.raiz
            while nodo_curr:
                columna, valor = nodo_curr.valor
                result.__setitem__((fila,columna),valor*k)
                nodo_curr = nodo_curr.siguiente
        return result
    
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # Esta funcion implementa la suma de matrices -> A + B
        if self.shape != other.shape:
            raise ValueError("Las dimensiones de las matrices son diferentes y no se pueden sumar.")

        result = MatrizRala(*self.shape)
        for m,fila in self.filas.items():
            for n in range(self.shape[0]):
                _A = self.__getitem__((m,n))
                _B = other.__getitem__((m,n))
                result.__setitem__((m,n),_A + _B)
        for m, fila in other.filas.items():
            if m not in self.filas:
                result.filas[m] = fila
        return result


        # for i in range(self.shape[0]):
        #      for j in range(self.shape[1]):
        #          suma = self[i,j] + other [i,j]
        #          if suma != 0:
        #              result[i,j] = suma
        # return result


        # for (i, j), value in self.data.items():
        #     suma = value + other[i, j]
        #     if suma != 0:
        #         result[i, j] = suma
        # # Iterar sobre los elementos no nulos de la segunda matriz
        # for (i, j), value in other.data.items():
        #     if (i, j) not in self.data:
        #         if value != 0:
        #             result[i, j] = value
        # return 
        


    
    def __sub__( self, other ):
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        if self.shape != other.shape:
            raise ValueError("Las dimensiones de las matrices son diferentes y no se pueden restar.")
        
        return self .__add__(other.__mul__(-1))
    
    def __matmul__( self, other ):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación.")
        
        result = MatrizRala(self.shape[0], other.shape[1])
        
        contador = 0
        filas = len(self.filas)

        for i in self.filas:
            contador = contador + 1
            fila = self.filas[i]
            if fila.raiz:
                nodo_raiz = fila.raiz
                for j in range (other.shape[1]):
                    nodo_curr = nodo_raiz
                    total = 0
                    while nodo_curr:
                        j_curr = nodo_curr.valor[0]
                        total = total + nodo_curr.valor[1] * other[j_curr,j]
                        nodo_curr = nodo_curr.siguiente
                    result[i,j] = total
        # for i in range(self.shape[0]):
        #     for j in range(other.shape[1]):
        #         value = 0
        #         for k in range(self.shape[1]):
        #             value = value + (self.__getitem__((i,k)) * other.__getitem__((k,j))) 
        #         if value != 0:  # Solo almacenamos valores no cero
        #             result.__setitem__((i, j), value)
        #         #result.__setitem__((i,j),value)
        return result
    

        
    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '
            
            res += ']\n'

        res += '])'

        return res
    
    def multiplicacion_diagonal_rala(self, D):
        # Multiplicación eficiente entre una matriz diddagonal y una matriz rala
        if D.shape[1] != self.shape[0]:
            raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación.")

        result = MatrizRala(D.shape[0], self.shape[1])

        for i in range(self.shape[0]):
            if i in self.filas:
                fila = self.filas[i]
                nodo_curr = fila.raiz
                while nodo_curr:
                    columna, valor = nodo_curr.valor
                    result[(i, columna)] = D.diagonal[i] * valor
                    nodo_curr = nodo_curr.siguiente

        return result
    
    @staticmethod
    def diffVectors(v1,v2):
        """Agarra dos matricesRalas que son de 1 columna y compara su diferencia absoluta 
        por cada posicion y suma todas las diferencias

        Args:
            A (MatrizRala): Matriz de nx1
            B (MatrizRala): matriz de nx1

        Raises:
            ValueError: si las matrices no tienen la misma cantidad de filas

        Returns:
            int: Devuelve la sumatoria de las diferencias posicion a posicion
        """
        # Verificar que los vectores tengan la misma longitud
        if v1.shape[0] != v2.shape[0]:
            raise ValueError("Los vectores deben tener la misma longitud.")
        
        # Calcular la norma L1 de la diferencia entre los vectores
        # dif = 0
        # for i in v1.filas:
        #     fila = v1.filas[i]
        #     diferencia_absoluta = abs(v1[1,0]-v1[1,0])
        #     dif += diferencia_absoluta
        valorA = 0
        valorB = 0
        acumulado = 0
        for i in range(v1.shape[0]):
            if(i in v1.filas):
                filaA = v1.filas[i]
                valorA = filaA.raiz.valor[1]
            
            if(i in v2.filas):
                filaB = v2.filas[i]
                valorB = filaB.raiz.valor[1]
            acumulado += abs(valorA - valorB)
            valorA = 0
            valorB = 0

            
            
        # for i in range(v1.shape[0]):
        #     diferencia_absoluta = abs(v1[i,0] - v2[i,0])
        #     dif += diferencia_absoluta
        
        return acumulado



def GaussJordan(A, B):

    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado

    """
    Función que resuelve un sistema de ecuaciones lineales Ax = B utilizando el algoritmo de Gauss-Jordan.
    """
    # Concatenar A y B horizontalmente para formar una única matriz extendida
    
    m,n = A.shape
    if B.shape[0] != m or B.shape[1] != 1:
        raise ValueError ("Dimensiones no compatibles para un sistema")
    
    extended_matrix = MatrizRala(m,n+1)
    for i in range(m):
        for j in range (n):
            extended_matrix[i,j] = A[i,j]
        extended_matrix[i,n] = B[i,0]

    for i in range(m):
        if extended_matrix[i,i] == 0:
            intercambio = False
            for k in range(i+1,m):
                if extended_matrix[k,1] != 0:
                    for j in range(n+1):
                        extended_matrix[i,j], extended_matrix[k,j] = extended_matrix[k,j], extended_matrix[i,j]
                    intercambio = True
                    break
                if not intercambio:
                    raise ValueError("no se puede dividir por cero")
                
        pivote = extended_matrix[i,i]
        for j in range(n+1):
            if pivote != 0:
                extended_matrix[i,j] = extended_matrix[i,j]/pivote

        for k in range(m):
            if not k==i:
                factor = extended_matrix[k,i]
                for j in range (n+1):
                    extended_matrix[k,j] = extended_matrix[k,j] - factor * extended_matrix[i,j]

    sol = MatrizRala(m,1)
    for i in range(m):
        sol[i,0] = extended_matrix[i,n]
    return sol

