import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import Read_log
import kalman
def find_nzero(t):
	for i in range(0,len(t)):
		if t[i]!= 0:
			return i
	return -1
def avg(x,num):
	rx = []
	for i in range(int(len(x)/num)):
		temp = 0
		count = 0
		for j in range(num):
			if (x[i*num+j] == 0):
				count = count + 1
			temp = float(temp) + x[i*num+j]
		if num -count == 0:
			count = 0
		temp = format(temp/(num),'.2f')
		rx.append(float(temp))
	return rx
def to_X(ax,t):#加速度数据转化为位移数据
	dx = [0]
	vx = [0]
	for i in range(len(ax)):
		dxx = float(dx[len(dx)-1]) + float(vx[len(vx)-1])*t + float(0.5 * ax[i] * t * t) #当前x轴位移dxx，改变前x轴位置dx[len(dx)-1]，初速度为vx[len(vx)-1]，此次位移改变为vt+ 1/2*a*t^2
		dxx = format(dxx, '.3f')
		vx0 = vx[len(vx)-1] + ax[i] * t
		vx0 = format(vx0, '.3f')
		#降低速度干扰
		r = 0.4
		if i-1 >= 0 and i+1 < len(ax):
			if (-r <ax[i-1]<r and -r<ax[i]<r and -r<ax[i+1]<r):
				vx0 = 0
		dx.append(float(dxx))
		vx.append(float(vx0))#求出末速度，放入x轴速度list中
	return dx
def to_V(ax,t):
	vx = [0]
	for i in range(len(ax)):
		#dxx = float(dx[len(dx)-1]) + float(vx[len(vx)-1])*t + float(0.5 * ax[i] * t * t) #当前x轴位移dxx，改变前x轴位置dx[len(dx)-1]，初速度为vx[len(vx)-1]，此次位移改变为vt+ 1/2*a*t^2
		#dxx = format(dxx, '.3f')
		vx0 = vx[len(vx)-1] + ax[i] * t
		vx0 = format(vx0, '.3f')
		#降低速度干扰
		r = 0.4
		if i-1 >= 0 and i+1 < len(ax):
			if (-r <ax[i-1]<r and -r<ax[i]<r and -r<ax[i+1]<r):
				vx0 = 0
		#dx.append(float(dxx))
		vx.append(float(vx0))#求出末速度，放入x轴速度list中
	return vx
def filter_a(ax):
	result1 = [] 
	result2 = []
	#计算出平均值（过滤掉小于f1的加速度）
	f1 = 0.2
	for axx in ax:
		if (axx>f1 or axx<-f1) :
			result1.append(axx)
	avg = 0
	for axx in result1:
		avg = avg + abs(axx)
	if len(result1) != 0:
		avg = abs(avg/len(result1))
	else:
		avg = 1
	#avg是过滤的阈值，小于这个阈值的加速度一律被定为0，防止小的加速度偏移
	ff2 = 0.1#过滤掉小于ff2*avg的所有加速度数值
	#print("avg",avg*ff2)
	for axx in ax :
		f2 = abs(avg*ff2)
		if (-f2<axx<f2):
			axx =0
		result2.append(axx)
	#print("result2",result2)
	return result2
def set_data():#读取加速度数据
	t = 0.1 #采集延时
	ax,ay,az = Read_log.read()
	#低通滤波器
	ax = filter_a(ax)
	ay = filter_a(ay)
	az = filter_a(az)
	#卡尔曼滤波器
	ax = kalman.K(ax)
	ay = kalman.K(ay)
	az = kalman.K(az)
	#每n个数据求一个平均值
	n = 10
	ax = avg(ax,n)
	ay = avg(ay,n)
	az = avg(az,n)
	#print ("ax",ax)
	#print ("ay",ay)
	#print ("az",az)
	dx = to_X(ax,t)
	dy = to_X(ay,t)
	dz = to_X(az,t)
	return dx,dy,dz
