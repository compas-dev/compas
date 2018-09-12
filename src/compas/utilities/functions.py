from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'fibonacci',
]


def fibonacci(n, memo={}):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 1
    if n not in memo:
        memo[n] = fibonacci(n - 2, memo) + fibonacci(n - 1, memo)
    return memo[n]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(fibonacci(100))
