from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    print("Inside Parent Process")
else:
    print("Inside Process: ",rank)

name = MPI.Get_processor_name()
print("Hello I am rank %d of %d with name %s" %(rank,size,name))
