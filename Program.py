#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import deepcopy
import numpy as np
from math import inf
from typing import Tuple, List

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
        for i in range(len(zera[0])):
            y = zera[0][i]
            x = zera[1][i]
            A[y, x] = np.inf  # tymczasowe ustawienie na inf
            suma = np.min(A[y, :]) + np.min(A[:, x])
            A[y, x] = 0
            if suma > suma_max:
                suma_max = suma
                odcinek = (y, x)
        if odcinek == (-1, -1):
            raise RuntimeError("Nie znaleziono jakiegokolwiek wierzchołka optymalnego - błąd?")
        return odcinek

    def two_matrix(self, matrix, edge):
        row, col = edge
        M1 = deepcopy(matrix)  # Macierz z usuniętym wierszem i kolumną
        M1[row, :] = inf
        M1[:, col] = inf

        M2 = deepcopy(matrix)  # Macierz z usuniętym odcinkiem
        M2[row, col] = inf
        return M1, M2

    def algorithm(self, matrix):
        size = len(matrix)
        LB_result = inf
        edges_result = []
        path_result: List[int] = []

        LB = self.reduction(matrix)
        P = [matrix, LB, []]
        Problem_list = [P]
        PP_counter = 0
        while Problem_list:
            # Zajęcie się podproblemem - usunięcie go z listy
            matrix, LB, edges = Problem_list.pop(0)
            print('='*50)
            print('PP.',PP_counter)
            print(matrix)
            print('LB = ',LB)
            print("Ścieżka: ", edges)
            print('='*50)
            PP_counter += 1


            # # Gdy LB pod problemu większe niż LB aktualnego rozwiązania - KZ2
            if LB > LB_result:
                continue

            # if np.max(matrix) == np.min(matrix):  # KZ1
            #     continue

            # Czy znaleziono rozwiązanie dla podproblemu?
            #  === Kryteria zamykania ===
            # Sprawdź, czy istnieje jednoznaczna ścieżka TSP
            # Jeśli istnieje i nie jest podcyklem - rozwiązanie
            # Jeśli to podcykl - zamknij podproblem
            # Podcykl nie powinien się zdarzyć, dlatego zgłoś wtedy błąd

            # zaczynam od dowolnego wierzchołka
            v_start: int = 0
            v: int = v_start
            loop_length: int = 0
            problem_closed: bool = False
            full_path: List[int] = [v]
            while True:

                # poszukuję następny wierzchołek, najpierw w obowiązkowych krawędziach
                try:
                    v = next(v2 for v1, v2 in edges if v1 == v)
                    # znaleziono wierzchołek
                except StopIteration:
                    # nie ma takiej krawędzi, przeszukaj macierz
                    # w macierzy musi być tylko jedno wyjście dla danego wierzchołka
                    m = matrix[v, :]
                    u = np.where(m != np.inf)[0]
                    if len(u) == 1:
                        # znaleziono następny wierzchołek
                        v = u[0]
                    elif len(u) == 0: 
                        # nie można przejść dalej - KZ1
                        problem_closed = True
                        break
                    else:
                        # za dużo możliwości przejścia - KZ0
                        break

                # ścieżka jest dłuższa
                loop_length += 1
                full_path.append(v)

                # warunek do-while
                # znaleziono jakiś (pod)cykl
                if v == v_start:
                    # sprawdzam, czy to nie jest podcykl
                    if loop_length != size:
                        # KZ1
                        problem_closed = True
                    break
            
            if problem_closed:
                continue

            # jeśli udało się przejść pełną ścieżkę, sprawdź KZ3
            if loop_length == size:
                if LB < LB_result:
                    # nastąpiła poprawa rozwiązania
                    LB_result = LB
                    edges_result = edges
                    path_result = full_path
                continue

            # Znajdź krawędź o optymalnym koszcie wyłączenia
            edge = self.optimal_edge(matrix)

            # Wyznacz macierze dla nowych podproblemów
            M_with_edge, M_without_edge = self.two_matrix(matrix, edge)

            # Pierwszy podproblem
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
                        raise RuntimeError("Osiągnięto niechciany (pod)cykl")
                    # dłukość cyklu zwiększona o 1
                    dlugosc += 1
                except StopIteration:
                    # udało się bez problemów dotrzeć do końca ścieżki
                    break

            # zabronienie przejścia (k, p)
            M_with_edge[k, p] = np.inf
            # Nowa redukcja
            LB_with_edge = LB + self.reduction(M_with_edge)

            # Drugi podproblem
            # Redukcja i nowe LB
            LB_without_edge = LB + self.reduction(M_without_edge)

            # Dodanie problemu do listy podproblemów
            if np.max(M_with_edge) != np.min(M_with_edge):  # KZ1
                Problem_list.append([M_with_edge, LB_with_edge, edges + [edge]])
            if np.max(M_without_edge) != np.min(M_without_edge):  # KZ1
                Problem_list.append([M_without_edge, LB_without_edge, edges])

            # Posortowanie podproblemów pod względem LB
            Problem_list.sort(key=lambda elem: elem[1], reverse=False)

        print(LB_result)
        print(path_result)


# matrix = [
#     [inf, 5, 4, 6, 6],
#     [8, inf, 5, 3, 4],
#     [4, 3, inf, 3, 1],
#     [8, 2, 5, inf, 6],
#     [2, 2, 7, 0, inf],
# ]

matrix = [
    [inf, 8, 7, 3, 8],
    [8, inf, 9, 3, 8],
    [7, 7, inf, 9, 4],
    [6, 3, 9, inf, 5],
    [3, 9, 3, 8, inf],
]

cm1 = [[inf, 10, 8, 19, 12],
       [10, inf, 20, 6, 3],
       [8,  20, inf, 4, 2],
       [19, 6, 4, inf, 7],
       [12, 3, 2, 7, inf]]

sample_matrix = [
    [inf,2,3,2,1,4],
    [2,inf,1,2,1,2],
    [3,1,inf,3,4,1],
    [2,2,3,inf,2,2],
    [1,1,4,2,inf,3],
    [4,2,1,2,3,inf],
]

little = Little_algorithm(sample_matrix)
little.algorithm(np.array(sample_matrix))
