from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:  
    if rank == 0:
        print("Error")
    MPI.Finalize()

if rank == 0:
    n = 10
    rand_array = np.random.randint(0,100, size = n)
    print("Master process: ", rand_array)

    comm.send(rand_array, dest = 1)

    less_than_50 = np.count_nonzero(rand_array < 50)
    print("Master process: ",less_than_50) 

    slave_result = comm.recv(source = 1)
    print("Master Process: ",slave_result)

elif rank == 1:
    rand_array = comm.recv(source = 0)
    print("Slave process: ",rand_array)

    sum_result = np.sum(rand_array)
    print("Slave result: ", sum_result)

    comm.send(sum_result, dest = 0)

MPI.finalize()


