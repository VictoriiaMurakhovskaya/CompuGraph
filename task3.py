from tkinter import Tk, Frame, LabelFrame, Canvas, TOP, LEFT, Scale, HORIZONTAL
from tkinter import Button, NO, LAST, END, N, Label, W
from tkinter.ttk import Treeview
import numpy as np
import sys
from itertools import product
from math import sqrt


def draw_mirrored(c, x0, y0):
    """
    рисует отражение, если луч попал в зеркало
    :param x0: x-координата пересечения луча с зеркалом
    :param y0: y-координата пересечения луча с зеркалом
    :return: None
    """
    pass
    # xc, yc = 30, 115
    #
    # # уравнение нормали
    # x = lambda y: a * (y - yc) ** 2 + xc
    # x_der = lambda y: 2 * a * (y - yc)
    # x_norm = lambda y: x(y0) - 1 / x_der(y0) * (y - y0)
    #
    # k = 50 / sqrt((10)**2 + (x_norm(y0 + 10) - x0)**2)
    #
    # # отрисовка вектора нормали к зеркалу
    # c.create_line([x0, y0, x_norm(y0 + np.sign(yc - y0) * 10 * k), y0 + np.sign(yc - y0) * 10 * k],
    #               width=1, fill='green', arrow=LAST)
    #
    # # расчет вектора нормали
    # yN = np.sign(yc - y0) * 10 * k
    # xN = x_norm(y0 + np.sign(yc - y0) * 10 * k) - x0
    # lN = sqrt(xN**2 + yN**2)
    # yN = yN / lN
    # xN = xN / lN
    #
    # xV = x_fin - press_x
    # yV = y_fin - press_y
    #
    # N = np.array([xN, yN])
    # V = np.array([xV, yV])
    #
    # v = np.dot(V, N)
    # M = V - 2 * v * N
    #
    # x1 = x0 + 0.5 * M[0]
    # y1 = y0 + 0.5 * M[1]
    #
    # c.create_line([x0, y0, x1, y1], width=2, fill='magenta')


def redraw(event, c, setarrow=False):
    """
    перерисовка изображения на canvas
    :param event:
    :param c:
    :param setarrow:
    :return:
    """
    pass
    # if setarrow:
    #     arrow_state = False
    #     press_x, press_y = 0, 0
    #     temp_x, temp_y = 0, 0
    #     x_fin, y_fin = 0, 0
    # if event:
    #     a = event.widget.get()
    # c.delete("all")
    # if arrow_state:
    #     c.create_line([press_x, press_y, x_fin, y_fin], width=2, fill='blue', arrow=LAST)




# def update_treeview():


class Math:
    """
    Класс, реализующи необходимые математические операции
    """

    def __init__(self, xc, yc):
        """
        Конструкторк класса, установка параметров системы
        :param xc: x-координата центра зеркала
        :param yc: y-координата центра зеркала
        """
        self.mirror_x = xc
        self.mirror_y = yc
        self.higher_edge = (0, 0)
        self.lower_edge = (0, 0)
        self.mirror_xy = []
        self.a = 0
        self.phi = 0

    def x_2(self, t):
        """
        Расчет x зеркала в исходной системе координат
        Функция задана параметрически
        :param t: параметр
        :return: x-координата
        """
        return self.a * (t - self.mirror_y) ** 2 + self.mirror_x

    def x(self, t):
        """
        Расчет x зеркала в повернутой на phi системе координат
        :param t: параметр
        :return: x-координата в новой системе координат
        """
        x1 = self.x_2(t)
        return (x1 - self.mirror_x) * np.cos(self.phi) + (t - self.mirror_y) * np.sin(self.phi) + self.mirror_x

    def y(self, t):
        """
        Расчет y зеркала в повернутой на phi системе координат
        :param t: параметр
        :return: н-координата в новой системе координат
        """
        x1 = self.x_2(t)
        return -1 * (x1 - self.mirror_x) * np.sin(self.phi) + (t - self.mirror_y) * np.cos(self.phi) + self.mirror_y

    def x_vector(self, vector):
        # чтение координат направляющего вектора луча в привычные переменные
        press_x, press_y, x_fin, y_fin = vector[0], vector[1], vector[2], vector[3]

        if y_fin != press_y:
            b1 = (x_fin - press_x) / (y_fin - press_y)
            b2 = press_x - press_y * (x_fin - press_x) / (y_fin - press_y)
        else:
            b1 = 0
            b2 = x_fin

        return b1, b2


    def mirror(self, a, phi):
        """
        Расчет координат параболы, изображающей зеркало
        :param a: кривизна параболы (к-т уравнения при x^2)
        :param phi: угол наклона параболы
        :return: список координат параболы для отображения, правую x-координату параболического зеркала
        """
        self.a = a
        self.phi = phi / 180 * 3.14159265358
        t = np.ones(180).cumsum() - 90 + self.mirror_y
        x2 = self.x(t)
        y2 = self.y(t)

        mirror_border = max(x2)

        c1 = np.empty(len(y2) * 2)
        c1[0::2], c1[1::2] = x2, y2
        c1 = c1.astype(int).copy()

        vec_func = np.vectorize(lambda x: int(x))

        self.mirror_xy = [item for item in zip(vec_func(x2), vec_func(y2))]

        self.higher_edge = (c1[0], c1[1])
        self.lower_edge = (c1[-2], c1[-1])

        return c1, mirror_border

    def cross(self, vector):
        """
        Нахождение точки пересечения луча и параболы
        :param a: кривизна параболы
        :param phi: наклон параболы относительно оси
        :param vector: вектор координат направляющего вектора луча
        :return:
        """
        b1, b2 = self.x_vector(vector)
        press_x, press_y, x_fin, y_fin = vector[0], vector[1], vector[2], vector[3]
        if press_y == y_fin:
            x_line = np.linspace(0, x_fin, x_fin+1)
            y_line = y_fin * np.ones(len(x_line))
        elif np.abs(press_x - x_fin) > np.abs(press_y - y_fin):
            x_line = np.linspace(0, x_fin, x_fin+1)
            y_line = (x_line - b2) / b1
        else:
            if y_fin > press_y:
                y_line = np.linspace(y_fin, 350, 350-y_fin+1)
            else:
                y_line = np.linspace(0, y_fin, y_fin + 1)
            x_line = b1 * y_line + b2

        xy_line = [item for item in zip(x_line, y_line)]
        cross = []
        for item in product(xy_line, self.mirror_xy):
            p1, p2 = item[0], item[1]
            if sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) < sqrt(2):
                cross.append(p2)
        cross = list(set(cross))
        print(cross)
        if len(cross) > 0:
            g1_x = cross[0][0]
            p = cross[0]
            for item in cross:
                if item[0] > g1_x:
                    p = item
            return p, True
        else:
            if y_fin > press_y:
                return (int(b1 * 350 + b2), 350), False
            else:
                return (int(b2), 0), False


