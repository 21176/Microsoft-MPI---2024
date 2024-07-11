from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    # Master Process (Process 1)
    input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
else:
    input_list = None

# Broadcast the input list to all processes
input_list = comm.bcast(input_list, root=0)

# Calculate the sum of the entire list
sum_total = sum(input_list)
if rank == 0:
    print(f"Process {rank}: Master process - Sum of all elements = {sum_total}")

    # Send the input list to other processes
    for i in range(1, comm.Get_size()):
        comm.send(input_list, dest=i, tag=i)

else:
    # Receive the input list from the master process
    input_list = comm.recv(source=0, tag=rank)

    # Calculate and print the sum of even and odd elements
    even_sum = sum(x for x in input_list if x % 2 == 0)
    odd_sum = sum(x for x in input_list if x % 2 != 0)

    if rank == 2:
        print(f"Process {rank}: Sum of even elements = {even_sum}")
    elif rank == 3:
        print(f"Process {rank}: Sum of odd elements = {odd_sum}")
