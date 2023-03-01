from functools import wraps
from time import perf_counter


class timeit: # noqa
    def __init__(self, verbose=False, rounds=1):
        self.verbose = verbose
        self.rounds = max(rounds, 1)

    def __call__(self, function):
        @wraps(function)
        def wrapper_function(*args, **kwargs):
            start = perf_counter()
            result = None
            for _ in range(self.rounds):
                result = function(*args, **kwargs)
            elapsed = perf_counter() - start
            calls = ''
            if self.rounds > 1:
                calls = f'{self.rounds} calls '
                if self.verbose:
                    calls += 'to '
            if self.verbose:
                print(f"[@timeit] {calls}{function.__name__}("
                      f"{', '.join(str(arg) for arg in args)}"
                      f"{', ' if args and kwargs else ''}"
                      f"{', '.join(str(k) + '=' + str(v) for k, v in kwargs.items())}"
                      f") took {elapsed:.4} s")
            else:
                print(f"[@timeit] {calls}took {elapsed:.4} s")
            return result
        return wrapper_function


if __name__ == '__main__':

    @timeit()
    def f(a):
        return sum(range(a))


    @timeit(rounds=30000, verbose=True)
    def g(a, b=12):
        return a * b

    print('Running f')
    f(1_000_000)
    g(1_000, b=14)

