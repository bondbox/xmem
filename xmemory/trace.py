# coding:utf-8

from gc import collect
from tracemalloc import start
from tracemalloc import stop
from tracemalloc import take_snapshot


def top_malloc(top: int = 10):
    start()
    number: int = max(top, 3)
    print(f"[ Top {number} ]")
    snapshot = take_snapshot()
    statuses = snapshot.statistics("lineno")
    for stat in statuses:
        if number > 0:
            print(stat)
            number -= 1
    collect()
    stop()
