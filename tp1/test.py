from multiprocessing import Process, Pipe
import os

# def leer(file, size):
#     fd = os.open(file, os.O_RDONLY)
#     while True:
#         lectura = os.read(fd, size)
#         if fd == b'' or len(lectura) < size:
#             break
#         print(lectura)

def filtro_rojo(chunk, header):
    fd = os.open('r_tux.ppm', os.O_RDWR | os.O_CREAT)
    os.write(fd, header)
    lista_chunk = []
    for i in chunk:
        lista_chunk.append(bytes([i]))
    
    

if __name__ == '__main__':
    size = 20
    fd = os.open('tux.ppm', os.O_RDONLY)
    size = size - (size % 3)
    f = os.read(fd, size)
    header = f
    header = (header.split(b'\n'))  # Crea una lista con los elementos del header separados por \n
    len_header = 0
    for i in range(len(header)):
        if header[i-1] == b'255':   # Compara el último elemento tomado por 'i'
            break
        len_header += (len(header[i]))
        len_header += 1
    os.lseek(fd, 0, 0)
    chunk = os.read(fd, size)
    os.lseek(fd, 0, 0)
    header = os.read(fd, len_header)
    filtro_rojo(chunk, header)





    

    