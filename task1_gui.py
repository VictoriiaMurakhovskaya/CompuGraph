from tkinter import Tk, Frame, LabelFrame, Canvas, TOP, LEFT, Scale, HORIZONTAL, Button, NO, LAST, END, N, W
from tkinter.ttk import Treeview, Notebook, Label
import numpy as np
import sys
from math import sqrt
import numpy.linalg as la
from math import atan


class App:

    def __init__(self):
        # создание основного окна Tkinter
        self.window = Tk()
        self.window.title("Треугольники")
        self.window.geometry('500x460')
        self.window.minsize(500, 480)
        self.window.maxsize(500, 480)

        self.press_x, self.press_y = 0, 0
        self.release_x, self.release_y = 0, 0

        # размещение элементов интерфейса

        # основной элемент - Canvas
        self.c = Canvas(self.window, width=450, height=250, bg='black')
        self.c.pack(side=TOP, padx=10, pady=(10, 0))

        # элементы управления: настройки, отображение параметров, очистка/выход
        setup = Frame(self.window, width=450)
        setup_left = Frame(setup, width=250)
        setup_right = Frame(setup, width=180)

        self.setup_notebook = Notebook(setup_left)

        setup1 = Frame(setup_left, width=230, height=140)
        setup2 = Frame(setup_left, width=230, height=140)
        setup3 = Frame(setup_left, width=230, height=140)

        # элементы управления на вкладках
        # вкладка 1
        Label(setup1, text='Длина стороны').pack(side=TOP, pady=(10, 0), padx=(10, 0), anchor=W)
        self.scal_b = Scale(setup1, orient=HORIZONTAL, length=200, from_=0, to=300, tickinterval=100, resolution=10)
        self.scal_b.pack(side=TOP)
        self.scal_b.set(100)
        self.scal_b.bind("<ButtonRelease-1>", self.draw_triangle)
        Label(setup1, text='Угол \u03b1').pack(side=TOP, pady=(10, 0), padx=(10, 0), anchor=W)
        self.scal_alpha = Scale(setup1, orient=HORIZONTAL, length=200, from_=0, to=90, tickinterval=15, resolution=5)
        self.scal_alpha.pack(side=TOP)
        self.scal_alpha.set(30)
        self.scal_alpha.bind("<ButtonRelease-1>", self.draw_triangle)

        # вкладка 2
        Label(setup2, text='Угол \u03b1').pack(side=TOP, pady=(10, 0), padx=(10, 0), anchor=W)
        self.scal_alpha2 = Scale(setup2, orient=HORIZONTAL, length=200, from_=0, to=90, tickinterval=15, resolution=5)
        self.scal_alpha2.pack(side=TOP)
        self.scal_alpha2.set(60)
        self.scal_alpha2.bind("<ButtonRelease-1>", self.draw_triangle)
        Label(setup2, text='Угол \u03b2').pack(side=TOP, pady=(10, 0), padx=(10, 0), anchor=W)
        self.scal_beta = Scale(setup2, orient=HORIZONTAL, length=200, from_=0, to=90, tickinterval=15, resolution=5)
        self.scal_beta.pack(side=TOP)
        self.scal_beta.set(60)
        self.scal_beta.bind("<ButtonRelease-1>", self.draw_triangle)

        # вкладка 3
        Label(setup3, text='Длина стороны 2').pack(side=TOP, pady=(10, 0), padx=(10, 0), anchor=W)
        self.scal_a = Scale(setup3, orient=HORIZONTAL, length=200, from_=0, to=300, tickinterval=100, resolution=10)
        self.scal_a.pack(side=TOP)
        self.scal_a.set(100)
        self.scal_a.bind("<ButtonRelease-1>", self.draw_triangle)
        Label(setup3, text='Длина стороны 3').pack(side=TOP, pady=(10, 0), padx=(10, 0), anchor=W)
        self.scal_b2 = Scale(setup3, orient=HORIZONTAL, length=200, from_=0, to=300, tickinterval=100, resolution=10)
        self.scal_b2.pack(side=TOP)
        self.scal_b2.set(100)
        self.scal_b2.bind("<ButtonRelease-1>", self.draw_triangle)

        setup1.pack()
        setup2.pack()
        setup3.pack()

        self.setup_notebook.add(setup1, text='Задача 1')
        self.setup_notebook.add(setup2, text='Задача 2')
        self.setup_notebook.add(setup3, text='Задача 3')
        self.setup_notebook.bind('<<NotebookTabChanged>>', self.draw_triangle)

        self.setup_notebook.pack(side=LEFT)

        columns = ('#1', '#2')
        self.params = Treeview(setup_right, show='headings', columns=columns, height=5)
        self.params.heading('#1', text='Параметр')
        self.params.heading('#2', text='Значение')
        self.params.column('#1', width=100, minwidth=50, stretch=NO, anchor=N)
        self.params.column('#2', width=100, minwidth=50, stretch=NO, anchor=N)
        self.params.pack(side=TOP, padx=(15, 0), pady=(27, 5))

        butframe = Frame(setup_right)
        Button(butframe, text='Очистить', width=10, command=self.draw_base()).pack(side=LEFT, padx=(25, 5))
        Button(butframe, text='Выход', width=10, command=lambda x=0: sys.exit(x)).pack(side=LEFT, padx=(0, 10))
        butframe.pack(side=TOP, pady=(5, 5))

        setup_left.pack(side=LEFT)
        setup_right.pack(side=LEFT)
        setup.pack(side=TOP, pady=(5, 10), padx=(5, 5))

        self.window.bind('<Button-1>', self.press)
        self.window.bind('<ButtonRelease-1>', self.release)

        self.draw_base()
        self.window.mainloop()

    def draw_base(self):
        self.c.delete("all")
        self.c.create_line([5, 125, 445, 125], arrow=LAST, fill='white')
        self.c.create_line([225, 245, 225, 5], arrow=LAST, fill='white')
        self.c.create_text(442, 135, text='x', fill='white')
        self.c.create_text(235, 8, text='y', fill='white')

    def press(self, event):
        """
        Обработчкик события "нажатие кнопки мыши"
        :param event:
        :return:
        """
        if event.widget.master is not None:
            if event.widget.widgetName == 'canvas':
                self.draw_base()
                self.press_x, self.press_y = event.x, event.y

    def release(self, event):
        if event.widget.master is not None:
            if event.widget.widgetName == 'canvas':
                self.release_x, self.release_y = event.x, event.y
                if (self.release_x in range(450)) & (self.release_y in range(250)):
                    self.draw_triangle(None)

    def draw_triangle(self, event):
        if (self.press_x > 0) & (self.press_y > 0) & (self.release_x > 0) & (self.release_y > 0):
            self.draw_base()
            triangle = Math((self.press_x, self.press_y), (self.release_x, self.release_y))
            task = self.setup_notebook.index(self.setup_notebook.select()) + 1
            if task == 1:
                data_dict = {'b': self.scal_b.get(), 'alpha': self.scal_alpha.get()}
            elif task == 2:
                data_dict = {'alpha': self.scal_alpha2.get(), 'beta': self.scal_beta.get()}
            elif task == 3:
                data_dict = {'a': self.scal_a.get(), 'b': self.scal_b2.get()}
            else:
                return
            C1, C2, data_dict = triangle.get_c(task, data_dict)
            if (C1[0] < 0) | (C1[1] < 0) | (C2[0] < 0) | (C2[1] < 0):
                self.c.create_text(300, 100, text='Невозможно выполнить построение', fill='white')
            else:
                self.c.create_polygon([self.press_x, self.press_y, self.release_x, self.release_y, C1[0], C1[1]],
                                      fill='red')
                self.c.create_polygon([self.press_x, self.press_y, self.release_x, self.release_y, C2[0], C2[1]],
                                      fill='blue')
                self.update_treeview(data_dict)

    def update_treeview(self, data):
        """
        запись параметров в элемент Treeview
        :return: None
        """
        for x in self.params.get_children():
            self.params.delete(x)
        for key in data.keys():
            self.params.insert("", END, values=[key, data[key]])


