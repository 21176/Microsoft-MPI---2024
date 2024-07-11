from mpi4py import MPI

def parallel_sum(numbers):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    chunk_size = len(numbers) // size
    start = rank * chunk_size
    end = start + chunk_size if rank < size - 1 else len(numbers)
    
    partial_sum = sum(numbers[start:end])
    
    if rank == 0:
        total_sum = partial_sum
        for i in range(1, size):
            partial_sum = comm.recv(source=i)
            total_sum += partial_sum
        print("Final Sum:", total_sum)
    else:
        comm.send(partial_sum, dest=0)

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # Your list of numbers
    
    parallel_sum(numbers)


