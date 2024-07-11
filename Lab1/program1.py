from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()

print("Processor name: ",name)
print("Rank: ",rank)
print("Size: ",size)

if rank == 0:
    print("Inside parent process")
else:
    print("Inside process: ", rank)