import random
import math
from tkinter import *

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH // 2
CANVAS_CENTER_Y = CANVAS_HEIGHT // 2
IMAGE_ENLARGE = 11
HEART_COLOR = "#ff2190"

class Heart:
    def __init__(self):
        self.original_heart_coordinates = set()
        self.edge_expansion_coordinates = set()
        self.center_expansion_coordinates = set()

    def heart_function(self, t, shrink_ratio=IMAGE_ENLARGE):
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        return int(x * shrink_ratio + CANVAS_CENTER_X), int(y * shrink_ratio + CANVAS_CENTER_Y)

    def scatter_inside(self, x, y, beta=0.15):
        ratio_x = -beta * math.log(random.random())
        ratio_y = -beta * math.log(random.random())
        x0, y0 = self.heart_function(t=random.uniform(0, 2 * math.pi))
        return int((x0 + (x - x0) * ratio_x)), int((y0 + (y - y0) * ratio_y))

    def shrink(self, x, y, ratio):
        x0, y0 = self.heart_function(t=random.uniform(0, 2 * math.pi))
        return int((x - x0) * ratio), int((y - y0) * ratio)

    def build(self, number=2000):
        for _ in range(number):
            t = random.uniform(0, 2 * math.pi)
            x, y = self.heart_function(t)
            self.original_heart_coordinates.add((x, y))
            for _ in range(3):
                x, y = self.scatter_inside(x, y)
                self.edge_expansion_coordinates.add((x, y))

    def calc_position(self, x, y, ratio):
        force = 1 / ((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6
        dx = ratio * force * (x - CANVAS_CENTER_X)
        dy = ratio * force * (y - CANVAS_CENTER_Y)
        return x - dx, y - dy

    @staticmethod
    def calc_position_static(x, y, ratio):
        return Heart.calc_position(x, y, ratio)

    def render(self, render_canvas, render_frame):
        render_canvas.delete('all')
        for x, y in self.original_heart_coordinates:
            x, y = self.calc_position_static(x, y, 11.6)
            size = random.randint(1, 3)
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)
        # 继续添加其他效果...

class HeartInterface:
    def __init__(self):
        self.heart_instance = Heart()

    def draw(self, main, render_canvas, render_frame):
        render_canvas.delete('all')
        self.heart_instance.render(render_canvas, render_frame)
        main.after(160, self.draw, main, render_canvas, render_frame + 1)

if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart_interface_instance = HeartInterface()
    heart_interface_instance.draw(root, canvas, 0)
    root.mainloop()
