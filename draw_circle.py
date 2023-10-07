import array

# PPM header
width = 1024 
height = 960    
header = f'P6 {width} {height} {255}\n'
# crear la matrizPPM en negro
img = array.array('B', [0, 0, 0] * width * height)
opc=int(input())


