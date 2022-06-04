#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from math import inf
from typing import Tuple

matrix = [
    [inf, 2, 3, 2, 1, 2],
    [2, inf, 1, 3, 2, 4],
    [3, 1, inf, 1, 1, 3],
    [2, 3, 1, inf, 2, 2],
    [1, 2, 1, 2, inf, 3],
    [2, 4, 3, 2, 3, inf],
]


class Little_algorithm:
    def __init__(self, matrix):
        self.matrix = matrix

    def reduction(self, A: np.ndarray, verbose: bool = False) -> float:
        """
        Redukcja macierzy in-place (krok 1)
        """
        # sumaryczna redukcja
        sum_red = 0
        # odjęcie najmniejszego elementu od każdego wiersza
        mn = np.min(A, axis=1, keepdims=True)
        A -= mn
        sum_red += np.sum(mn)
        if verbose:
            print("Redukcja w wierszach:\n{}\n".format(A))

        # odjęcie najmniejszego elementu od każdej kolumny
        mn = np.min(A, axis=0, keepdims=True)
        A -= mn
        sum_red += np.sum(mn)
        if verbose:
            print("Redukcja w kolumnach:\n{}\n".format(A))
            print("Sumaryczna redukcja: {}\n".format(sum_red))
        return sum_red

    def optimal_edge(self, A: np.ndarray) -> Tuple[int, int]:
        """
        Wyszukiwanie odcinka o max koszcie wyłączenia (krok 2)
        """
        # === wyszukanie odcinka o najmniejszym koszcie ===
        A = A.astype('float')
        # zera w macierzy
        zera = np.where(A == 0)
        # suma maksymalna
        suma_max = -np.inf
        # najlepszy odcinek
        odcinek: Tuple[int, int] = (-1, -1)
        for i in zera[0]:
            y = zera[0][i]
            x = zera[1][i]
            A[y, x] = np.inf  # tymczasowe ustawienie na inf
            suma = np.min(A[y, :]) + np.min(A[:, x])
            A[y, x] = 0
            if suma > suma_max:
                suma_max = suma
                odcinek = (y, x)
        return odcinek
