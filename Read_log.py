import re
def read():
	x = [0]
	y = [0]
	z = [0]
	file = open("log.txt",'r') 
	lines=file.readlines()
	for line in lines:
		line = line.strip()
		out = re.split('X=|,Y=|,Z=',line)
		out1 = float(out[1])
		out2 = float(out[2])
		out3 = float(out[3])
		x.append(out1)
		y.append(out2)
		z.append(out3)
	file.close()
	x.remove(0)
	y.remove(0)
	z.remove(0)
	return x,y,z
