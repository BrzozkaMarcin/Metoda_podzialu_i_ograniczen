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

    def redukcja_i_odcinek(self, A: np.ndarray) -> Tuple[float, Tuple[int, int]]:
        """
        Algorytm Little'a - redukcja macierzy

        :param A: Macierz przejść do redukcji, jest redukowana in-place.
        :type A: np.ndarray

        :returns: Wartość redukcji oraz indeksy wierzchołków najlepszego odcinka do wyłączenia
        :rtype: Tuple[float, int]
        """
        print("redukcja_i_odcinek - nie zaimplementowane")
        return 0, (0, 1)

    def algorithm(self):

        matrix = self.redukcja_i_odcinek()
