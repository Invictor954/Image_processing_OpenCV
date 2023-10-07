import cv2
import numpy as np
import random
import time


cv2.imwrite('image.ppm', cv2.imread('image.png'))


# Función para leer un archivo PPM en formato binario (P6)
def ppmread(filename):
    with open(filename, 'rb') as f:
        # Leer el encabezado del archivo PPM
        line = f.readline().decode('latin-1')
        if not line.startswith('P6'):
            print("ERROR: Expected PPM file to start with P6")
            return None

        line = f.readline().decode('latin-1')
        dims = line.split()
        width, height = int(dims[0]), int(dims[1])

        line = f.readline().decode('latin-1')
        if not line.startswith('255'):
            print("ERROR: Expected 8-bit PPM with MAXVAL=255")
            return None
        # Leer los datos de la imagen
        image_data = bytearray(f.read(width * height * 3))
        return width, height, image_data