#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from multiprocessing import Process, Queue

MTX1 = './files/mtx1.txt'
MTX2 = './files/mtx2.txt'
MTX_RES = './files/mtx_res.txt'


def read_mtx(file):
    with open(file, 'r') as f:
        matrix = list()
        for line in f.readlines():
            matrix.append([int(el) for el in line.strip().split(" ")])
    return matrix


def list_to_line(lst):
    line = ""
    for el in lst:
        for k in el:
            line += str(k) + " "
        line += "\n"
    return line


def write_mtx(mtx, file='./files/mtx_res.txt'):
    with open(file, 'w') as f:
        f.write(list_to_line(mtx))


def generate_mtx(n, m):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(random.randint(1, 100))
    return matrix


def start():
    matrix1 = read_mtx(MTX1)
    matrix2 = read_mtx(MTX2)
    if (len(matrix1) == 0) and (len(matrix2) == 0):
        n = int(input("Введите кол-во строк в матрице : "))
        m = int(input("Введите кол-во столбцов в матрице : "))
        if n > 1 and m > 1:
            write_mtx(generate_mtx(n, m), MTX1)
            write_mtx(generate_mtx(m, n), MTX2)
    elif len(matrix1) == 0:
        write_mtx(generate_mtx(len(matrix2[0]), len(matrix2)), MTX1)
    elif len(matrix2) == 0:
        write_mtx(generate_mtx(len(matrix1[0]), len(matrix1)), MTX2)
    with open(MTX_RES, 'w') as f:
        f.write("")


def element(index, a, b, queue):
    i, j = index
    res = 0
    n = len(a[0]) or len(b)
    for k in range(n):
        res += a[i][k] * b[k][j]
    queue.put(res)
    return res


def print_mtx(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end=" ")
        print("")
    if len(matrix) > 0:
        print("Размер матрицы", len(matrix), "*", len(matrix[0]))


if __name__ == '__main__':
    print("Загрузка матриц из файлов")
    start()
    matrix1 = read_mtx(MTX1)
    matrix2 = read_mtx(MTX2)
    print_mtx(matrix1)
    print_mtx(matrix2)

    q = Queue()
    d = min(len(matrix1), len(matrix2))
    res_matrix = list()
    for i in range(d):
        for j in range(d):
            p = Process(target=element, args=((i, j), matrix1, matrix2, q))
            p.start()
            p.join()
            with open(MTX_RES, 'a') as f:
                f.write(str(q.get()) + " ")
        with open(MTX_RES, 'a') as f:
            f.write("\n")
    print("Выполнено")
    q.close()
    q.join_thread()
