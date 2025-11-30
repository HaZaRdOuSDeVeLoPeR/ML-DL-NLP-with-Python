def subtract(*nums):
    first, *rest = nums
    diff = [first[0], first[1]]
    for num in rest:
        diff[0] -= num[0]
        diff[1] -= num[1]
    return f"{diff[0]} + {diff[1]}i"