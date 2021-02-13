import numpy as np
import sys
import re
import matplotlib.pyplot as plt
import numpy.linalg as la


def calcB(c, phi, A):
    """
    Расчет положения точки B
    :param c: длина начальной стороны
    :param phi: угол наклона начальной стороны
    :param A: положение вершины A
    :return: положение вершины B
    """
    return A + c * np.array([np.cos(phi * 3.1415 / 180), np.sin(phi * 3.1415 / 180)]).T


def calc(A, B, alpha, beta, phi):
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


def case1(c, phi, A):
    """
    расчет положения точек для случая 1
    :param c: длина начальной стороны, здесь не используется. Для унификации параметров case1-case3
    :param phi: угол наклона начальной стороны
    :param A: положение точки А
    :return: возвращает кортеж положений точек C1 и C2
    """
    try:
        b = float(input('Длина стороны b='))
        if b <= 0:
            raise ValueError
        alpha = float(input('Угол alpha='))
    except ValueError:
        print('Неверный ввод')
        sys.exit(1)

    C1 = A + b * np.array([np.cos((phi + alpha) * 3.1415 / 180), np.sin((phi + alpha) * 3.1415 / 180)])
    C2 = A + b * np.array([np.cos((phi - alpha) * 3.1415 / 180), np.sin((phi - alpha) * 3.1415 / 180)])

    return C1, C2


def case2(c, phi, A):
    """
    расчет положения точек для случая 2
    :param c: длина начальной стороны
    :param phi: угол наклона начальной стороны
    :param A: положение точки А
    :return: возвращает кортеж положений точек C1 и C2
    """
    try:
        alpha = float(input('Угол alpha='))
        beta = float(input('Угол beta='))
        if (alpha * beta <= 0) | (abs(alpha + beta) >= 180):
            raise ValueError
    except ValueError:
        print('Неверный ввод')
        sys.exit(1)

    B = calcB(c, phi, A)

    phi = np.radians(phi)
    alpha = np.radians(alpha)
    beta = np.radians(beta)

    return calc(A, B, alpha, beta, phi)


def case3(c, phi, A):
    """
    расчет положения точек для случая 3. Рассчитывает углы и использует расчет для случая 2
    :param c: длина начальной стороны
    :param phi: угол наклона начальной стороны
    :param A: положение точки А
    :return: возвращает кортеж положений точек C1 и C2
    """
    try:
        a = float(input('Сторона a='))
        b = float(input('Сторона b='))
        if (a <= 0) | (b <= 0):
            raise ValueError
    except ValueError:
        print('Неверный ввод')
        sys.exit(1)

    alpha = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))
    beta = np.arccos((a**2 + c**2 - b**2) / (2 * a * c))

    B = calcB(c, phi, A)
    phi = np.radians(phi)

    return calc(A, B, alpha, beta, phi)


def use_reference():
    """
    выводит сообщение об использовании скрипта с параметрами командной строки
    :return: None
    """
    print('Некорректное использование аргументов запуска\nДля запуска укажите следующие параметры:')
    print('\t type= для определения типа задачи \n \t с= для задания стороны \n \t phi= для задания угла')


def get_parameters(lst):
    """
    формирование словаря параметров из списка параметров командной стркоки sys.argv
    :param lst: sys.argv
    :return: словарь параметров
    """
    res = {}
    for item in lst:
        p_name = re.search(r'[A-Za-z]{1,}=', item).group(0)[:-1]
        p_value = item[item.index('=') + 1:]
        if p_name != 'A':
            try:
                res.update({p_name: float(p_value)})
            except ValueError:
                res.update({p_name: 0})
        else:
            Ax = p_value[1:p_value.index(',')].strip()
            Ay = p_value[p_value.index(',') + 1:-1].strip()
            try:
                res.update({p_name: (float(Ax), float(Ay))})
            except ValueError:
                res.update({p_name: (0, 0)})
    return res


def plot(A, B, C1, C2):
    """
    построение треугольников с использованием Matplotlib по заданным координатам
    :param A, B, C1, C2: кооординаты вершин
    :return: None
    """
    fig, axes = plt.subplots()

    dim = np.dstack((A, B, C1, C2)).squeeze()
    x = dim[0, :]
    y = dim[1, :]

    diam = max(max(x) - min(x) + 1, max(y) - min(y) + 1)

    t1 = plt.Polygon([A, B, C1], color='red')
    t2 = plt.Polygon([A, B, C2], color='blue')
    fig.gca().add_patch(t1)
    fig.gca().add_patch(t2)
    axes.set_xlim([min(x) - 1, min(x) + diam])
    axes.set_ylim([min(y) - 1, min(y) + diam])
    plt.grid()
    plt.show()


def main():
    """
    основная процедура
    :return: None
    """
    # проверка аргументов запуска скрипта
    if len(sys.argv) != 5:
        use_reference()
        sys.exit(1)

    # получение присвоение параметров для проведения расчетов
    params = get_parameters(sys.argv[1:])
    try:
        task_type = params['type']
        c = params['c']
        phi = params['phi']
        Ax, Ay = params['A']
    except KeyError:
        print('Недостаточно параметров')
        sys.exit(1)

    A = np.array([Ax, Ay]).T
    B = calcB(c, phi, A)
    C1, C2 = cases[task_type](c, phi, A)

    plot(A, B, C1, C2)


cases = {1: case1, 2: case2, 3: case3}

if __name__ == '__main__':
    main()
