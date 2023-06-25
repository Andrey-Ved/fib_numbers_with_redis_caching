from random import randint
from redis import Redis, ConnectionPool
from os import getpid

from collections.abc import Callable


def fibonacci_number_via_strings(n: int, r: Redis = None) -> int:
    assert 0 <= n <= 1000, \
        "expected that n in the range from 0 to 1000"

    if not r:
        r = Redis(
            host='localhost',
            port=6379,
            charset="utf-8",
            decode_responses=True
        )

    index = f'fib_{n}'
    fib_n = r.get(index)

    if not fib_n:
        if n <= 1:
            fib_n = n
        else:
            fib_n = (
                    fibonacci_number_via_strings(n - 1, r)
                    + fibonacci_number_via_strings(n - 2, r)
            )
        r.set(index, fib_n)
    else:
        fib_n = int(fib_n)

    return fib_n


redis_pool = None


def redis_conn_init():
    global redis_pool
    print("PID %d: initializing redis pool..." % getpid())
    redis_pool = ConnectionPool(
        host='localhost',
        port=6379,
        db=0)


def fibonacci_number_via_hash(n: int) -> int:
    assert 0 <= n <= 1000, \
        "expected that n in the range from 0 to 1000"

    global redis_pool

    if not redis_pool:
        redis_conn_init()

    with Redis(connection_pool=redis_pool) as r:
        fibonacci_series = r.hgetall('fibonacci_numbers')

        b_str_n = str(n).encode('UTF-8')

        if b_str_n not in fibonacci_series:
            if n <= 1:
                fibonacci_series[b_str_n] = b_str_n
            else:
                fibonacci_series[b_str_n] = str(
                    fibonacci_number_via_hash(n - 1)
                    + fibonacci_number_via_hash(n - 2)
                ).encode('UTF-8')

                r.hset(
                    name='fibonacci_numbers',
                    key=b_str_n,
                    value=fibonacci_series[b_str_n]
                )

    return int(fibonacci_series[b_str_n])


def fibonacci_number_demonstration(fibonacci_number: Callable) -> None:
    print()

    for i in range(5):
        n = randint(10, 20)
        print(n, "---", fibonacci_number(n))

    print(1000, "-", foo(1000))


def dict_print(dictionary: dict) -> None:
    [
        print(f'{k:>50} : {dictionary[k]}')
        for k in dictionary
    ]


def naive_redis_connect() -> None:
    r = Redis(
        host='localhost',
        port=6379,
        charset="utf-8",
        decode_responses=True
    )

    dict_print(r.config_get())

    print()
    print(r.set('foo', 'bar'))
    print(r.get('foo'))

    print(f'\nkeys:')
    [print(k) for k in r.keys()]


if __name__ == '__main__':
    naive_redis_connect()

    for foo in (
            fibonacci_number_via_strings,
            fibonacci_number_via_hash
    ):
        fibonacci_number_demonstration(foo)
