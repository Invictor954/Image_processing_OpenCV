import array

# PPM header
width = 1024 
height = 960    
header = f'P6 {width} {height} {255}\n'
# crear la matrizPPM en negro
img = array.array('B', [0, 0, 0] * width * height)
opc=int(input())

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
	c=X-r
	e=X+r
	d=Y-r
	h=Y+r
	if X-r < 0:
		c=0
	if Y-r < 0:
		d=0
	if X+r <0:
		e=0
	if Y+r <0:
		h=0
	if X+r > 960:
		e=960
	if Y+r > 1024:
		h=1024
	for x in range(c,e):
		for y in range(d,h):
			ind = 3 * (x * width + y)
			#Se verifica que el punto este dentro del circulo
			if (x-X)*(x-X)+(y-Y)*(y-Y)<=r*r :
				img[ind] = img[ind] ^ R              # rOJO
				img[ind + 1] = img[ind + 1]^G       # VERDE
				img[ind + 2] = img[ind + 2]^B        # AZUL


# aqui se genera la imagen
with open('salida.ppm', 'wb') as f:
	f.write(bytearray(header, 'ascii'))
	img.tofile(f)
