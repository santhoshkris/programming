

def rec_fib(n):
    '''Nth fibonacci number using recursion'''
    if n <= 2:
        return 1
    return rec_fib(n-1) + rec_fib(n-2)


def gen_fib(n):
    """Fibonacci series generator"""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
        yield a

# print(rec_fib(8))


for i in gen_fib(8):
    print(i)
