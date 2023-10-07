import cv2
import numpy as np

#SE ASIGNA LA IMAGENTXT
#################################################
cv2.imwrite('image.ppm', cv2.imread('waves.png'))
#################################################

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

# Nombre del archivo PPM de entrada
input_filename = 'image.ppm'

# Leer el archivo PPM
image_width, image_height, image_data = ppmread(input_filename)

# Se asigna el header
header = f'P6 {image_width} {image_height} {255}\n'

# Continuar con el código original para realizar las operaciones en la imagen en formato PPM
opc = int(input("Ingrese la cantidad de círculos a dibujar: "))
for n in range(0,opc):
	ent = [int(x) for x in input().split()]
	
	X = ent[0]		#punto x
	Y = ent[1]		#punto y
	r = ent[2]		#radio
	R = ent[3]		#rojo
	G = ent[4]		#verde
	B = ent[5]		#blanco 
	##DIBUJAR UN CIRCULO
	##validacionde de las entradas
	c = max(X - r, 0)
	e = min(X + r, image_width)
	d = max(Y - r, 0)
	h = min(Y + r, image_height)
	for x in range(c,e):
		for y in range(d,h):
			ind = 3 * (x + image_width * y)
			#Se verifica que el punto este dentro del circulo
			if (x - X) * (x - X) + (y - Y) * (y - Y) <= r * r:
				image_data[ind] = image_data[ind] ^ R              # rOJO
				image_data[ind + 1] = image_data[ind + 1]^G       # VERDE
				image_data[ind + 2] = image_data[ind + 2]^B        # AZUL

# Guardar la imagen resultante en formato PPM
with open('salida.ppm', 'wb') as f:
    f.write(bytearray(header, 'ascii'))
    f.write(image_data)

cv2.imwrite('salida.png', cv2.imread('salida.ppm'))