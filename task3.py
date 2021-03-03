from tkinter import Tk, Frame, LabelFrame, Canvas, TOP, LEFT, Scale, HORIZONTAL
from tkinter import Button, NO, LAST, END, N, Label, W
from tkinter.ttk import Treeview
import numpy as np
import sys
from math import sqrt


def draw_beam(canv):
    global a, x_fin, y_fin, press_x, press_y, x_cross, y_cross
    xc, yc = 30, 115
    if y_fin == 0:
        return
    if y_fin != press_y:
        b1 = (x_fin - press_x) / (y_fin - press_y)
        b2 = press_x - press_y * (x_fin - press_x) / (y_fin - press_y)

        b = 2 * a * yc + b1
        c = a * yc ** 2 + xc - b2

        D = b ** 2 - 4 * a * c
        if y_fin < press_y:
            y_root1 = (b - sqrt(D)) / (2 * a)
        else:
            y_root1 = (b + sqrt(D)) / (2 * a)

        if y_root1 < 16:
            y_root1 = 0
        elif y_root1 > 215:
            y_root1 = 230

        x0 = b1 * y_root1 + b2
    else:
        y_root1 = y_fin
        if (y_root1 < 16) | (y_root1 > 215):
            x0 = 0
        else:
            x0 = a * (y_root1 - yc) ** 2 + xc

    canv.create_line([x_fin, y_fin, x0, y_root1], width=1, fill='yellow')
    x_cross, y_cross = int(x0), int(y_root1)
    if (y_root1 > 15) & (y_root1 < 216):
        draw_mirrored(canv, x0, y_root1)
    update_treeview()


def draw_mirrored(c, x0, y0):
    """
    рисует отражение, если луч попал в зеркало
    :param x0: x-координата пересечения луча с зеркалом
    :param y0: y-координата пересечения луча с зеркалом
    :return: None
    """
    xc, yc = 30, 115

    # уравнение нормали
    x = lambda y: a * (y - yc) ** 2 + xc
    x_der = lambda y: 2 * a * (y - yc)
    x_norm = lambda y: x(y0) - 1 / x_der(y0) * (y - y0)

    k = 50 / sqrt((10)**2 + (x_norm(y0 + 10) - x0)**2)

    # отрисовка вектора нормали к зеркалу
    c.create_line([x0, y0, x_norm(y0 + np.sign(yc - y0) * 10 * k), y0 + np.sign(yc - y0) * 10 * k],
                  width=1, fill='green', arrow=LAST)

    # расчет вектора нормали
    yN = np.sign(yc - y0) * 10 * k
    xN = x_norm(y0 + np.sign(yc - y0) * 10 * k) - x0
    lN = sqrt(xN**2 + yN**2)
    yN = yN / lN
    xN = xN / lN

    xV = x_fin - press_x
    yV = y_fin - press_y

    N = np.array([xN, yN])
    V = np.array([xV, yV])

    v = np.dot(V, N)
    M = V - 2 * v * N

    x1 = x0 + 0.5 * M[0]
    y1 = y0 + 0.5 * M[1]

    c.create_line([x0, y0, x1, y1], width=2, fill='magenta')


def redraw(event, c, setarrow=False):
    """
    перерисовка изображения на canvas
    :param event:
    :param c:
    :param setarrow:
    :return:
    """
    global a, arrow_state, press_y, press_x, temp_y, temp_x, x_fin, y_fin
    if setarrow:
        arrow_state = False
        press_x, press_y = 0, 0
        temp_x, temp_y = 0, 0
        x_fin, y_fin = 0, 0
    if event:
        a = event.widget.get()
    c.delete("all")
    if arrow_state:
        c.create_line([press_x, press_y, x_fin, y_fin], width=2, fill='blue', arrow=LAST)
        draw_beam(c)
    update_treeview()


def press(event):
    """
    Обработчкик события "нажатие кнопки мыши"
    :param event:
    :return:
    """
    global temp_x, temp_y
    if event.widget.master is not None:
        if event.widget.widgetName == 'canvas':
            temp_x, temp_y = event.x, event.y


def release(event, c):
    """
    обработчик события "отпускание кнопки мыши"
    :param event:
    :param c:
    :return:
    """
    global x_fin, y_fin, arrow_state, mirror_border, temp_x, temp_y, press_x, press_y
    if event.widget.master is not None:
        if event.widget.widgetName == 'canvas':
            if (event.x > mirror_border) & (event.x < temp_x):
                x_fin, y_fin = event.x, event.y
                press_x, press_y = temp_x, temp_y
                c.delete('all')
                arrow_state = True
                c.create_line([press_x, press_y, x_fin, y_fin], width=2, fill='blue', arrow=LAST)
                draw_beam(c)

def update_treeview():
    """
    запись параметров в элемент Treeview
    :return: None
    """
    global params
    for x in params.get_children():
        params.delete(x)
    if (press_x != 0) & (press_y != 0):
        params.insert("", END, values=['(x1, y1)', '(' + str(press_x) + ', ' + str(press_y) + ')'])
        params.insert("", END, values=['(x2, y2)', '(' + str(x_fin) + ', ' + str(y_fin) + ')'])
        params.insert("", END, values=['(x_cross, y_cross)', '(' + str(int(x_cross)) + ', ' + str(int(y_cross)) + ')'])