'''
	dx = [0]
	dy = [0]
	dz = [0]
	vx = [0]
	vy = [0]
	vz = [0]
	for axx in ax:
		dxx = float(dx[len(dx)-1]) + float(vx[len(vx)-1])*t + float(0.5 * axx * t * t) #当前x轴位移dxx，改变前x轴位置dx[len(dx)-1]，初速度为vx[len(vx)-1]，此次位移改变为vt+ 1/2*a*t^2
		dxx = format(dxx, '.3f')
		dx.append(float(dxx))
		vx0 = vx[len(vx)-1] + axx * t
		vx0 = format(vx0, '.3f')
		vx.append(float(vx0))#求出末速度，放入x轴速度list中
	for ayy in ay:
		dyy = float(dy[len(dy)-1]) + float(vy[len(vy)-1])*t + float(0.5 * ayy * t * t) #当前y轴位移dyy，改变前y轴位置dy[len(dy)-1]，初速度为vy[len(vy)-1]，此次位移改变为vt+ 1/2*a*t^2
		dyy = format(dyy, '.3f')
		dy.append(float(dyy))
		vy0 = vy[len(vy)-1] + ayy * t
		vy0 = format(vy0, '.3f')
		vy.append(float(vy0))#求出末速度，放入y轴速度list中
	for azz in az:
		dzz = float(dz[len(dz)-1]) + float(vz[len(vz)-1])*t + float(0.5 * azz * t * t) #当前z轴位移dzz，改变前z轴位置dz[len(dz)-1]，初速度为vz[len(vz)-1]，此次位移改变为vt+ 1/2*a*t^2
		dzz = format(dzz, '.3f') 
		dz.append(float(dzz))
		vz0 = vz[len(vz)-1] + azz * t
		vz0 = format(vz0, '.3f')
		vz.append(float(vz0))#求出末速度，放入z轴速度list中
'''
def get_V():
	t = 0.1 #采集延时
	ax,ay,az = Read_log.read()
	ax = filter_a(ax)
	ay = filter_a(ay)
	az = filter_a(az)
	#每n个数据求一个平均值
	n = 10
	ax = avg(ax,n)
	ay = avg(ay,n)
	az = avg(az,n)
	#print ("ax",ax)
	#print ("ay",ay)
	#print ("az",az)
	dx = to_V(ax,t)
	dy = to_V(ay,t)
	dz = to_V(az,t)
	return dx,dy,dz
def gesture_re1(change_x,change_y,change_z):#模型一判断
	type = 0
	if change_x<(0.1*change_z) and change_y<(0.1*change_z):#仅在z轴上有运动
		type = "z"
	elif change_x<(0.1*change_y) and change_z<(0.1*change_y):#仅在y轴上有运动
		type = "y"
	elif change_y<(0.1*change_x) and change_z<(0.1*change_x):#仅在z轴上有运动
		type = "x"
	return type
def gesture_re2(change_x,change_y,change_z):
	vx,vy,vz = get_V()
	#print(vx)
	#print(vy)
	#print(vz)
	x_nzero = find_nzero(vx)
	y_nzero = find_nzero(vy)
	z_nzero = find_nzero(vz)
	if (min(change_x,change_y,change_z) == change_y):#在xz平面上
		#print("xz")
		if x_nzero < z_nzero:#判断先向哪一个轴运动
			if (vx[x_nzero] < 0) :#判断运动方向
				print("先沿着x轴负方向运动")
			else:
				print("先沿着x轴正方向运动")
			if (vz[z_nzero] < 0) :#判断运动方向
				print("然后沿着z轴负方向运动")
			else:
				print("然后沿着z轴正方向运动")
		else:
			if (vz[z_nzero] < 0) :#判断运动方向
				print("先沿着z轴负方向运动")
			else:
				print("先沿着z轴正方向运动")
			if (vx[x_nzero] < 0) :#判断运动方向
				print("然后沿着x轴负方向运动")
			else:
				print("然后沿着x轴正方向运动")
	if (min(change_x,change_y,change_z) == change_z):#在xy平面上
		#print("xy")
		if x_nzero < y_nzero:#判断先向哪一个轴运动
			if (vx[x_nzero] < 0) :#判断运动方向
				print("先沿着x轴负方向运动")
			else:
				print("先沿着x轴正方向运动")
			if (vy[y_nzero] < 0) :#判断运动方向
				print("然后沿着y轴负方向运动")
			else:
				print("然后沿着y轴正方向运动")
		else:
			if (vy[y_nzero] < 0) :#判断运动方向
				print("先沿着y轴负方向运动")
			else:
				print("先沿着y轴正方向运动")
			if (vx[x_nzero] < 0) :#判断运动方向
				print("然后沿着x轴负方向运动")
			else:
				print("然后沿着x轴正方向运动")
	if (min(change_x,change_y,change_z) == change_x):#在yz平面上
		#print("yz")
		if z_nzero < y_nzero:#判断先向哪一个轴运动
			if (vz[z_nzero] < 0) :#判断运动方向
				print("先沿着z轴负方向运动")
			else:
				print("先沿着z轴正方向运动")
			if (vy[y_nzero] < 0) :#判断运动方向
				print("然后沿着y轴负方向运动")
			else:
				print("然后沿着y轴正方向运动")
		else:
			if (vy[y_nzero] < 0) :#判断运动方向
				print("先沿着y轴负方向运动")
			else:
				print("先沿着y轴正方向运动")
			if (vz[z_nzero] < 0) :#判断运动方向
				print("然后沿着z轴负方向运动")
			else:
				print("然后沿着z轴正方向运动")
