from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    input_string = "Hello, World!"
else:
    input_string = None

input_string = comm.bcast(input_string, root=0)

if rank != 0:
    comm.send(input_string, dest=rank, tag=rank)

else:
    for i in range(2, comm.Get_size()):
        input_string_to_send = input_string
        comm.send(input_string_to_send, dest=i, tag=i)

if rank != 0:
    input_string = comm.recv(source=0, tag=rank)
    
    if rank == 2:
        vowels = [char for char in input_string if char.lower() in 'aeiou']
        print(f"Process {rank}: Vowels in the string: {''.join(vowels)}")

    elif rank == 3:
        consonants = [char for char in input_string if char.isalpha() and char.lower() not in 'aeiou']
        print(f"Process {rank}: Consonants in the string: {''.join(consonants)}")
