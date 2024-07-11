# program to experiment send-recv functions with parallet time
from mpi4py import MPI

a = MPI.Wtime()
print("Welcome")
b = MPI.Wtime()

ts = b - a

comm = MPI.COMM_WORLD
x = MPI.Wtime()
rank = comm.Get_rank()

if rank == 0:
    a = {'Jan':1, 'Feb': 2}
    comm.send("Hi", dest = 1, tag = 1)
    comm.send(a,dest = 2)

if rank == 1:
    d = comm.recv(source = 0, tag = 1)
    print("The received message at process 1 is %s %d")

if rank == 2:
    b = comm.recv(source = 0)
    print("received from process 0", b)

if rank == 0:
    y = MPI.Wtime()
    tp = y - x
    sp = ts / tp
    eff = sp / 2 * 100
    print("Speed up factor: ",sp)
    print("Efficiency: ",eff)
    
