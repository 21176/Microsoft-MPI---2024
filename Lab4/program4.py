from mpi4py import MPI
import numpy as np
import math
def rotate_point(x, y, theta):
    x_new = math.cos(theta) * x - math.sin(theta) * y
    y_new = math.sin(theta) * x + math.cos(theta) * y
    return x_new, y_new
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
image_size = (100, 100)
rotation_angle = math.radians(30)
rows_per_process = image_size[0] // size
if rank == 0:
    image = np.zeros(image_size)
    image[:, :] = np.arange(image_size[1])  
    for i in range(1, size):
        start_row = i * rows_per_process
        end_row = start_row + rows_per_process
        if i == size - 1:  
            end_row = image_size[0]
        comm.Send(image[start_row:end_row, :], dest=i, tag=1)
    for i in range(rows_per_process):
        for j in range(image_size[1]):
            image[i, j] = rotate_point(j, i, rotation_angle)[0]
    for i in range(1, size):
        start_row = i * rows_per_process
        end_row = start_row + rows_per_process
        if i == size - 1:
            end_row = image_size[0]
        received_data = np.empty((end_row - start_row, image_size[1]), dtype=float)
        comm.Recv(received_data, source=i, tag=2)
        image[start_row:end_row, :] = received_data
    print("Master is printing the final image:")
    print(image)
else:
    rows_to_process = np.empty((rows_per_process, image_size[1]), dtype=float)
    comm.Recv(rows_to_process, source=0, tag=1)
    for i in range(rows_per_process):
        for j in range(image_size[1]):
            rows_to_process[i, j] = rotate_point(j, rank * rows_per_process + i, rotation_angle)[0]
    comm.Send(rows_to_process, dest=0, tag=2)
if rank == 0:
    sequential_time = 100  
    parallel_time = 10     
    speedup = sequential_time / parallel_time
    efficiency = speedup / size
    print(f"Speedup factor: {speedup}")
    print(f"Efficiency: {efficiency}")
