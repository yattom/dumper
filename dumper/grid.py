import Tkinter
import threading
import time

class Grid(object):
    class Dim:
        def __init__(self, width, height):
            self.width = width
            self.height = height

    def __init__(self, dim=(10, 10), wait=0):
        self.canvas = Tkinter.Canvas(width=500, height=500)
        self.canvas.pack()
        self.dim = Grid.Dim(*dim)
        self.wait = wait
        self.draw_gridlines()
        self.create_texts()

        def run():
            self.canvas.mainloop()

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def draw_gridlines(self):
        for col in range(self.dim.width + 1):
            self.canvas.create_line(col * 460 / self.dim.width + 20, 20, col * 460 / self.dim.width + 20, 480, fill='black')
        for row in range(self.dim.height + 1):
            self.canvas.create_line(20, row * 460 / self.dim.height + 20, 480, row * 460 / self.dim.height + 20, fill='black')

    def create_texts(self):
        self.text_ids = {}
        for col in range(self.dim.width):
            for row in range(self.dim.height):
                self.text_ids[(col, row)] = self.canvas.create_text(col * 460 / self.dim.width + 20 + (460 / 2) / self.dim.width, row * 460 / self.dim.height + 20 + (460 / 2) / self.dim.height, text='')

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

if __name__=='__main__':
    g=Grid(dim=(15, 10))
    for i in range(100):
        s = ''.join([str(n % 10) for n in range(i, i + 100)])
        g.dump_cluster([s[i:i+10] for i in range(0, 100, 10)])
