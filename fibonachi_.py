def func(x):
    return x * x - 4 * x + 6


fib_numbers = [1, 1]

def fibonachi(N: int):
    while N >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
    return fib_numbers[N]

def fib_method(a, b, l, epsilon):
    N = 1
    while fibonachi(N) < (b-a)/l:
        N += 1
    
    print(f"{N=}")
    
    y = a + (fibonachi(N-2)/fibonachi(N)) * (b-a)
    z = a + (fibonachi(N-1)/fibonachi(N)) * (b-a)
    print(f"{y=}, {z=}")
    k = 0

    while True:
        fy = func(y)
        fz = func(z)
        print(f"{fy=}, {fz=}")
        if fy <= fz:
            print("=a=")
            b = z
            z = y
            y = a + (fibonachi(N-k-3)/fibonachi(N-k-1)) * (b-a)
            print(f"new {y=}")
        else:
            print("=a=")
            a = y
            y = z
            z = a + (fibonachi(N-k-2)/fibonachi(N-k-1)) * (b-a)
            print(f"new {z=}")
        if k == N - 3:
            break
        k += 1
    
    print(y, z)
    
    if abs(y - z) < epsilon:
        z = y + epsilon
        fy = func(y)
        fz = func(z)
        if fy <= fz:
            b = z
        else:
            a = y
        return {
            "x": (a + b) / 2,
            "N": N,
            "k": k,
            "fib": fib_numbers,
            "Ln": [a, b],
            "R": 1/fibonachi(N)
        }
    

print(fib_method(0, 10, 0.5, 0.2))

    