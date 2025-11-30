from concurrent.futures import ProcessPoolExecutor
import time

# simulating a cpu heavy task
def compute_fibonacci(n):
    if n <= 1:
        return 1
    else: return compute_fibonacci(n-1) + compute_fibonacci(n-2)

# Computing 1st 35 Fibonacci Numbers

if __name__ == "__main__":
    executor = ProcessPoolExecutor(max_workers = 8)
    start = time.time()

    processes = [executor.submit(compute_fibonacci, i) for i in range(35)]
    results = [process.result() for process in processes]
    print(results)
    end = time.time()

    executor.shutdown(wait = True)
    print('Multi-Process Version finished in :', end-start, 's')