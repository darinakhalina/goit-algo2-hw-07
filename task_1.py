import random
import time
from collections import OrderedDict


def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


class LRUCache:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, condition_func):
        keys_to_remove = [k for k in self.cache.keys() if condition_func(k)]
        for k in keys_to_remove:
            del self.cache[k]


def range_sum_with_cache(array, L, R, lru_cache):
    cached_value = lru_cache.get((L, R))
    if cached_value is not None:
        return cached_value

    s = sum(array[L : R + 1])
    lru_cache.put((L, R), s)
    return s


def update_with_cache(array, index, value, lru_cache):
    array[index] = value

    def condition(key):
        L, R = key
        return L <= index <= R

    lru_cache.invalidate(condition)


def main():
    N = 100_000
    Q = 50_000
    CAPACITY = 1000

    array = [random.randint(1, 1000) for _ in range(N)]

    queries = []
    for _ in range(Q):
        query_type = random.choice(["Range", "Update"])
        if query_type == "Range":
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 1000)
            queries.append(("Update", index, value))

    start_time_no_cache = time.perf_counter()

    array_no_cache = array[:]
    for q in queries:
        if q[0] == "Range":
            _, L, R = q
            _ = range_sum_no_cache(array_no_cache, L, R)
        else:
            _, idx, val = q
            update_no_cache(array_no_cache, idx, val)

    end_time_no_cache = time.perf_counter()
    total_time_no_cache = end_time_no_cache - start_time_no_cache

    start_time_cache = time.perf_counter()

    array_with_cache = array[:]
    lru_cache = LRUCache(capacity=CAPACITY)

    for q in queries:
        if q[0] == "Range":
            _, L, R = q
            _ = range_sum_with_cache(array_with_cache, L, R, lru_cache)
        else:
            _, idx, val = q
            update_with_cache(array_with_cache, idx, val, lru_cache)

    end_time_cache = time.perf_counter()
    total_time_cache = end_time_cache - start_time_cache

    print(f"Час виконання без кешування: {total_time_no_cache:.3f} cекунд")
    print(f"Час виконання з LRU-кешем: {total_time_cache:.3f} cекунд")


if __name__ == "__main__":
    main()
