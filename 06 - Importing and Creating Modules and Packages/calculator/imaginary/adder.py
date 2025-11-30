def add(*nums):
    sum = [0,0]
    for num in nums:
        sum[0] += num[0]
        sum[1] += num[1]
    return f"{sum[0]} + {sum[1]}i"