class Math:
    def __init__(self, A, B):
        self.A, self.B = A, B
        self.C1, self.C2 = (0, 0), (0, 0)
        Ax, Ay = self.A[0], self.A[1]
        Bx, By = self.B[0], self.B[1]
        self.phi = atan((By-Ay) / (Bx-Ax)) * 180 / 3.1415
        self.c = sqrt((Ax-Bx)**2 + (Ay-By)**2)

    def get_c(self, case, data):
        if case == 1:
            self.C1, self.C2 = self.case1(self.phi, self.A, data['b'], data['alpha'])
        elif case == 2:
            self.C1, self.C2 = self.case2(self.c, self.phi, self.A, data['alpha'], data['beta'])
        elif case == 3:
            self.C1, self.C2 = self.case3(self.c, self.phi, self.A, data['a'], data['b'])
        return self.C1, self.C2, {'A': '({:d}, {:d})'.format(int(self.A[0]), int(self.A[1])),
                                  'B': '({:d}, {:d})'.format(int(self.B[0]), int(self.B[1])),
                                  'phi': int(self.phi),
                                  'C1': '({:d}, {:d})'.format(int(self.C1[0]), int(self.C1[1])),
                                  'C2': '({:d}, {:d})'.format(int(self.C2[0]), int(self.C2[1]))}

    def calcB(self, c, phi, A):
        """
        Расчет положения точки B
        :param c: длина начальной стороны
        :param phi: угол наклона начальной стороны
        :param A: положение вершины A
        :return: положение вершины B
        """
        return A + c * np.array([np.cos(phi * 3.1415 / 180), np.sin(phi * 3.1415 / 180)]).T

    def calc(self, A, B, alpha, beta, phi):
        """
        расчет положения точек C1 и C2
        :param A: положение точки А
        :param B: положение точки В
        :param alpha: угол альфа (случаи 2 и 3)
        :param beta: угол бета (случаи 2 и 3)
        :param phi: угол наклона начальной стороны
        :return: возвращает кортеж положений точек C1 и C2
        """
        V1 = np.array([np.cos(phi + alpha), np.sin(phi + alpha)])
        V2 = np.array([np.cos(phi - alpha), np.sin(phi - alpha)])
        W1 = -1 * np.array([np.cos(phi - beta), np.sin(phi - beta)])
        W2 = -1 * np.array([np.cos(phi + beta), np.sin(phi + beta)])

        t = np.dot((B - A), la.inv(np.array([V1, -1 * W1])))
        C1 = A + V1 * t[0]

        t = np.dot((B - A), la.inv(np.array([V2, -1 * W2])))
        C2 = A + V2 * t[0]

        return C1, C2

    def case1(self, phi, A, b, alpha):
        """
        расчет положения точек для случая 1
        :param phi: угол наклона начальной стороны
        :param A: положение точки А
        :return: возвращает кортеж положений точек C1 и C2
        """
        C1 = A + b * np.array([np.cos((phi + alpha) * 3.1415 / 180), np.sin((phi + alpha) * 3.1415 / 180)])
        C2 = A + b * np.array([np.cos((phi - alpha) * 3.1415 / 180), np.sin((phi - alpha) * 3.1415 / 180)])

        return C1, C2

    def case2(self, c, phi, A, alpha, beta):
        """
        расчет положения точек для случая 2
        :param c: длина начальной стороны
        :param phi: угол наклона начальной стороны
        :param A: положение точки А
        :return: возвращает кортеж положений точек C1 и C2
        """
        B = self.calcB(c, phi, A)

        phi = np.radians(phi)
        alpha = np.radians(alpha)
        beta = np.radians(beta)

        return self.calc(A, B, alpha, beta, phi)

    def case3(self, c, phi, A, a, b):
        """
        расчет положения точек для случая 3. Рассчитывает углы и использует расчет для случая 2
        :param c: длина начальной стороны
        :param phi: угол наклона начальной стороны
        :param A: положение точки А
        :return: возвращает кортеж положений точек C1 и C2
        """

        alpha = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
        beta = np.arccos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))

        B = self.calcB(c, phi, A)
        phi = np.radians(phi)

        return self.calc(A, B, alpha, beta, phi)




def main():
    app = App()




if __name__ == '__main__':
    main()
