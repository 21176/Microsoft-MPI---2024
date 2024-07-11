from mpi4py import MPI

def partialFactorial(start, end):
    result = 1
    for i in range(start, end + 1):
        result = result * i
    return result

def computeFactorial(n, rank, size):
    localResult = 1
    if rank == 0:
        mid = n // 2
        leftResult = partialFactorial(1,mid)
        rightResult = partialFactorial(mid + 1, n)
        localResult = leftResult + rightResult
    return localResult

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    n = 10

    localResult = computeFactorial(n, rank, size)
    totalResult = comm.reduce(localResult, op = MPI.PROD, root = 0)

    if rank == 0:
        print(f"(n)! =", totalResult)