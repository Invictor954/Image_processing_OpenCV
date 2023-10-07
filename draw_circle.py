import cv2
import numpy as np
import random
import time
import threading

#SE ASIGNA LA IMAGEN
#################################################
cv2.imwrite('image.ppm', cv2.imread('image.png'))
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

# Leer el archivo PPM e INICIALIZAR image_data
image_width, image_height, image_data = ppmread(input_filename)

# Se asigna el header
header = f'P6 {image_width} {image_height} {255}\n'


# Continuar con el código original para realizar las operaciones en la imagen en formato PPM
opc = random.randint(5, 20)
random_numbers = []

for n in range(0,opc):

	X = random.randint(0, image_width)		#punto x
	Y = random.randint(0, image_height)		#punto y
	r = random.randint(5, 170)		        #radio
	R = random.randint(0, 255)		        #rojo
	G = random.randint(0, 255)		        #verde
	B = random.randint(0, 255)		        #blanco 
	random_numbers.append((X, Y, r, R, G, B)) #guardamos los randoms para usarlo nuevamente
	#DIBUJAR UN CIRCULO

start = time.time()
#validacionde de las entradas
for X, Y, r, R, G, B in random_numbers:
    c = max(X - r, 0)
    e = min(X + r, image_width)
    d = max(Y - r, 0)
    h = min(Y + r, image_height)
    for x in range(c, e):
        for y in range(d, h):
            ind = 3 * (x + image_width * y)
            # Se verifica que el punto esté dentro del círculo
            if (x - X) * (x - X) + (y - Y) * (y - Y) <= r * r:
                image_data[ind] = image_data[ind] ^ R  # Rojo
                image_data[ind + 1] = image_data[ind + 1] ^ G  # Verde
                image_data[ind + 2] = image_data[ind + 2] ^ B  # Azul

# Guardar la imagen resultante en formato PPM
with open('salida.ppm', 'wb') as f:
    f.write(bytearray(header, 'ascii'))
    f.write(image_data)

cv2.imwrite('salida_c.png', cv2.imread('salida.ppm'))
end = time.time()
print(f"T.concurrente:\t\t\t {end - start} s")

#################################
#INICIALIZO NUEVAMENTE image_data
image_width, image_height, image_data = ppmread(input_filename)
#hilos//threads
def process_section(X, Y, r, R, G, B, image_data, image_width, image_height):
    c = max(X - r, 0)
    e = min(X + r, image_width)
    d = max(Y - r, 0)
    h = min(Y + r, image_height)
    for x in range(c, e):
        for y in range(d, h):
            ind = 3 * (x + image_width * y)
            # Se verifica que el punto esté dentro del círculo
            if (x - X) * (x - X) + (y - Y) * (y - Y) <= r * r:
                image_data[ind] = image_data[ind] ^ R  # Rojo
                image_data[ind + 1] = image_data[ind + 1] ^ G  # Verde
                image_data[ind + 2] = image_data[ind + 2] ^ B  # Azul

start = time.time()
threads = []

for X, Y, r, R, G, B in random_numbers:
    thread = threading.Thread(target=process_section, args=(X, Y, r, R, G, B, image_data, image_width, image_height))
    thread.start()
    threads.append(thread)

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()
    
# Guardar la imagen resultante en formato PPM
with open('salida.ppm', 'wb') as f:
    f.write(bytearray(header, 'ascii'))
    f.write(image_data)

cv2.imwrite('salida_h.png', cv2.imread('salida.ppm'))
end = time.time()
print(f"T.paralelismo de hilos:\t\t {end - start} s")

#################################
#INICIALIZO NUEVAMENTE image_data
image_width, image_height, image_data = ppmread(input_filename)
#paralelismo de datos
def process_section_pd(X, Y, r, R, G, B, section, image_width):
    c, e, d, h = section
    for x in range(c, e):
        for y in range(d, h):
            ind = 3 * (x + image_width * y)
            # Se verifica que el punto esté dentro del círculo
            if (x - X) * (x - X) + (y - Y) * (y - Y) <= r * r:
                image_data[ind] = image_data[ind] ^ R  # Rojo
                image_data[ind + 1] = image_data[ind + 1] ^ G  # Verde
                image_data[ind + 2] = image_data[ind + 2] ^ B  # Azul

