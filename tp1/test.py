import os
from posix import O_RDONLY

f = os.open('text.txt', os.O_RDONLY)
size = 3
print(f.real)
#while x: 
#    print(os.read(f, size))
