import numpy as np

def K(position_noise):
    pass
    predicts = [position_noise[0]]
    position_predict = predicts[0]
    predict_var = 0
    odo_var = 100**2 #这是我们自己设定的位置测量仪器的方差，越大则测量值占比越低
    v_std = 5 # 测量仪器的方差
    for i in range(1,len(position_noise)):
        dv =  (position_noise[i]-position_noise[i-1])# 模拟从IMU读取出的速度
        #print("dv",dv)
        position_predict = position_predict + dv # 利用上个时刻的位置和速度预测当前位置
        predict_var += v_std**2 # 更新预测数据的方差
        # 下面是Kalman滤波
        position_predict = position_predict*odo_var/(predict_var + odo_var)+position_noise[i]*predict_var/(predict_var + odo_var)
        predict_var = (predict_var * odo_var)/(predict_var + odo_var)**2
        predicts.append(position_predict)
    return predicts

if __name__ == '__main__':
    #测试数据
    data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17.000001,17.9999,19,20,21,22]
    print(data)
    data = K(data)
    print(data)