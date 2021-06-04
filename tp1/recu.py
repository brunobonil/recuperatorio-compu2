#!/usr/bin/python3
import argparse
import multiprocessing
import os
from posix import O_RDONLY


def header(fd):
    header = os.read(fd, 30)
    header = (header.split(b'\n'))  # Crea una lista con los elementos del header separados por \n
    aux = 0
    for i in range(len(header)):
        if header[i-1] == b'255':   # Compara el último elemento tomado por 'i'
            break
        aux += (len(header[i]))
        aux += 1    # Representa los saltos de línea
    return aux

def insert_header(fd, long):
    os.lseek(fd, 0, 0)
    head = os.read(fd, long)
    new_file = os.open('r_dog.ppm', os.O_RDWR | os.O_CREAT)
    for i in head:
        os.write(new_file, bytes([i]))


def filtro_rojo(fd, name, size, inicio):
    size = size - (size % 3) 
    lectura = os.read(fd, size)
    name = 'r_' + name
    new_file = os.open(name, os.O_RDWR | os.O_CREAT)
    bytesarray = []
    for i in lectura:
        bytesarray.append(bytes([i]))
    while bytesarray:
        os.lseek(new_file, inicio, 0)
        lista_bytes = []
        j = b'\x00'
        while bytesarray:
            for i in bytesarray:
                if len(lista_bytes) == 3:
                    break
                lista_bytes.append(i)
            lista_bytes[0]
            os.write(new_file, i)
            try:
                lista_bytes[1]
            except:
                pass
            os.write(new_file, j)
            try:
                lista_bytes[2]
            except:
                pass
            os.write(new_file, j)
            lista_bytes.clear()
            if bytesarray:
                for _ in range(3):
                    bytesarray.pop(0)
            else:
                continue
        os.lseek(new_file, inicio + size, 0)
    
        


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Procesador de Imagenes')
    parser.add_argument('-r', '--red', help='Escala para rojo', type=float, default=1) 
    parser.add_argument('-g', '--green', help='Escala para verde', type=float, default=1)
    parser.add_argument('-b', '--blue', help='Escala para azul', type=float, default=1)
    parser.add_argument('-f', '--file', help='Archivo que se desea leer', type=str)
    parser.add_argument('-s', '--size', help='Bloque que desea leer', type=int)
    args = parser.parse_args()

    file = 'dog.ppm'
    fd = os.open(file, os.O_RDWR)
    tope = header(fd)
    insert_header(fd, tope)
    filtro_rojo(fd, file, 178829 , tope)
    
    