from multiprocessing import Process, Manager
import time

def fibonacci(n):
    if(n == 1 or n == 0): return 1
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_mp(n, result):
    result[n] = fibonacci(n)

def compute_fibonaccis_multi_process(n):
    with Manager() as manager:      
        result = manager.dict()         # shared dictionary among processes
        processes = []

        for x in range(n):
            p = Process(target=fibonacci_mp, args=(x, result))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        return dict(result) 

if __name__ == "__main__":
    start = time.time()
    fibonaccis = compute_fibonaccis_multi_process(35)
    print([fibonaccis[x] for x in range(len(fibonaccis))])
    end = time.time()

    print('Multi Process Execution in: ', end-start,'s')