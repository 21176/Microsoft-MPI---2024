from mpi4py import MPI

def bucket_sort(numbers):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Number of buckets
    num_buckets = 10
    
    # Initialize buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute numbers to buckets based on the digit
    for num in numbers:
        digit = int(str(num)[-1])
        bucket_id = digit % num_buckets
        buckets[bucket_id].append(num)
    
    # Sort numbers within each bucket
    for i in range(num_buckets):
        buckets[i].sort()
    
    # Gather sorted buckets to master process
    sorted_buckets = comm.gather(buckets, root=0)
    
    if rank == 0:
        sorted_numbers = []
        # Merge sorted buckets
        for bucket in sorted_buckets:
            for sublist in bucket:
                sorted_numbers.extend(sublist)
        print("Sorted numbers:", sorted_numbers)
    else:
        comm.gather(None, root=0)

if __name__ == "__main__":
    numbers = [170, 45, 75, 90, 802, 24, 2, 66]  # Example list of numbers
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    if rank == 0:
        print("Original numbers:", numbers)
    
    bucket_sort(numbers)
