import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
if __name__ == '__main__':
	plt.figure(num='Chensirui’s Paper Effciency',figsize=(6,5))
	plt.title('Chensirui’s Paper Effciency',color = 'red')
	t = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
	e = [0,0,0.1,0.2,0.3,3,7,9,20,50,100,500,1000,6000,200000,9000000,10000000]
	plt.plot(t, e,label='xy')
	plt.plot(t[0],e[0],label = 'START',color = 'r',markersize = 9,marker='o')
	plt.plot(t[len(t)-1],e[len(e)-1],label = 'END',color = 'g',markersize = 9,marker='o')
	plt.xlabel('Time(O’clock in a day)')
	plt.ylabel('Effciency')
	plt.legend(loc='best',edgecolor='blue')#图例设置
	plt.show()