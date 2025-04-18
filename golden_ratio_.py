import math
from typing import Callable

def func(x):
    return x*x - 4 * x + 6


PHI = (3 - math.sqrt(5)) / 2

def find_min(func: Callable, a0: float, b0: float, epsilon: float):
    a = a0
    b = b0
    x_ = a + PHI * (b - a)
    y_ = a + b - x_
    f_x = func(x_)
    f_y = func(y_)
    k = 0
    while b - a > epsilon:
        print("=========")
        print(k)
        print(a, b)
        print(x_, y_)
        print(f_x, f_y)
        k += 1
        if f_x <= f_y:
            b = y_
            y_ = x_
            x_ = a + b - x_
            f_y = f_x
            f_x = func(x_)

            print("new b: " + b.__str__())
        else:
            a = x_
            x_ = y_
            y_ = a + b - y_
            f_x = f_y
            f_y = func(y_)
            print("new a: " + a.__str__())
        print("========")
    return {
        "min": (a + b) / 2,
        "func_min": func((a + b) / 2),
        "a": a,
        "b": b,
        "k": k,
        "N": k + 2,
        "R(N)": (0.618)**(k + 1)
    }

if __name__ == '__main__':
    print(find_min(func, 0, 10, 0.5))
