def func(x):
    return x*x - 4 * x + 6

def find_min(a0: float, b0: float, epsilon: float, delta: float):
    a = a0
    b = b0
    k = 0
    while b - a > epsilon:
        print(a, b)
        x_ = (a + b - delta) / 2
        y_ = (a + b + delta) / 2
        print(x_, y_)
        f_x = func(x_)
        f_y = func(y_)
        print(f_x, f_y)
        if f_x <= f_y:
            b = y_
            print("new b: " + b.__str__())
        else:
            a = x_
            print("new a: " + a.__str__())
        print("========")
        k += 1

    return {
        "min": (a + b) / 2,
        "func_min": func((a + b) / 2),
        "a": a,
        "b": b,
        "k": k,
        "N": 2 * (k+1),
        "R(N)": (2)**(-1 * (k + 1))
    }


print(find_min(0, 10, 0.5, 0.2))