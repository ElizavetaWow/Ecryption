from Figure import *
from Board import *
import random


class Piece:
    COLORS = ["red", "green", "blue", "yellow", "pink"]

    def __init__(self, board, shape=None):
        if not shape:
            shape = random.randint(0, 6)
        self.figure = Figure(shape)
        self.board = board
        self.color = random.choice(self.COLORS)
        self.cells = self.draw_cells((Board.START_POINT, Board.INDENT))

    # создание блоков фигуры
    def draw_cells(self, point):
        cells = []
        flag = True
        for coord in self.figure.coords:
            flag *= self.can_move((coord[0] * Board.CELL_WIDTH + point[0], coord[1] * Board.CELL_WIDTH + point[1]),
                                  (0, 1))
        if flag:
            for coord in self.figure.coords:
                cell = self.board.canvas.create_rectangle(coord[0] * Board.CELL_WIDTH + point[0],
                                                          coord[1] * Board.CELL_WIDTH + point[1],
                                                          coord[0] * Board.CELL_WIDTH + point[0] + Board.CELL_WIDTH,
                                                          coord[1] * Board.CELL_WIDTH + point[1] + Board.CELL_WIDTH,
                                                          fill=self.color, tags="cell", outline="#1C1C1C")
                cells += [cell]
        return cells

    # проверка возможности двигаться в напрвлении direction
    def can_move(self, coord, direction):
        px = int((coord[0] - Board.INDENT) // Board.CELL_WIDTH)
        py = int((coord[1] - Board.INDENT) // Board.CELL_WIDTH)
        nx, ny = px + direction[0], py + direction[1]
        if ny >= Board.CELL_COUNT_H or ny < 0 or nx < 0 or nx >= Board.CELL_COUNT_W:
            return False
        elif self.board.table[ny][nx] != 0:
            return False
        return True

    # движение фигуры в напрвлении direction, если есть возможность
    def move(self, direction):
        flag = True
        for cell in self.cells:
            flag *= self.can_move(self.board.canvas.coords(cell), direction)
        if flag:
            for cell in self.cells:
                self.board.canvas.move(cell, direction[0] * Board.CELL_WIDTH, direction[1] * Board.CELL_WIDTH)
            return True
        return False

    # поворот фигуры
    def rotate(self):
        rotated = self.figure._rotate()
        direction = []
        for i in range(4):
            direction.append((rotated[i][0] - self.figure.coords[i][0], rotated[i][1] - self.figure.coords[i][1]))
        flag = True
        for i in range(4):
            flag *= self.can_move(self.board.canvas.coords(self.cells[i]), direction[i])
        if flag:
            self.figure.rotate()
            for i in range(4):
                cell = self.cells[i]
                self.board.canvas.move(cell, direction[i][0] * Board.CELL_WIDTH, direction[i][1] * Board.CELL_WIDTH)

    # максимальное количество строк, на которое может передвинуться фигура
    @property
    def max_movement(self):
        levels = []
        for i in range(4):
            x, y, _, _ = self.board.canvas.coords(self.cells[i])
            flag = True
            levels.append(0)
            while flag:
                levels[i] += 1
                y += Board.CELL_WIDTH
                flag = self.can_move((x, y), (0, 1))
        return min(levels)
