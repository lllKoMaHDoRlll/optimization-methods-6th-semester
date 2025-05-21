from collections.abc import Callable
from fletcher_revs import fletcher_revs_method
from newton import newton_method

def penalties_method(
        f: Callable[[list[float]], float],
        g: Callable[[list[float]], tuple[list[float], list[float]]],
        x0: list[float] = [1, 1],
        r0: float = 1,
        C: float = 10,
        epsilon: float = 0.001,
        M: int = 50,
    ):
    if r0 <= 0: raise Exception(f"Invalid argument {r0=}")
    if C <= 1: raise Exception(f"Invalid argument {C=}")
    if epsilon <= 0: raise Exception(f"Invalid argument {epsilon=}")

    def P(x: list[float], r: float) -> float:
        return (r / 2) * (
            sum([g_j * g_j for g_j in g(x)[0]]) + sum([max(0, g_j_plus) * max(0, g_j_plus) for g_j_plus in g(x)[1]])
        )

    def F(x: list[float], r: float) -> float:
        return f(x) + P(x, r)

    r = r0
    x = x0
    k = 0
    table = []
    while True:
        x = fletcher_revs_method(lambda y: F(y, r), x, epsilon / 100, epsilon / 100, M, True)["x*"]
        penalty = P(x, r)

        table.append({
            "k": k,
            "r": 1,
            "x": x,
            "F(x, r)": F(x, r),
            "P(x, r)": P(x, r),
            "g(x)": g(x)
        })

        if penalty <= epsilon:
            return {
                "x*": x,
                "f(x*)": f(x),
                "k": k,
                "condition": "penalty is low",
                "table": table
            }

        r *= C
        k += 1

        if k == M:
            return {
                "x*": x,
                "f(x*)": f(x),
                "k": k,
                "condition": "total iterations limit",
                "table": table
            }

if __name__ == '__main__':

    def func(x: list[float]) -> float:
        return x[0]*x[0] + 5 * x[1] * x[1] + x[0] * x[1] + x[0]

    def g(x: list[float]) -> tuple[list[float], list[float]]:
        return (
            [
                2 * x[0] + 3 * x[1] - 1
            ],
            []
        )

    res = penalties_method(func, g)

    print("\n".join(map(str, res["table"])))
