def subtract(*nums):
    first, *rest = nums
    for num in rest:
        first -= num
    return first