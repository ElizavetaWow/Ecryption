from tkinter import *


class Board:
    CELL_WIDTH = 20
    INDENT = 20
    CELL_COUNT_W = 13
    CELL_COUNT_H = 20
    WIDTH = CELL_WIDTH * CELL_COUNT_W + INDENT * 2
    HEIGHT = CELL_WIDTH * CELL_COUNT_H + INDENT * 2
    START_POINT = CELL_WIDTH * int(CELL_COUNT_W // 2) + INDENT

    def __init__(self, window):
        self.canvas = Canvas(window, width=self.WIDTH, height=self.HEIGHT, bg="white")
        self.canvas.pack()
        self.status_var = StringVar()
        self.status = Label(window, textvariable=self.status_var)
        self.status.pack(side=BOTTOM)
        self.update_score(0)
        self.table = []
        for i in range(self.CELL_COUNT_H):
            self.table.append([])
            for j in range(self.CELL_COUNT_W):
                self.table[i].append([])
                self.table[i][j] = 0

    # обновление очков
    def update_score(self, score):
        self.status_var.set(f"Score: {score}")

    # очистка доски и отрисовка линий сетки
    def clear(self):
        self.canvas.delete("all")
        self.table = []
        for i in range(self.CELL_COUNT_H):
            self.table.append([])
            y = i * self.CELL_WIDTH + self.INDENT
            self.canvas.create_line(self.INDENT, y, self.WIDTH - self.INDENT, y, fill='#B5B5B5')
            for j in range(self.CELL_COUNT_W):
                self.table[i].append([])
                self.table[i][j] = 0
                x = j * self.CELL_WIDTH + self.INDENT
                self.canvas.create_line(x, self.INDENT, x, self.HEIGHT - self.INDENT, fill='#B5B5B5')
        x = self.CELL_COUNT_W * self.CELL_WIDTH + self.INDENT
        self.canvas.create_line(x, self.INDENT, x, self.HEIGHT - self.INDENT, fill='#B5B5B5')
        y = self.CELL_COUNT_H * self.CELL_WIDTH + self.INDENT
        self.canvas.create_line(self.INDENT, y, self.WIDTH - self.INDENT, y, fill='#B5B5B5')
        y = self.CELL_WIDTH + self.INDENT
        self.canvas.create_line(self.INDENT, y, self.WIDTH - self.INDENT, y, fill='red')

    # удаление заполненных линий
    def completed_lines(self):
        cleaned_lines = 0
        flag = 1
        while flag != 0:
            flag = 0
            for i in range(self.CELL_COUNT_H):
                if sum(self.table[i]) == Board.CELL_COUNT_W:
                    flag += 1
                    y = i * Board.CELL_WIDTH + Board.INDENT
                    self.clean_line(
                        [cell for cell in self.canvas.find_withtag('cell') if self.canvas.coords(cell)[1] == y])
                    self.drop_cells(
                        [cell for cell in self.canvas.find_withtag('cell') if self.canvas.coords(cell)[1] < y])
                    self.drop_table(i)
                    cleaned_lines += 1
        return cleaned_lines

    # удаление блоков
    def clean_line(self, cells):
        for cell in cells:
            self.canvas.delete(cell)

    # спуск блоков на линию вниз
    def drop_cells(self, cells):
        for cell in cells:
            self.canvas.move(cell, 0, Board.CELL_WIDTH)

    # обновление таблицы доски
    def drop_table(self, y):
        for i in range(y, 0, -1):
            for j in range(self.CELL_COUNT_W):
                self.table[i][j] = self.table[i - 1][j]
        for i in range(self.CELL_COUNT_W):
            self.table[0][i] = 0
