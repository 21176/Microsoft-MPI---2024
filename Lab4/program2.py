from mpi4py import MPI

def producer(n, rank, size):
    queue = []
    for i in range(rank + 1, n + 1, size):
        queue.append(i)
    return queue

def customer(queue):
    result = 1
    for num in queue:
        result = result * num
    return result

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    n = 10

    localQueue = producer(n, rank, size)
    localResult = customer(localQueue)

    if rank == 0:
        print(f"(n)! =", localResult)

        