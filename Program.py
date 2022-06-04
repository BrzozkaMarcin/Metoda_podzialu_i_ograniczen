#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import deepcopy
import numpy as np
from math import inf
from typing import Tuple


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
        mn[mn == np.inf] = 0  # może się zdarzyć, że będą tylko infy
        A -= mn
        sum_red += np.sum(mn)
        if verbose:
            print("Redukcja w wierszach:\n{}\n".format(A))

        # odjęcie najmniejszego elementu od każdej kolumny
        mn = np.min(A, axis=0, keepdims=True)
        mn[mn == np.inf] = 0  # może się zdarzyć, że będą tylko infy
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

    def two_matrix(self, matrix, edge):
        row, col = edge
        M1 = deepcopy(matrix)  # Macierz z usuniętym wierszem i kolumną
        M1[row, :] = inf
        M1[:, col] = inf

        M2 = deepcopy(matrix)  # Macierz z usuniętym odcinkiem
        M2[row, col] = inf
        return M1, M2

    def algoritm(self, matrix):
        LB = inf
        solution = []

        cost = self.reduction(matrix)
        P = [matrix, cost, []]
        Problem_list = [P]

        while Problem_list:
            matrix, cost, edges = Problem_list.pop()

            if cost > LB:
                continue

            edge = self.optimal_edge(matrix)
            M_with_edge, M_without_edge = self.two_matrix(matrix, edge)

            # Pierwszy podproblem
            # Zabronienie podcyklu
            # Dodatkowa redukcja i nowe LB

            # PSikorski

            # Utwórz ścieżkę z posiadanych krawędzi, zaczynając od najnowszej.
            # A dokładniej wystarczy znaleźć wierzchołek początkowy i końcowy,
            # kontrolując przy tym długość podcyklu

            dlugosc: int = 1
            p: int = edge[0]
            k: int = edge[1]

            # przeszukanie do przodu - poszukiwanie końca
            while True:
                try:
                    # znajdź początek następnej krawędzi
                    # i zastąp jej koniec
                    k = next(v2 for v1, v2 in edges if v1 == k)

                    # warunek bezpieczeństwa: nie stworzyliśmy podcyklu
                    if k == edge[1]:
                        # TODO: sprawdzić, czy trzeba obsługiwać zaistnienie podcyklu
                        raise RuntimeError("Osiągnięto niechciany (pod)cykl")

                    # dłukość cyklu zwiększona o 1
                    dlugosc += 1

                except StopIteration:
                    # udało się bez problemów dotrzeć do końca ścieżki
                    break

            # przeszukanie do tyłu - poszukiwanie początku
            # tylko kilka zmiennych zmienionych
            while True:
                try:
                    # znajdź początek następnej krawędzi
                    # i zastąp jej koniec
                    p = next(v1 for v1, v2 in edges if v2 == p)

                    # warunek bezpieczeństwa: nie stworzyliśmy podcyklu
                    if p == edge[0]:
                        # TODO: patrz wyżej do analogicznego miejsca
                        raise RuntimeError("Osiągnięto niechciany (pod)cykl")

                    # dłukość cyklu zwiększona o 1
                    dlugosc += 1

                except StopIteration:
                    # udało się bez problemów dotrzeć do końca ścieżki
                    break
            
            # zabronienie przejścia (k, p)
            # TODO: sprawdź, czy to dobra macierz
            M_with_edge[k, p] = np.inf

            # /PSikorski

            # Drugi podproblem
            # Redukcja i nowe LB


# matrix = [
#     [inf, 2, 3, 2, 1, 2],
#     [2, inf, 1, 3, 2, 4],
#     [3, 1, inf, 1, 1, 3],
#     [2, 3, 1, inf, 2, 2],
#     [1, 2, 1, 2, inf, 3],
#     [2, 4, 3, 2, 3, inf],
# ]

matrix = [
    [inf, 5, 4, 6, 6],
    [8, inf, 5, 3, 4],
    [4, 3, inf, 3, 1],
    [8, 2, 5, inf, 6],
    [2, 2, 7, 0, inf],
]

little = Little_algorithm(matrix)
little.algoritm(np.array(matrix))
