# Para correr los tests:
#   1- Instalar pytest: ("pip install pytest")
#   2- Correr en la terminal "pytest tests.py"

import pytest
from matrices_ralas import MatrizRala, GaussJordan
import numpy as np

class TestIndexacionMatrices:
    def test_indexarCeros( self ):
        A = MatrizRala(3,3)
        
        assert np.allclose( np.zeros(9), [A[i,j] for i in range(3) for j in range(3)] )

    def test_asignarValor( self ):
        A = MatrizRala(3,3)
        A[0,0] = 1

        assert A[0,0] == 1

    def test_asignarDejaCeros(self):
        A = MatrizRala(3,3)
        A[0,0] = 1

        assert np.allclose( np.zeros(9), [A[i,j] if (i != j and i != 0) else 0 for i in range(3) for j in range(3)] )

    def test_asignarEnMismaFila( self ):
        A = MatrizRala(3,3)
        A[0,1] = 2
        A[0,0] = 1

        assert A[0,1] == 2 and A[0,0] == 1

    def test_reasignar( self ):
        A = MatrizRala(3,3)
        A[1,0] = 1
        A[1,0] = 3

        assert A[1,0] == 3

class TestSumaMatrices:
    def test_distintasDimensiones( self ):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)
        with pytest.raises(Exception) as e_info:
            C = A + B
        
    def test_sumaCorrectamente( self ):
        A = MatrizRala(3,3)
        B = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[2,2]=4

        B[0,2]=3
        B[1,1]=2

        C = A+B
        assert C[0,0] == 1 and C[0,2] == 6 and C[2,2] == 4 and C[1,1] == 2

class TestProductoPorEscalar:
    def test_escalaCorrectamente( self ):
        A = MatrizRala(3,3)
        A[0,0]=1
        A[0,2]=3
        A[2,2]=4

        C = A * 13
        assert C[0,0] == (1*13) and C[0,2] == (3*13) and C[2,2] == (4*13)

class TestProductoMatricial:
    def test_dimensionesEquivocadas(self):
        A = MatrizRala(2,3)
        B = MatrizRala(4,3)
        with pytest.raises(Exception) as e_info:
            C = A @ B

    def test_productoAndaBien(self):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[1,2]=4

        B[2,0]=3
        B[1,1]=2

        C = A @ B

        assert C.shape[0] == 2 and C.shape[1]==3 and C[0,0] == 9 and C[0,1] == 0 and C[0,2] == 0 and C[1,0] == 12 and C[1,1] == 0 and C[1,2] == 0

    def test_productoPorIdentidad( self ):
        A = MatrizRala(3,3)
        Id = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[1,2]=4

        Id[0,0] = 1
        Id[1,1] = 1
        Id[2,2] = 1

        C1 = A @ Id
        C2 = Id @ A
        assert C1[0,0] == 1 and C1[0,2] == 3 and C1[1,2] == 4 and C2[0,0] == 1 and C2[0,2] == 3 and C2[1,2] == 4 and C1.shape == C2.shape and C1.shape == A.shape

class TestGaussJordan:
    def test_tamanos( self ):
        A = MatrizRala(2,2)
        b = MatrizRala(3,1)

        with pytest.raises(Exception) as e_info:
            GaussJordan(A,b)

    def test_matrizSingularTiraError( self ):
        A = MatrizRala(3,3)
        b = MatrizRala(3,1)

        b[0,0] = 1
        b[1,0] = 2
        b[2,0] = 3

        with pytest.raises(Exception) as e_info:
            GaussJordan(A,b)

    def test_identidad( self ):
        A = MatrizRala(3,3)
        b = MatrizRala(3,1)

        A[0,0] = 1
        A[1,1] = 1
        A[2,2] = 1

        b[0,0] = 1
        b[1,0] = 2
        b[2,0] = 3

        x = GaussJordan(A,b)

        assert x[0,0] == 1 and x[1,0] == 2 and x[2,0] == 3

    def test_triangularSup( self ):
        A = MatrizRala(3,3)
        b = MatrizRala(3,1)

        A[0,0] = 1
        A[1,1] = 1
        A[2,2] = 1
        A[0,1] = 1
        A[0,2] = 1
        A[1,2] = 1

        b[0,0] = 1
        b[1,0] = 2
        b[2,0] = 3

        x = GaussJordan(A,b)

        assert np.isclose( x[0,0], -1 ) and np.isclose(x[1,0], -1) and np.isclose(x[2,0], 3)

    def test_completa( self ):
        A = MatrizRala(3,3)
        b = MatrizRala(3,1)

        A[0,0] = 1
        A[1,0] = 2
        A[2,0] = 3

        A[2,1] = 5
        A[0,2] = 12
        A[2,2] = 2.34

        b[0,0] = 1
        b[1,0] = 1
        b[2,0] = 1

        x = GaussJordan(A,b)

        assert np.isclose( x[0,0], 0.5 ) and np.isclose(x[1,0], -0.1195) and np.isclose(x[2,0], 0.041667)






