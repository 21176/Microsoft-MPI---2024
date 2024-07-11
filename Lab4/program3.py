from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def generateMatrix(n):
    return np.random.randint(1, 10, (n, n))
def addMatrices(matrix1, matrix2):
    return np.add(matrix1, matrix2)
def masterProcess(n, P):
    matrix = generateMatrix(n)
    chunkSize = n // P
    for i in range(1, P):
        startRow = i * chunkSize
        endRow = startRow + chunkSize
        comm.send(matrix[startRow:endRow], dest = i)

    partialSum = np.zeros((n,n))
    for i in range(1, P):
        partialSum += comm.recv(source = i)
    finalSum = np.sum(partialSum)
    print(f"Final sum of the matrix: {finalSum}")
def slaveProcess():
    matrixChunk = comm.recv(source = 0)
    partialSum = np.sum(matrixChunk)
    comm.send(partialSum, dest = 0)
    print(f"Slave process {rank} has completed the task.")
n = 5
p = 4
if rank == 0:
    masterProcess(n,  p)
else:
    slaveProcess()    