def change_direction_count(vv):#速度方向改变次数
	count = 0
	v = []
	for v1 in vv:
		if v1 != 0:
			v.append(v1)
	for i in range(len(v)-1):
		if v[i]*v[i+1] < 0:
			count += 1
	return count
def gesture_re3(change_x,change_y,change_z): #模型三，握手、挥手
	type = 0
	rate = 0.3
	if change_x<(rate*change_z) and change_y<(rate*change_z):#仅在z轴上有运动
		type = "z"
	elif change_x<(rate*change_y) and change_z<(rate*change_y):#仅在y轴上有运动
		type = "y"
	elif change_y<(rate*change_x) and change_z<(rate*change_x):#仅在z轴上有运动
		type = "x"
	if type :
		Vx,Vy,Vz = get_V()
		#print(max(change_x,change_y,change_z))
		#print(change_x,change_y,change_z)
		if max(change_x,change_y,change_z) == change_z:
			if change_direction_count(Vz) > 1:
				print("当前手势是“握手”，上下挥动了" + str(change_direction_count(Vz)) + "次")
		if max(change_x,change_y,change_z) == change_x:
			if change_direction_count(Vx) > 1:
				print("当前手势是“挥手”，左右挥动了" + str(change_direction_count(Vx)) + "次")
		if max(change_x,change_y,change_z) == change_y:
			if change_direction_count(Vy) > 1:
				print("当前手势是“挥手”，左右挥动了" + str(change_direction_count(Vy)) + "次")
		return 1
	return 0
	#print('x',Vx)
	#print('y',Vy)
	#print('z',Vz)
def mean(a):
	sum = 0
	for aa in a:
		sum += aa
		#format(temp/(num),'.2f')
	return format(sum/len(a),'.4f')
def distance(x1,y1,x2,y2):
	return ((x1-x2)**2+(y1-y2)**2)**0.5
def find_min_d(x,z):
	mid = int(len(x)/3)
	num = mid
	num1 = 0
	#print('num',num)
	min = distance(x[0],z[0],x[mid],z[mid])
	for j in range (0,mid):
		for i in range(len(x)-mid,len(x)):
			if min > distance(x[j],z[j],x[i],z[i]):
				min = distance(x[j],z[j],x[i],z[i])
				num = i
				num1 =j
	#print('num',num)
	#print('num1',num1)
	return min,num,num1
