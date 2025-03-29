# coding:utf-8

from gc import collect
from tracemalloc import start
from tracemalloc import take_snapshot

start()


def top_malloc(top: int = 10):
    number: int = max(top, 3)
    print(f"[ Top {number} ]")
    snapshot = take_snapshot()
    statuses = snapshot.statistics("lineno")
    for stat in statuses:
        if number > 0:
            print(stat)
            number -= 1
        del stat
    del statuses
    del snapshot
    collect()
