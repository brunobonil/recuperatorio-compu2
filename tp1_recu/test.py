from multiprocessing import Process, Pipe
import os
from typing import ByteString

# def leer(file, size):
#     fd = os.open(file, os.O_RDONLY)
#     while True:
#         lectura = os.read(fd, size)
#         if fd == b'' or len(lectura) < size:
#             break
#         print(lectura)
def escalar(b, scale):
    b = int.from_bytes(b, 'big')
    b = b * scale
    b = b.__round__()
    if b > 255:
        b = 255
    b = b.to_bytes(1, 'big')
    return b


def filter_gen(chunk, header, color):
    if color == 'r':
        fd = os.open('r_tux.ppm', os.O_RDWR | os.O_CREAT)
        os.write(fd, header)
        lista_chunk = []
        for i in chunk:
            lista_chunk.append(bytes([i]))
        for i in range(0, len(lista_chunk), 3):
            lista_chunk[i] = escalar(lista_chunk[i], 1)
            lista_chunk[i+1] = b'\x00'
            lista_chunk[i+2] = b'\x00'
        os.write(fd,b''.join(lista_chunk))
    
    if color == 'g':
        fd = os.open('g_tux.ppm', os.O_RDWR | os.O_CREAT)
        os.write(fd, header)
        lista_chunk = []
        for i in chunk:
            lista_chunk.append(bytes([i]))
        for i in range(1, len(lista_chunk), 3):
            lista_chunk[i-1] = b'\x00'
            lista_chunk[i] = escalar(lista_chunk[i], 1)
            lista_chunk[i+1] = b'\x00'
        for i in lista_chunk:
            os.write(fd, i)

    if color == 'b':
        fd = os.open('b_tux.ppm', os.O_RDWR | os.O_CREAT)
        os.write(fd, header)
        lista_chunk = []
        for i in chunk:
            lista_chunk.append(bytes([i]))
        for i in range(2, len(lista_chunk), 3):
            lista_chunk[i-2] = b'\x00'
            lista_chunk[i-1] = b'\x00'
            lista_chunk[i] = escalar(lista_chunk[i], 1)
        for i in lista_chunk:
            os.write(fd, i)

    
    
    

if __name__ == '__main__':
    
    size = 196624 - 15
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
    os.lseek(fd, len_header, 0)
    chunk = os.read(fd, size)
    os.lseek(fd, 0, 0)
    header = os.read(fd, len_header)
    filter_gen(chunk, header, 'r')