if __name__ == '__main__':
	mpl.rcParams['legend.fontsize'] = 10
	fig = plt.figure(num='xyz',figsize=(5,4))
	grp = fig.gca(projection='3d')
	xx,yy,zz = set_data()
	grp.plot(xx, yy, zz, label='Gesture Line')
	#各轴比例一样
	max_x = max(xx)
	min_x = min(xx)
	max_y = max(yy)
	min_y = min(yy)
	max_z = max(zz)
	min_z = min(zz)
	#print("xx",xx)
	#print("yy",yy)
	#print("zz",zz)
	max_all = max_x
	#print(min_z)
	#print(max_z)
	min1 = []
	max1 = []
	min1.append(min_x)
	min1.append(min_y)
	min1.append(min_z)
	max1.append(max_x)
	max1.append(max_y)
	max1.append(max_z)
	#print(min(min1))
	#print(max(max1))
	range_max = max(max1) + abs(max(max1)*0.2)
	range_min = min(min1) - abs(min(min1)*0.2)
	grp.set_xlim(range_min,range_max)
	grp.set_ylim(range_min,range_max)
	grp.set_zlim(range_min,range_max)
	grp.set_xlabel('X')
	grp.set_ylabel('Y')
	grp.set_zlabel('Z')
	#标注出开始点
	sx = [xx[0]]
	sy = [yy[0]]
	sz = [zz[0]]
	grp.plot(sx,sy,sz,label = 'START',color = 'r',markersize = 9,marker='o')
	#标注结束点
	ex = [xx[len(xx)-1]]
	ey = [yy[len(yy)-1]]
	ez = [zz[len(zz)-1]]
	grp.plot(ex,ey,ez,label = 'END',color = 'g',markersize = 9,marker='o')
	grp.legend(loc='best',edgecolor='blue')#图例设置
	gesture_type = 0
	if(gesture_re1(abs(max_x-min_x),abs(max_y-min_y),abs(max_z-min_z))):
		result1 = gesture_re1(abs(max_x-min_x),abs(max_y-min_y),abs(max_z-min_z))
		if result1 == 'x':
			if xx[len(xx)-1] > 0:
				print("轨迹运动方向单向平行于x轴并沿x轴正方向运动")
			else:
				print("轨迹运动方向单向平行于x轴并沿x轴负方向运动")
		if result1 == 'y':
			if yy[len(yy)-1] > 0:
				print("轨迹运动方向单向平行于y轴并沿y轴正方向运动")
			else:
				print("轨迹运动方向单向平行于y轴并沿y轴负方向运动")
		if result1 == 'z':
			if zz[len(zz)-1] > 0:
				print("轨迹运动方向单向平行于z轴并沿z轴正方向运动")
			else:
				print("轨迹运动方向单向平行于z轴并沿z轴负方向运动")
		gesture_type = 1
	if gesture_type == 0:
		if gesture_re3(abs(max_x-min_x),abs(max_y-min_y),abs(max_z-min_z)) == 1:
			gesture_type = 3
	#手势模型4
	round = -1
	mx = []
	mz = []
	mx.append(float(mean(xx)))
	mz.append(float(mean(zz)))
	#print(mx,mz)
	#print(ex,ez)
	#print(sx,sz)
	diameter = min(abs(max_x-min_x),abs(max_z-min_z))
	for i in range(len(xx)):
		if distance(mx[0],mz[0],xx[i],zz[i]) > diameter:
			round = 0
	#print(round)
	min_d,n1,n2 = find_min_d(xx,zz)#找最小距离
	#print(0.2*max(abs(max_x-min_x),abs(max_z-min_z)))
	#print(min_d)
	if min_d < 0.2*max(abs(max_x-min_x),abs(max_z-min_z)) and round ==-1:
		round = 1
	if round == 1:
		gesture_type = 4
		print("该手势为圆形")
	if gesture_type == 0:
		print("本手势按照手势模型二进行分析")
		gesture_re2(abs(max_x-min_x),abs(max_y-min_y),abs(max_z-min_z))
	#xy
	plt.figure(num='xy',figsize=(4,3))
	plt.plot(xx, yy,label='xy')
	plt.plot(sx,sy,label = 'START',color = 'r',markersize = 9,marker='o')
	plt.plot(ex,ey,label = 'END',color = 'g',markersize = 9,marker='o')
	plt.xlim(range_min,range_max)
	plt.ylim(range_min,range_max)
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.legend(loc='best',edgecolor='blue')#图例设置
	#yz
	plt.figure(num='yz',figsize=(4,3))
	plt.plot(yy, zz,label='yz')
	plt.plot(sy,sz,label = 'START',color = 'r',markersize = 9,marker='o')
	plt.plot(ey,ez,label = 'END',color = 'g',markersize = 9,marker='o')
	plt.xlim(range_min,range_max)
	plt.ylim(range_min,range_max)
	plt.xlabel('Y')
	plt.ylabel('Z')
	plt.legend(loc='best',edgecolor='blue')#图例设置
	#zx
	plt.figure(num='xz',figsize=(4,3))
	plt.plot(xx, zz,label='xz')
	plt.plot(sx,sz,label = 'START',color = 'r',markersize = 9,marker='o')
	plt.plot(ex,ez,label = 'END',color = 'g',markersize = 9,marker='o')
	sb = []
	sd = []
	sb.append(xx[n1])
	sd.append(zz[n1])
	plt.plot(sb,sd,label = 'node1',color = 'b',markersize = 5,marker='o')
	sb = []
	sd = []
	sb.append(xx[n2])
	sd.append(zz[n2])
	plt.plot(sb,sd,label = 'node2',color = 'b',markersize = 5,marker='o')
	plt.xlim(range_min,range_max)
	plt.ylim(range_min,range_max)
	plt.xlabel('X')
	plt.ylabel('Z')
	plt.legend(loc='best',edgecolor='blue')#图例设置
	plt.show()