# Dividir la imagen en secciones para paralelismo de datos
num_threads = 4  # Número de hilos para paralelismo
section_height = image_height // num_threads
sections = []

for i in range(num_threads):
    start_row = i * section_height
    end_row = (i + 1) * section_height if i < num_threads - 1 else image_height
    sections.append((0, image_width, start_row, end_row))

# Iniciar el procesamiento en paralelo
start = time.time()
threads = []

for X, Y, r, R, G, B in random_numbers:
    for section in sections:
        thread = threading.Thread(target=process_section_pd, args=(X, Y, r, R, G, B, section, image_width))
        thread.start()
        threads.append(thread)

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

# Guardar la imagen resultante en formato PPM
with open('salida.ppm', 'wb') as f:
    f.write(bytearray(header, 'ascii'))
    f.write(image_data)

cv2.imwrite('salida_pd.png', cv2.imread('salida.ppm'))
end = time.time()
print(f"T.paralelismo de datos:\t\t {end - start} s")

#################################
#INICIALIZO NUEVAMENTE image_data
image_width, image_height, image_data = ppmread(input_filename)
#paralelismo de datos numpy
def process_image(image_data, X, Y, r, R, G, B, image_width, image_height):
    # Convierte image_data en un arreglo NumPy
    image_data_np = np.frombuffer(image_data, dtype=np.uint8).reshape(image_height, image_width, 3)

    x, y = np.meshgrid(np.arange(image_width), np.arange(image_height))
    dist_squared = (x - X) ** 2 + (y - Y) ** 2
    mask = dist_squared <= r ** 2
    image_data_np[mask, 0] ^= R
    image_data_np[mask, 1] ^= G
    image_data_np[mask, 2] ^= B


start = time.time()

for X, Y, r, R, G, B in random_numbers:
    process_image(image_data, X, Y, r, R, G, B, image_width, image_height)

# Guardar la imagen resultante en formato PPM
with open('salida.ppm', 'wb') as f:
    f.write(bytearray(header, 'ascii'))
    f.write(image_data)

cv2.imwrite('salida_pd_np.png', cv2.imread('salida.ppm'))
end = time.time()
print(f"T.paralelismo de datos_np:\t {end - start} s")

#################################
#INICIALIZO NUEVAMENTE image_data
image_width, image_height, image_data = ppmread(input_filename)
#paralelismo de tareas
def apply_circular_filter(X, Y, r, R, G, B):
    c = max(X - r, 0)
    e = min(X + r, image_width)
    d = max(Y - r, 0)
    h = min(Y + r, image_height)
    
    for x in range(c, e):
        for y in range(d, h):
            ind = 3 * (x + image_width * y)
            # Se verifica que el punto esté dentro del círculo
            if (x - X) ** 2 + (y - Y) ** 2 <= r ** 2:
                image_data[ind] = image_data[ind] ^ R  # Rojo
                image_data[ind + 1] = image_data[ind + 1] ^ G  # Verde
                image_data[ind + 2] = image_data[ind + 2] ^ B  # Azul

start = time.time()
threads = []

for X, Y, r, R, G, B in random_numbers:
    thread = threading.Thread(target=apply_circular_filter, args=(X, Y, r, R, G, B))
    thread.start()
    threads.append(thread)

# Espera a que todos los hilos terminen
for thread in threads:
    thread.join()

# Guardar la imagen resultante en formato PPM
with open('salida.ppm', 'wb') as f:
    f.write(bytearray(header, 'ascii'))
    f.write(image_data)

cv2.imwrite('salida_pt.png', cv2.imread('salida.ppm'))

end = time.time()
print(f"T.paralelismo de tareas:\t {end - start} s")
