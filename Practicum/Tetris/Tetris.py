from Piece import *


class Tetris:

    def __init__(self):
        self.window = Tk()
        self.window.title('Tetris')
        self.window.bind("<Key>", self.controls)
        self.board = Board(self.window)
        self.pause = False
        self.score = 0
        self.status = True
        self.speed = 300
        self.create_menu()
        self.start()

    # создание верхнего меню
    def create_menu(self):
        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)
        self.menu_play = Menu(self.menu, tearoff=0)
        self.menu.add_command(label="Пауза", command=self.set_pause)
        self.menu_level = Menu(self.menu, tearoff=0)
        self.menu_level.add_radiobutton(label="Лёгкий", command=self.set_level1)
        self.menu_level.add_radiobutton(label="Средний", command=self.set_level2)
        self.menu_level.add_radiobutton(label="Сложный", command=self.set_level3)
        self.menu.add_cascade(label="Уровень", menu=self.menu_level)
        self.menu.add_command(label="Справка", command=self.show_rules)

    # создание нового элемента
    def create_piece(self):
        self.piece = Piece(self.board)
        self.board.canvas.update()

    # начало игры
    def start(self):
        self.score = 0
        self.speed = 300
        self.status = True
        self.pause = False
        self.board.clear()
        try:
            self.play_again_btn.destroy()
            self.quit_btn.destroy()
            self.end_pause_btn.destroy()
        except AttributeError:
            pass
        self.create_piece()
        self.window.after(self.speed, self.drop())
        self.window.mainloop()

    # спуск фигуры
    def drop(self):
        if not self.pause:
            if not self.piece.move((0, 1)):
                for cell in self.piece.cells:
                    coord = self.board.canvas.coords(cell)
                    px = int((coord[0] - Board.INDENT) // Board.CELL_WIDTH)
                    py = int((coord[1] - Board.INDENT) // Board.CELL_WIDTH)
                    self.board.table[py][px] = 1
                self.completed_lines()
                self.update_score()
                self.create_piece()
                if not self.piece.cells:
                    self.__over()
                    return
                if self.is_over():
                    return
            self.window.after(self.speed, self.drop)
        else:
            try:
                self.info_window.protocol("WM_DELETE_WINDOW", self.close)
            except(TclError, AttributeError):
                self.end_pause_btn = Button(self.window, text="Continue", command=self.end_pause, bg="#FFFFE0")
                width = Board.CELL_WIDTH * int(Board.CELL_COUNT_W // 2)
                self.end_pause_btn.place(x=Board.WIDTH // 2 - width // 2, y=Board.HEIGHT // 2 - 30, width=width,
                                         height=30)

    # полный спуск фигуры
    def hard_drop(self):
        self.piece.move((0, self.piece.max_movement))

    # удаление полных линий и подсчёт очков
    def completed_lines(self):
        completed_line = self.board.completed_lines()
        if completed_line >= 1:
            self.score += completed_line * 100
            self.speed = self.speed - (self.score // 500) * 10

    # конец игры и выбор дальнейших действий
    def __over(self):
        self.status = False
        self.play_again_btn = Button(self.window, text="Play Again", command=self.start, bg="#FFFFE0")
        self.quit_btn = Button(self.window, text="Quit", command=self.quit, bg="#FFFFE0")
        width = Board.CELL_WIDTH * int(Board.CELL_COUNT_W // 2)
        self.play_again_btn.place(x=Board.WIDTH // 2 - width // 2, y=Board.HEIGHT // 2 - 40, width=width, height=30)
        self.quit_btn.place(x=Board.WIDTH // 2 - width // 2, y=Board.HEIGHT // 2, width=width, height=30)

    # проверка конца игры
    def is_over(self):
        if not self.piece.move((0, 1)):
            self.__over()
            return True
        return False

    # выход из игры
    def quit(self):
        self.window.quit()

    # пауза
    def set_pause(self):
        self.pause = True
        self.status = False

    # продолжение игры после паузы
    def end_pause(self):
        try:
            self.end_pause_btn.destroy()
        except AttributeError:
            pass
        self.pause = False
        self.status = True
        self.drop()

    # закрытие окна справки
    def close(self):
        self.info_window.destroy()
        self.pause = False
        self.status = True
        self.drop()

    # обновление строки очков
    def update_score(self):
        self.board.update_score(self.score)

    # установка скорости в соответствии с уровнем сложности
    def set_level1(self):
        self.speed = 300

    def set_level2(self):
        self.speed = 200

    def set_level3(self):
        self.speed = 100

    # вызов окна справки
    def show_rules(self):
        self.pause = True
        self.info_window = Toplevel(self.window, bd=10, bg="white")
        self.info_window.title("Справка")
        self.info_window.minsize(width=300, height=150)
        lab = Label(self.info_window, text="Управление осуществляется 4 кнопками:\n"
                                           "LEFT(<-) - движение влево, \n"
                                           "RIGHT(->) - движение вправо, \n"
                                           "UP(^) - поворот на 90 градусов против часовой стрелки, \n"
                                           "DOWN - быстрое падение ", font="Arial 12", bg="white", justify=LEFT)
        lab.pack()
        self.info_window.grab_set()

    # управление игрой
    def controls(self, key):
        if self.status:
            if key.keysym == "Left":
                self.piece.move((-1, 0))
            elif key.keysym == "Right":
                self.piece.move((1, 0))
            elif key.keysym == "Down":
                self.hard_drop()
            elif key.keysym == "Up":
                self.piece.rotate()
