import timeit
import functools
import matplotlib.pyplot as plt


class SplayNode:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:

    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if key == self.root.key:
            return

        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def search(self, key):
        if self.root is None:
            return None

        self.root = self._splay(self.root, key)
        return self.root.value if self.root.key == key else None


@functools.lru_cache(maxsize=None)
def fibonacci_lru(n):

    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):

    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value

    if n < 2:
        tree.insert(n, n)
        return n

    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result



test_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in test_values:
    tree = SplayTree()
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)

    lru_times.append(lru_time)
    splay_times.append(splay_time)

# Виведення таблиці
print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
print("-" * 50)
for i in range(len(test_values)):
    print(f"{test_values[i]:<10}{lru_times[i]:<20.8f}{splay_times[i]:<20.8f}")

# Побудова графіка
plt.figure(figsize=(10, 5))
plt.plot(test_values, lru_times, marker="o", linestyle="-", label="LRU Cache")
plt.plot(test_values, splay_times, marker="s", linestyle="--", label="Splay Tree")
plt.xlabel("n (номер числа Фібоначчі)")
plt.ylabel("Час виконання (секунди)")
plt.title("Порівняння продуктивності LRU Cache та Splay Tree")
plt.legend()
plt.grid()
plt.show()