class Math:

    def __init__(self, xc, yc):
        self.mirror_x = xc
        self.mirror_y = yc

    def mirror(self, a, phi):
        """
        Расчет координат параболы, изображающей зеркало
        :param a: кривизна параболы (к-т уравнения при x^2)
        :param phi: угол наклона параболы
        :return: список координат параболы для отображения, правую x-координату параболического зеркала
        """
        xc, yc = self.mirror_x, self.mirror_y
        phi = phi / 180 * 3.1415
        y1 = np.ones(180)
        y1 = y1.cumsum() - 90 + yc
        x1 = a * (y1 - yc) ** 2 + xc

        x2 = (x1 - self.mirror_x) * np.cos(phi) + (y1 - self.mirror_y) * np.sin(phi) + self.mirror_x
        y2 = -1 * (x1 - self.mirror_x) * np.sin(phi) + (y1 - self.mirror_y) * np.cos(phi) + self.mirror_y

        mirror_border = max(x2)

        c1 = np.empty(len(y2) * 2)
        c1[0::2], c1[1::2] = x2, y2
        c1 = c1.astype(int).copy()

        return c1, mirror_border


class App:

    def __init__(self, canvas_y):
        # инициализация переменных
        self.mirror_border = 0
        self.press_x, self.press_y = 0, 0
        self.temp_x, self.temp_y = 0, 0
        self.x_fin, self.y_fin = 0, 0
        self.x_cross, self.y_cross = 0, 0
        self.canvas_height = canvas_y
        self.x_center, self.y_center = 100, int(self.canvas_height / 2)

        self.math = Math(self.x_center, self.y_center)
        self.mirror_border = 0

        # arrow_state = False
        # a = 0.002
        # params = None

        window = Tk()
        window.title("Отражение в параболическом зеркале")
        window.geometry('600x'+str(self.canvas_height + 250))
        window.minsize(600, self.canvas_height + 250)
        window.maxsize(600, self.canvas_height + 250)
        canv = Frame(window)
        setup = LabelFrame(window, text='   Настройки   ', width=450, height=150)
        self.c = Canvas(canv, width=550, height=self.canvas_height, bg='black')
        self.c.pack(side=TOP, padx=10)

        setup1 = Frame(setup)
        setup2 = Frame(setup)
        butFrame = Frame(setup2)

        Label(setup1, text='Форма зеркала').pack(side=TOP, padx=(10, 0), anchor=W)
        self.scal = Scale(setup1, orient=HORIZONTAL, length=300, from_=0, to=0.015, tickinterval=0.005, resolution=0.001)
        self.scal.set(0.002)
        self.scal.pack(side=TOP, pady=(0, 10), padx=(10, 10))
        self.scal.bind("<ButtonRelease-1>", self.redraw)

        Label(setup1, text='Наклон зеркала').pack(side=TOP, padx=(10, 0), anchor=W)
        self.angle = Scale(setup1, orient=HORIZONTAL, length=300, from_=-45, to=45, tickinterval=15, resolution=15)
        self.angle.set(0)
        self.angle.pack(side=TOP, pady=(0, 10), padx=(10, 10))
        self.angle.bind("<ButtonRelease-1>", self.redraw)

        Button(butFrame, text='Очистить', width=12,
               command=lambda event=None, draw_canv=self.c, flag=True: redraw(event, draw_canv,
                                                                         setarrow=flag)) \
            .pack(side=LEFT, padx=(10, 5), pady=(5, 10))
        Button(butFrame, text='Закрыть', width=12, command=lambda flag=0: sys.exit(flag)).pack(side=LEFT, padx=(5, 10),
                                                                                               pady=(5, 10))
        columns = ('#1', '#2')
        params = Treeview(setup2, show='headings', columns=columns, height=5)
        params.heading('#1', text='Параметр')
        params.heading('#2', text='Значение')
        params.column('#1', width=100, minwidth=50, stretch=NO, anchor=N)
        params.column('#2', width=100, minwidth=50, stretch=NO, anchor=N)
        params.pack(side=TOP, padx=(5, 10), pady=(0, 10))

        butFrame.pack(side=TOP)

        setup1.pack(side=LEFT)
        setup2.pack(side=LEFT)

        canv.pack(side=TOP, pady=(10, 10))
        setup.pack(side=TOP, pady=(0, 10), padx=(25, 25))

        window.bind('<Button-1>', press)
        window.bind('<ButtonRelease-1>', lambda event, draw_canv=self.c: release(event, draw_canv))
        self.draw_mirror()
        window.mainloop()

    def redraw(self, event):
        self.c.delete('all')
        self.draw_mirror()

    def draw_mirror(self):
        c1, self.mirror_border = self.math.mirror(self.scal.get(), self.angle.get())
        self.c.create_line(list(c1), width=3, fill='red')

        # отображение центра зеркала
        self.c.create_oval(self.x_center, self.y_center, self.x_center - 5, self.y_center-5, fill='green')



def main():
    app = App(350)


if __name__ == '__main__':
    main()
