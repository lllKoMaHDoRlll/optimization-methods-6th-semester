import math
from golden_ratio_ import find_min

def func(x: list[float]) -> float:
    return x[0]*x[0] + 5 * x[1] * x[1] + x[0] * x[1] + x[0]

def find_min_t(x: list[float], d: list[float], epsilon) -> float:
    return find_min(
        lambda t: func([x[i] + t * d[i] for i in range(len(x))]),
        0, 1, epsilon
    )["min"]

def get_H(x: list[float], h: float) -> list[list[float]]:
    print([x[0] + h, x[1]])
    print(func([x[0] + h, x[1]]))
    return [
        [
            (
                func([x[0] + h, x[1]]) - 2 * func(x) + func([x[0] - h, x[1]])
            ) / (h*h),
            (
                func([x[0] + h, x[1] + h]) - func([x[0] + h, x[1] - h]) - func([x[0] - h, x[1] + h]) + func([x[0] - h, x[1] - h])
            ) / (4*h*h)
        ],
        [
            (
                func([x[0] + h, x[1] + h]) - func([x[0] + h, x[1] - h]) - func([x[0] - h, x[1] + h]) + func([x[0] - h, x[1] - h])
            ) / (4*h*h),
            (
                func([x[0], x[1] + h]) - 2 * func(x) + func([x[0], x[1] - h])
            ) / (h*h)
        ]
    ]

def get_inv_H(H: list[list[float]]):
    det = H[0][0] * H[1][1] - H[0][1] * H[1][0]
    return [
        [H[1][1] / det, -1 * H[0][1] / det],
        [-1 * H[1][0] / det, H[0][0] / det]
    ]

def is_positive(matrix):
    return matrix[0][0] > 0 and (matrix[0][0] * matrix[1][1] - matrix[0][1]*matrix[1][0]) > 0 

def grad(x: list[float]) -> list[float]:
    grad = [0. for _ in range(len(x))]
    epsilon = 0.0001
    for i in range(len(x)):
        x_ = x[:]
        x_[i] += epsilon
        grad[i] =  (func(x_) - func(x)) / epsilon
    return grad

def norm(vec: list[float]) -> float:
    return math.sqrt(sum([el * el for el in vec]))


def ramsen_method(x0: list[float], epsilon1: float, epsilon2: float, M: int):
    k = 0
    x_prev = x0[:]
    x_next = x0[:]
    stop_condition_prev = False
    stop_condition_cur = False
    condition = ""
    while True:
        print(f"{k=}")
        print(f"{x_prev}")
        grad_value = grad(x_prev)
        print(f"{grad_value=}")
        print(f"norm_grad: {norm(grad_value)}")
        if norm(grad_value) < epsilon1:
            x_min = x_prev
            condition = "1"
            break
        if k >= M:
            x_min = x_prev
            condition = "2"
            break
        H = get_H(x_prev, 0.0001)
        print(f"{H=}")
        inv_H = get_inv_H(H)
        print(f"{inv_H=}")
        if is_positive(inv_H):
            d = [ -1 * sum([inv_H[i][j] * grad_value[j] for j in range(len(x0))]) for i in range(len(x0))]
        else:
            d = [-1 * grad_value[i] for i in range(len(x0))]
        t = find_min_t(x_prev, d, epsilon1)
        print(f"{d=}")
        print(f"{t=}")
        x_next = [x_prev[i] + t * d[i] for i in range(len(x0))]
        print(f"{x_next=}")
        print(f"norm: {norm([x_next[i] - x_prev[i] for i in range(len(x0))])}, delta: {abs(func(x_next) - func(x_prev))}")
        if norm([x_next[i] - x_prev[i] for i in range(len(x0))]) < epsilon2 and abs(func(x_next) - func(x_prev)) < epsilon2:
            stop_condition_cur = True
            if stop_condition_prev and stop_condition_cur:
                x_min = x_next
                condition = "3"
                break
        k += 1
        x_prev = x_next
        stop_condition_prev = stop_condition_cur
        stop_condition_cur = False
    
    return {
        "x*": x_min,
        "f(x*)": func(x_min),
        "k": k,
        "condition": condition
    }

print(ramsen_method([1, 1], 0.1, 0.15, 10))
