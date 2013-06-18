import Tkinter
import threading
import time

class Grid(object):
    WIDTH = 500
    HEIGHT = 500
    RIM_SIZE = 20

    class Dim:
        def __init__(self, width, height):
            self.width = width
            self.height = height

    def __init__(self, dim=(10, 10), wait=0):
        initialized = threading.Condition()
        initialized.acquire()
        def run():
            self.canvas = Tkinter.Canvas(width=Grid.WIDTH, height=Grid.HEIGHT)
            self.canvas.pack()
            self.dim = Grid.Dim(*dim)
            self.wait = wait
            self.draw_gridlines()
            self.create_texts()

            initialized.acquire()
            initialized.notifyAll()
            initialized.release()
            self.canvas.mainloop()

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        initialized.wait()
        initialized.release()

    def cell_width(self):
        return float(Grid.WIDTH - Grid.RIM_SIZE * 2) / self.dim.width

    def cell_height(self):
        return float(Grid.HEIGHT - Grid.RIM_SIZE * 2) / self.dim.height

    def cell_left(self, row, col):
        return col * self.cell_width() + Grid.RIM_SIZE

    def cell_top(self, row, col):
        return row * self.cell_height() + Grid.RIM_SIZE

    def draw_gridlines(self):
        for col in range(self.dim.width + 1):
            self.canvas.create_line(self.cell_left(row, col), Grid.RIM_SIZE, self.cell_left(row, col), Grid.WIDTH - Grid.RIM_SIZE, fill='black')
        for row in range(self.dim.height + 1):
            self.canvas.create_line(Grid.RIM_SIZE, self.cell_top(row, col), Grid.HEIGHT - Grid.RIM_SIZE, self.cell_top(row, col), fill='black')

    def create_texts(self):
        self.text_ids = {}
        for col in range(self.dim.width):
            for row in range(self.dim.height):
                self.text_ids[(col, row)] = self.canvas.create_text(self.cell_left(row, col) + self.cell_width() / 2, self.cell_top(row, col) + self.cell_height() / 2, text='')

    def draw_text(self, col, row, text, color='blue'):
        id = self.text_ids.get((col, row), -1)
        if id == -1: return
        self.canvas.dchars(id, 0, 100)
        self.canvas.itemconfig(id, fill=color)
        self.canvas.insert(id, 0, text)

    def dump(self, cluster=None):
        if cluster:
            self.dump_cluster(cluster)
        self.canvas.update_idletasks()
        if self.wait: time.sleep(self.wait)

    def dump_cluster(self, text):
        if isinstance(text, str):
            lines = text.split('\n')
        elif isinstance(text, list):
            lines = text
        else: raise ValueError()

        for row, l in enumerate(lines):
            for col, c in enumerate(l):
                self.draw_text(col, row, c)


def odd(n):
    return n % 2 != 0

import math
class Hex(Grid):
    def cell_left(self, row, col):
        if odd(row):
            return col * self.cell_width() + Grid.RIM_SIZE
        else:
            return col * self.cell_width() + self.cell_width() / 2 + Grid.RIM_SIZE

    def draw_gridlines(self):
        self.cells = {}
        for col in range(self.dim.width):
            for row in range(self.dim.height):
                self.cells[(row, col)] = self.draw_cell(row, col)

    def draw_cell(self, row, col):
        x = self.cell_left(row, col)
        y = self.cell_top(row, col) - self.cell_height() * 0.125
        w = self.cell_width()
        h = self.cell_height() * 1.25 + 2
        self.canvas.create_polygon(
            x + w / 2, y,
            x + w,     y + h / 4,
            x + w,     y + h * 3 / 4,
            x + w / 2, y + h,
            x,         y + h * 3 / 4,
            x,         y + h / 4,
            outline='black',
            fill='#c0ffd0')


if __name__=='__main__':
    g=Hex(dim=(8, 10))
    for i in range(100):
        s = ''.join([str(n % 10) for n in range(i, i + 100)])
        g.dump_cluster([s[i:i+10] for i in range(0, 100, 10)])
    raw_input()
