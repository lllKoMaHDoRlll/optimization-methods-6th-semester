import math
from golden_ratio_ import find_min
from collections.abc import Callable

def norm(vec: list[float]) -> float:
    return math.sqrt(sum([el * el for el in vec]))


def newton_method(f: Callable, x0: list[float], epsilon1: float, epsilon2: float, M: int, DO_LOG: bool = False):
    print = lambda x: print(x) if DO_LOG else ...
    def find_min_t(x: list[float], d: list[float], epsilon) -> float:
        return find_min(
            lambda t: f([x[i] + t * d[i] for i in range(len(x))]),
            0, 1, epsilon
        )["min"]

    def get_H(x: list[float], h: float) -> list[list[float]]:
        print([x[0] + h, x[1]])
        print(f([x[0] + h, x[1]]))
        return [
            [
                (
                    f([x[0] + h, x[1]]) - 2 * f(x) + f([x[0] - h, x[1]])
                ) / (h*h),
                (
                    f([x[0] + h, x[1] + h]) - f([x[0] + h, x[1] - h]) - f([x[0] - h, x[1] + h]) + f([x[0] - h, x[1] - h])
                ) / (4*h*h)
            ],
            [
                (
                    f([x[0] + h, x[1] + h]) - f([x[0] + h, x[1] - h]) - f([x[0] - h, x[1] + h]) + f([x[0] - h, x[1] - h])
                ) / (4*h*h),
                (
                    f([x[0], x[1] + h]) - 2 * f(x) + f([x[0], x[1] - h])
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
            grad[i] =  (f(x_) - f(x)) / epsilon
        return grad

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
        # t = find_min_t(x_prev, grad)
        H = get_H(x_prev, 0.0001)
        print(f"{H=}")
        inv_H = get_inv_H(H)
        print(f"{inv_H=}")
        if is_positive(inv_H):
            t = 1.
            d = [ -1 * sum([inv_H[i][j] * grad_value[j] for j in range(len(x0))]) for i in range(len(x0))]
        else:
            d = [-1 * grad_value[i] for i in range(len(x0))]
            t = find_min_t(x_prev, d, epsilon1)
        print(f"{d=}")
        print(f"{t=}")
        x_next = [x_prev[i] + t * d[i] for i in range(len(x0))]
        print(f"{x_next=}")
        print(f"norm: {norm([x_next[i] - x_prev[i] for i in range(len(x0))])}, delta: {abs(f(x_next) - f(x_prev))}")
        if norm([x_next[i] - x_prev[i] for i in range(len(x0))]) < epsilon2 and abs(f(x_next) - f(x_prev)) < epsilon2:
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
        "f(x*)": f(x_min),
        "k": k,
        "condition": condition
    }

if __name__ == '__main__':
    def func(x: list[float]) -> float:
        return x[0]*x[0] + 5 * x[1] * x[1] + x[0] * x[1] + x[0]

    print(newton_method(func, [1, 1], 0.1, 0.15, 10))
