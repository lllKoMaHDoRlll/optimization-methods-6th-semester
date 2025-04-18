import math

def func(x: list[float]) -> float:
    return 2 * x[0] * x[0] + x[0] * x[1] + x[1]*x[1]

def find_min_t(x: list[float], grad: list[float] = [0, 0]) -> float: # переделать с градом
    return (
        (4 * x[0] + x[1])**2 + (x[0] + 2 * x[1])**2
    ) / (
        4 * (4 * x[0] + x[1])**2 + 2 * (4 * x[0] + x[1]) * (x[0] + 2 * x[1]) + 2 * (x[0] + 2 * x[1])**2
    )

def partial(i: int, x: list[float]) -> list[float]:
    epsilon = 0.0001
    x_ = x[:]
    x_[i] += epsilon
    return (func(x_) - func(x)) / epsilon

def norm(vec: list[float]) -> float:
    return math.sqrt(sum([el * el for el in vec]))

def gradient_decrease(x0: list[float], epsilon1: float, epsilon2: float, M: int):
    k = 0
    x_prev = x0[:]
    x_next = x0[:]
    stop_condition_prev = False
    stop_condition_cur = False
    condition = ""
    while True:
        print(f"{k=}")
        print(f"{x_prev}")
        grad = [partial(i, x_prev) for i in range(len(x0))]
        print(f"{grad=}")
        print(f"norm_grad: {norm(grad)}")
        if norm(grad) < epsilon1:
            x_min = x_prev
            condition = "1"
            break
        if k >= M:
            x_min = x_prev
            condition = "2"
            break
        # t = find_min_t(x_prev, grad)
        t = find_min_t(x_prev)
        print(f"{t=}")
        x_next = [x_prev[i] - t * grad[i] for i in range(len(x0))]
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

print(gradient_decrease([0.5, 1], 0.1, 0.15, 10))
