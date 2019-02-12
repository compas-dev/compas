from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'fibonacci',
    'binomial_coefficient'
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

def binomial_coefficient(n, k):
    """Binomial coefficient (n k), i.e. the number of possible combinations to select k elements among n ones.

    Parameters
    ----------
    n : int
        Number of elements.
    k : int
        Number of selected elements.

    Returns
    -------
    x : int
        The number of possible combinations.

    """

    k = min(k, n - k)
    x = 1
    y = 1
    i = n - k + 1

    while i <= n:
        x = (x * i) // y
        y += 1
        i += 1
    
    return x

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(fibonacci(100))

    print(binomial_coefficient(5, 3))
