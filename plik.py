#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

def analiza_PP(matrix, LB_matrix, LB):

    if LB_matrix > LB:
        #KZ2
        pass

    ind_zeros = []
    dep_zeros = []
    size, _ = matrix.shape

    for number in range(1, size + 1):
        for idx, row in enumerate(matrix):
            if row.count(0) == number:
                added = False
                for idy, col in enumerate(row):
                    if col == 0 and not added and idy not in [el[1] for el in ind_zeros]:
                        another_zero_in_col = False
                        for row_in_col in range(size):
                            if matrix[row_in_col, idy] == 0 and row_in_col != row:
                                another_zero_in_col = True
                        if not another_zero_in_col:
                            added = True
                            ind_zeros.append((idx, idy))
                if not added:
                    for idy, col in enumerate(row):
                        if col == 0 and idy not in [el[1] for el in ind_zeros]:
                            ind_zeros.append((idx, idy))
                            break
    for row in range(size):
        for col in range(size):
            if matrix[row, col] == 0 and (row, col) not in ind_zeros:
                dep_zeros.append((row, col))

    if len(ind_zeros) == size:
        first = ind_zeros[0][0]
        V = ind_zeros[0][1]
        nb = 0
        while V != first:
            if nb > size:
                #Przerwanie, nie znaleziono całego jednego cyklu -> potrzebny kolejny podział
                if

            nb += 1
            if