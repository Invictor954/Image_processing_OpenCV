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
	
	X = ent[0]
	Y = ent[1]
	r = ent[2]
	R = ent[3]
	G = ent[4]
	B = ent[5]


