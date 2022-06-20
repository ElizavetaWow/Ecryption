import copy


class Figure:
    SHAPE = ([(0, 0), (1, 0), (0, 1), (1, 1)],  # Square
             [(0, 0), (1, 0), (2, 0), (3, 0)],  # Line
             [(2, 0), (0, 1), (1, 1), (2, 1)],  # Right L
             [(0, 0), (0, 1), (1, 1), (2, 1)],  # Left L
             [(0, 1), (1, 1), (1, 0), (2, 0)],  # Right Z
             [(0, 0), (1, 0), (1, 1), (2, 1)],  # Left Z
             [(1, 0), (0, 1), (1, 1), (2, 1)])  # T

    def __init__(self, shape):
        self.coords = self.SHAPE[shape]

    # координаты при повороте на 90 градусов против часовой стрелки
    def _rotate(self):
        rotated = copy.deepcopy(self.coords)
        for i in range(4):
            rotated[i] = (-rotated[i][1], rotated[i][0])
        min_x = min(rotated, key=lambda x: x[0])[0]
        min_y = min(rotated, key=lambda x: x[1])[1]
        return [(rotated[i][0] - min_x, rotated[i][1] - min_y) for i in range(4)]

    # поворот фигуры
    def rotate(self):
        self.coords = self._rotate()

    # представление фигуры в виде матрицы
    @property
    def matrix(self):
        mtx = []
        for i in range(4):
            mtx.append([])
            for j in range(4):
                mtx[i].append([])
                if (i, j) in self.coords:
                    mtx[i][j] = 1
                else:
                    mtx[i][j] = 0
        return mtx
