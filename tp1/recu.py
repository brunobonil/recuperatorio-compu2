#!/usr/bin/python3
import argparse
from multiprocessing import Pipe, Process
import os
from posix import O_RDONLY
import sys

# def readfile(fd, chunk):
#     len_header = header(fd)
#     try:
#         os.lseek(fd, len_header[0], 0)
#         datos_leidos = os.read(fd, chunk)
#         return datos_leidos
#     except FileNotFoundError:
#         print('El archivo no se encuentra en el directorio')
#         sys.exit(1)

def header(fd):
    leer_header = os.read(fd, 50)
    leer_header = (leer_header.split(b'\n'))  # Crea una lista con los elementos del header separados por \n
    len_header = 0
    for i in range(len(leer_header)):
        if leer_header[i-1] == b'255':   # Compara el último elemento tomado por 'i'
            break
        len_header += (len(leer_header[i]))
        len_header += 1    # Representa los saltos de línea
    os.lseek(fd, 0, 0)
    header = os.read(fd, len_header)
    return [len_header, header]
    
def filtro_rojo(header, name, scale, size, conn):
    name = 'r_' + name
    new_file = os.open(name, os.O_RDWR | os.O_CREAT)
    len_encab, encab = header
    os.write(new_file, encab)
    while True:
        bytes_recived = conn.recv()
        # Modifica los valores G y B de cada pixel y lo escribe
        bytesarray = []
        for i in bytes_recived:
            bytesarray.append(bytes([i]))
        os.lseek(new_file, len_encab, 0)
        lista_bytes = []
        j = b'\x00'
        x = 0
        while True:
            if bytesarray == []:
                break
            for i in bytesarray:
                while len(lista_bytes) != 3:
                    lista_bytes.append(i)
            # Calcula el valor del byte en decimal, lo escala al valor de r ingresado
            # Y lo devuelve en bytes
            x = int.from_bytes(lista_bytes[0], 'big')
            x = x * scale
            x = x.__round__()
            if x > 255:
                x = 255
            x = x.to_bytes(1, 'big')
            os.write(new_file, x)
            os.write(new_file, j)
            os.write(new_file, j)
            lista_bytes.clear()
            if bytesarray != []:
                for _ in range(3):
                    bytesarray.pop(0)

        if bytes_recived == b'' or len(bytes_recived) < size:
            break

def filtro_verde(fd, name, size, inicio):
    header = os.read(fd, 30)
    header = (header.split(b'\n'))  # Crea una lista con los elementos del header separados por \n
    len_header = 0
    for i in range(len(header)):
        if header[i-1] == b'255':   # Compara el último elemento tomado por 'i'
            break
        len_header += (len(header[i]))
        len_header += 1    # Representa los saltos de línea

    os.lseek(fd, 0, 0)
    head = os.read(fd, len_header)
    name = 'g_' + name
    new_file = os.open(name, os.O_RDWR | os.O_CREAT)
    for i in head:
        os.write(new_file, bytes([i]))

    size = size - (size % 3) 
    lectura = os.read(fd, size)
    new_file = os.open(name, os.O_RDWR)
    bytesarray = []
    for i in lectura:
        bytesarray.append(bytes([i]))
    while bytesarray:
        os.lseek(new_file, len_header, 0)
        lista_bytes = []
        j = b'\x00'
        while bytesarray:
            for i in bytesarray:
                if len(lista_bytes) == 3:
                    break
                lista_bytes.append(i)
            # Calcula el valor del byte en decimal, lo escala al valor de r ingresado
            # Y lo devuelve en bytes
            x = int.from_bytes(lista_bytes[0], 'big')
            x = x * scale
            x = x.__round__()
            if x > 255:
                x = 255
            x = x.to_bytes(1, 'big')
            os.write(new_file, j)
            os.write(new_file, x)
            os.write(new_file, j)
            lista_bytes.clear()
            if bytesarray:
                for _ in range(3):
                    bytesarray.pop(0)
    
def filtro_azul(fd, name, size, inicio):
    header = os.read(fd, 30)
    header = (header.split(b'\n'))  # Crea una lista con los elementos del header separados por \n
    len_header = 0
    for i in range(len(header)):
        if header[i-1] == b'255':   # Compara el último elemento tomado por 'i'
            break
        len_header += (len(header[i]))
        len_header += 1    # Representa los saltos de línea

    os.lseek(fd, 0, 0)
    head = os.read(fd, len_header)
    name = 'b_' + name
    new_file = os.open(name, os.O_RDWR | os.O_CREAT)
    for i in head:
        os.write(new_file, bytes([i]))

    size = size - (size % 3) 
    lectura = os.read(fd, size)
    new_file = os.open(name, os.O_RDWR)
    bytesarray = []
    for i in lectura:
        bytesarray.append(bytes([i]))
    while bytesarray:
        os.lseek(new_file, len_header, 0)
        lista_bytes = []
        j = b'\x00'
        while bytesarray:
            for i in bytesarray:
                if len(lista_bytes) == 3:
                    break
                lista_bytes.append(i)
            # Calcula el valor del byte en decimal, lo escala al valor de r ingresado
            # Y lo devuelve en bytes
            x = int.from_bytes(lista_bytes[0], 'big')
            x = x * scale
            x = x.__round__()
            if x > 255:
                x = 255
            x = x.to_bytes(1, 'big')
            os.write(new_file, j)
            os.write(new_file, j)
            os.write(new_file, x)
            lista_bytes.clear()
            if bytesarray:
                for _ in range(3):
                    bytesarray.pop(0)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Procesador de Imagenes')
    parser.add_argument('-r', '--red', help='Escala para rojo', type=float, default=1) 
    parser.add_argument('-g', '--green', help='Escala para verde', type=float, default=1)
    parser.add_argument('-b', '--blue', help='Escala para azul', type=float, default=1)
    parser.add_argument('-f', '--file', help='Archivo que se desea leer', type=str)
    parser.add_argument('-s', '--size', help='Bloque que desea leer', type=int)
    args = parser.parse_args()

    fd = os.open(args.file, os.O_RDWR)
    lista_header = header(fd)

    parent_conn = []
    child_conn = []
    for _ in range(3):
        p, h = Pipe()
        parent_conn.append(p)
        child_conn.append(h)

    args.size = args.size - (args.size % 3)
    p1 = Process(target=filtro_rojo, args=(lista_header, args.file, args.red, args.size, child_conn[0]))
    p1.start()    
    
    os.lseek(fd, lista_header[0], 0)
    while True:
        lectura = os.read(fd, args.size)
        parent_conn[0].send(lectura)

        if lectura == b'' or len(lectura) < args.size:
            break
    p1.join()
    print('Exito')



    