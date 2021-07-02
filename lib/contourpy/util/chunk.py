import math


def calc_chunk_sizes(chunk_size, chunk_count, total_chunk_count, ny, nx):
    if sum([chunk_size is not None, chunk_count is not None, total_chunk_count is not None]) > 1:
        raise ValueError("Only one of chunk_size, chunk_count and total_chunk_count should be set")

    if total_chunk_count is not None:
        max_chunk_count = (nx-1)*(ny-1)
        total_chunk_count = min(max(total_chunk_count, 1), max_chunk_count)
        if total_chunk_count == 1:
            chunk_size = 0
        elif total_chunk_count == max_chunk_count:
            chunk_size = (1, 1)
        else:
            factors = two_factors(total_chunk_count)
            if ny > nx:
                chunk_count = factors
            else:
                chunk_count = (factors[1], factors[0])

    if chunk_count is not None:
        if isinstance(chunk_count, tuple):
            y_chunk_count, x_chunk_count = chunk_count
        else:
            y_chunk_count = x_chunk_count = chunk_count
        x_chunk_count = min(max(x_chunk_count, 1), nx-1)
        y_chunk_count = min(max(y_chunk_count, 1), ny-1)
        chunk_size = (math.ceil((ny-1) / y_chunk_count), math.ceil((nx-1) / x_chunk_count))

    if chunk_size is None:
        y_chunk_size = x_chunk_size = 0
    elif isinstance(chunk_size, tuple):
        y_chunk_size, x_chunk_size = chunk_size
    else:
        y_chunk_size = x_chunk_size = chunk_size

    if x_chunk_size < 0 or y_chunk_size < 0:
        raise ValueError("chunk_size cannot be negative")

    return y_chunk_size, x_chunk_size


# Splits integer n into two integer factors that are as close as possible to the sqrt of n, and
# returns them in decreasing order.  Worst case returns (n, 1).
def two_factors(n):
    i = math.ceil(math.sqrt(n))
    while n % i != 0:
        i -= 1
    j = n // i
    if i > j:
        return i, j
    else:
        return j, i
