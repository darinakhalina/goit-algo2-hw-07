import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

from splaytree import SplayTree


@lru_cache(maxsize=None)
def fibonacci_lru(n: int):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n: int, splay_tree: SplayTree):
    if n < 2:
        return n
    cached_result = splay_tree.find(n)
    if cached_result is not None:
        return cached_result
    result = fibonacci_splay(n - 1, splay_tree) + fibonacci_splay(n - 2, splay_tree)
    splay_tree.insert(n, result)
    return result


def print_results(rows: list[tuple[int, int, int]]):
    print("\n")
    print("{:<10}{:<20}{:<20}".format("n", "LRU Cache Time (s)", "Splay Tree Time (s)"))
    print("-" * 50)

    for row in rows:
        n, lru_time, splay_time = row
        print("{:<10}{:<20.8f}{:<20.8f}".format(n, lru_time, splay_time))


def show_graph(values, lru_results, splay_results):
    plt.plot(
        values,
        lru_results,
        "-o",
        label="LRU Cache",
    )
    plt.plot(values, splay_results, "-x", label="Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()


def main():
    numbers = range(0, 1000, 50)
    lru_results, splay_results, results_rows = [], [], []
    splay_tree = SplayTree()

    for n in numbers:
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=100)
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=100)
        lru_results.append(lru_time)
        splay_results.append(splay_time)
        results_rows.append((n, lru_time, splay_time))

    print_results(results_rows)
    show_graph(numbers, lru_results, splay_results)


if __name__ == "__main__":
    main()
