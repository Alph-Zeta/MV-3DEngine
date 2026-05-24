import tkinter as tk
import math

WIDTH, HEIGHT = 1366, 768
GRID_SIZE = 10


def f(x, y):
    return math.cos(x) * math.sin(y)

def rotate(x, y, z, ax, ay):
    # rotate around x axis
    cosx, sinx = math.cos(ax), math.sin(ax)
    y, z = y * cosx - z * sinx, y * sinx + z * cosx

    # rotate around y axis
    cosy, siny = math.cos(ay), math.sin(ay)
    x, z = x * cosy + z * siny, -x * siny + z * cosy

    return x, y, z

def project(x, y, z, zoom, offset_x, offset_y):
    distance = 5
    factor = zoom / (z + distance)
    sx = x * factor + offset_x
    sy = y * factor + offset_y
    return sx, sy

class App:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.ax = 0
        self.ay = 0
        self.zoom = 200

        self.dragging = False
        self.last_x = 0
        self.last_y = 0

        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<MouseWheel>", self.zoom_event)

        self.draw()

    def start_drag(self, event):
        self.dragging = True
        self.last_x = event.x
        self.last_y = event.y


    def drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.ax += dy * 0.008
        self.ay += dx * 0.008
        self.last_x = event.x
        self.last_y = event.y
        self.draw()


    # zoom
    def zoom_event(self, event):
        if event.delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom *= 0.9
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        step = 0.3 # scale 
        points = []


        # generate surface
        for i in range(-GRID_SIZE, GRID_SIZE):
            row = []
            for j in range(-GRID_SIZE, GRID_SIZE):
                x = i * step
                y = j * step
                z = f(x, y)

                # rotate
                rx, ry, rz = rotate(x, y, z, self.ax, self.ay)

                # project
                sx, sy = project(
                    rx, ry, rz,
                    self.zoom,
                    WIDTH // 2,
                    HEIGHT //2
                )

                row.append((sx, sy))
            points.append(row)


        # draw mesh
        for i in range(len(points) - 1):
            for j in range(len(points[i]) - 1):
                x1, y1 = points[i][j]
                x2, y2 = points[i + 1][j]
                x3, y3 = points[i][j + 1]

                self.canvas.create_line(x1, y1, x2, y2, fill="cyan")
                self.canvas.create_line(x1, y1, x3, y3, fill="cyan")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("3D multivariable function")
    App(root)
    root.mainloop()


