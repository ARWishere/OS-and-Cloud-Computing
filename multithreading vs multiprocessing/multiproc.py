import time
import multiprocessing

def sum_of_squares(n):
    return sum([i * i for i in range(n)])

def sum_of_squares_proc(n, result_list, index):
    result_list[index] = sum(i * i for i in range(n))

def main():
    N = 10 ** 7  # Large number for heavy computation
    start_time = time.time()


    results = [sum_of_squares(N) for _ in range(4)]
    end_time = time.time()
    print("Sequential Execution Time:", end_time - start_time)

    num_processes = 4  # num of processes to use
    start_time = time.time()
    processes = []
    manager = multiprocessing.Manager()
    results = manager.list([0] * num_processes)

    for i in range(num_processes):
        p = multiprocessing.Process(target=sum_of_squares_proc, args=(N, results, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print("Parallel Execution Time:", end_time - start_time)

if __name__ == "__main__":
    main()
