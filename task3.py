from tkinter import Tk, Frame, LabelFrame, Canvas, TOP, LEFT, Scale, HORIZONTAL, Button, NO, LAST
from tkinter.ttk import Treeview
import numpy as np
import sys

press_x, press_y = 0, 0
x_fin, y_fin = 0, 0
mirror_border = 0
arrow_state = False
a = 0.002


def draw_parabola(canv):
    global a, mirror_border
    y1 = np.ones(100)
    y1 = y1.cumsum()
    y2 = -1 * y1
    x1 = a * (y1 * y1) + 30
    x2 = a * (y2 * y2) + 30
    mirror_border = max(max(x1), max(x2))
    y1, y2 = y1 + 115, y2 + 115

    c1, c2 = np.empty(len(y1) * 2), np.empty(len(y2) * 2)
    c1[0::2], c1[1::2] = x1, y1
    c2[0::2], c2[1::2] = x2, y2
    c1, c2 = c1.astype(int).copy(), c2.astype(int).copy()
    canv.create_line(list(c1), width=3, fill='red')
    canv.create_line(list(c2), width=3, fill='red')
    canv.create_line(list(c1)[:2] + list(c2)[:2], width=3, fill='red')


def main():
    window = Tk()
    window.title("Отражение в параболическом зеркале")
    window.geometry('500x400')
    canv = Frame(window)
    setup = LabelFrame(window, text='Настройки', width=450, height=150)
    c = Canvas(canv, width=450, height=230, bg='black')
    c.pack(side=TOP, padx=10)

    setup1 = Frame(setup)
    butFrame = Frame(setup1)

    scal = Scale(setup1, orient=HORIZONTAL, length=200, from_=0.002, to=0.01, tickinterval=0.002, resolution=0.002)
    scal.set(0.002)
    scal.pack(side=TOP, pady=(0, 10), padx=(10, 10))
    scal.bind("<ButtonRelease-1>", lambda event, draw_canv=c: redraw(event, draw_canv))

    Button(butFrame, text='Очистить', width=12, command=lambda event=None, draw_canv=c, flag=True: redraw(event, draw_canv,
                                                                                                     setarrow=flag)) \
        .pack(side=LEFT, padx=(10, 5), pady=(5, 10))
    Button(butFrame, text='Закрыть', width=12, command=lambda flag=0: sys.exit(flag)).pack(side=LEFT, padx=(5, 10),
                                                                                           pady=(5, 10))

    butFrame.pack(side=TOP)

    setup1.pack(side=LEFT)

    columns = ('#1', '#2')
    params = Treeview(setup, show='headings', columns=columns)
    params.heading('#1', text='Параметр')
    params.heading('#2', text='Значение')
    params.column('#1', width=100, minwidth=50, stretch=NO)
    params.column('#2', width=100, minwidth=50, stretch=NO)
    params.pack(side=LEFT, padx=(5, 10), pady=(0, 10))

    canv.pack(side=TOP, pady=(10, 10))
    setup.pack(side=TOP, pady=(0, 10), padx=(25, 25))

    draw_parabola(c)

    window.bind('<Button-1>', press)
    window.bind('<ButtonRelease-1>', lambda event, draw_canv=c: release(event, draw_canv))
    window.mainloop()


def redraw(event, c, setarrow=False):
    global a, arrow_state
    if setarrow:
        arrow_state = False
    if event:
        a = event.widget.get()
    c.delete("all")
    if arrow_state:
        c.create_line([press_x, press_y, x_fin, y_fin], width=2, fill='blue', arrow=LAST)
    draw_parabola(c)


def press(event):
    global press_x, press_y
    if event.widget.widgetName == 'canvas':
        press_x, press_y = event.x, event.y


def release(event, c):
    global x_fin, y_fin, arrow_state
    if event.widget.widgetName == 'canvas':
        c.delete('all')
        draw_parabola(c)
        arrow_state = True
        x_fin, y_fin = event.x, event.y
        c.create_line([press_x, press_y, x_fin, y_fin], width=2, fill='blue', arrow=LAST)


if __name__ == '__main__':
    main()