class Property_viewer(Treeview):

    def __init__(self, master, **kw):
        super(Property_viewer, self).__init__(master, **kw)
        self.info = {'SP': (0, 0),
                     'FP': (0, 0),
                     'CP': (0, 0)}
        self.txts = {'SP': 'Нач. точка',
                     'FP': 'Кон. точка',
                     'CP': 'Пересечение'}

    def update_values(self, key, value):
        self.info.update({key: value})
        for x in self.get_children():
            self.delete(x)
        for key in self.info.keys():
            if self.info[key][0] != 0:
                self.insert("", END, values=[self.txts[key], '({}, {})'.format(self.info[key][0], self.info[key][1])])


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
        self.arrow_state = False

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
        self.params = Property_viewer(setup2, show='headings', columns=columns, height=5)
        self.params.heading('#1', text='Параметр')
        self.params.heading('#2', text='Значение')
        self.params.column('#1', width=100, minwidth=50, stretch=NO, anchor=N)
        self.params.column('#2', width=100, minwidth=50, stretch=NO, anchor=N)
        self.params.pack(side=TOP, padx=(5, 10), pady=(0, 10))

        butFrame.pack(side=TOP)

        setup1.pack(side=LEFT)
        setup2.pack(side=LEFT)

        canv.pack(side=TOP, pady=(10, 10))
        setup.pack(side=TOP, pady=(0, 10), padx=(25, 25))

        window.bind('<Button-1>', self.press)
        window.bind('<ButtonRelease-1>', self.release)
        self.draw_mirror()
        window.mainloop()

    def press(self, event):
        """
        Обработчкик события "нажатие кнопки мыши"
        :param event: экземпляр класса Event (событие)
        :return:
        """
        if event.widget.master is not None:
            if event.widget.widgetName == 'canvas':
                self.temp_x, self.temp_y = event.x, event.y

    def release(self, event):
        """
        обработчик события "отпускание кнопки мыши"
        :param event: экземпляр класса Event (событие)
        :return:
        """
        if event.widget.master is not None:
            if event.widget.widgetName == 'canvas':
                if (event.x > self.mirror_border) & (event.x < self.temp_x):
                    self.x_fin, self.y_fin = event.x, event.y
                    self.press_x, self.press_y = self.temp_x, self.temp_y
                    self.arrow_state = True
                    self.redraw()
                    self.params.update_values('SP', (self.press_x, self.press_y))
                    self.params.update_values('FP', (self.x_fin, self.y_fin))
                else:
                    self.arrow_state = False

    def check_arrowstate(self):
        """
        проверка состояния (отображения) направляющего вектора луча
        :return: True, если вектор отображен на канве
        """
        if self.x_fin > self.mirror_border:
            self.arrow_state = True
            return True
        else:
            self.arrow_state = False
            return False

    def draw_beam(self):
        """
        Изображение луча
        :return: None
        """
        self.c.create_line([self.press_x, self.press_y, self.x_fin, self.y_fin], width=2, fill='blue', arrow=LAST)
        if self.y_fin == 0:
            return

        cross, cross_flag = self.math.cross([self.press_x, self.press_y, self.x_fin, self.y_fin])
        if cross_flag:
            self.c.create_oval([cross[0]-3, cross[1]-3, cross[0]+3, cross[1]+3], fill='yellow')
            self.params.update_values('CP', (cross[0], cross[1]))
        else:
            self.params.update_values('CP', (0, 0))
        self.c.create_line([self.x_fin, self.y_fin, cross[0], cross[1]], fill='green', dash=True)

    def draw_mirror(self):
        """
        Отображение зеркала с учетом параметров, определенных ползунками
        :return:
        """
        # получение данных из экземпляра класса Math
        # изображение зеркала
        c1, self.mirror_border = self.math.mirror(self.scal.get(), self.angle.get())
        self.c.create_line(list(c1), width=3, fill='red')

        # отображение центра зеркала
        self.c.create_oval(self.x_center, self.y_center, self.x_center - 5, self.y_center-5, fill='green')

    def redraw(self, event=None):
        """
        Обновление (перерисовка) канвы
        :param event: событие, вызвавшее метод перерисовки
        :return: None
        """
        self.c.delete('all')
        self.draw_mirror()
        if self.check_arrowstate():
            self.draw_beam()


if __name__ == '__main__':
    App(350)  # создание экземпляра класса приложение с вертикальным размером канвы 350
