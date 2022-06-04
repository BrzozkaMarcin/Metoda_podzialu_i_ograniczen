# autor: Piotr Sikorski

import numpy as np
from typing import Tuple

def redukcja_macierzy(A: np.ndarray, verbose: bool = False) -> float:
    """
    Redukcja macierzy in-place (krok 1)

    :param A: Macierz przejść do redukcji, jest redukowana in-place.
    :type A: np.ndarray
    :param verbose: Dodatkowe wyświetlanie danych (debug).
    :type verbose: bool

    :returns: Wartość redukcji.
    :rtype: float
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


def optymistyczny_odcinek(A: np.ndarray) -> Tuple[int, int]:
    """
    Wyszukiwanie odcinka o max koszcie wyłączenia (krok 2)

    :param A: Macierz przejść, zredukowana wcześniej.
    :type A: np.ndarray
    
    :returns: Indeksy wierzchołków najlepszego odcinka do wyłączenia.
    :rtype: Tuple[int, int]
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
