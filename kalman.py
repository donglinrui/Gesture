import numpy as np

def K(position_noise):
    pass
    predicts = [position_noise[0]]
    position_predict = predicts[0]
    predict_var = 0
    odo_var = 100**2 
    v_std = 5 # variance of instrument
    for i in range(1,len(position_noise)):
        dv =  (position_noise[i]-position_noise[i-1])# read imitate the velocity of IMU
        #print("dv",dv)
        position_predict = position_predict + dv # use the last position to predict the next
        predict_var += v_std**2 # update the new variance
        #Kalman fliter
        position_predict = position_predict*odo_var/(predict_var + odo_var)+position_noise[i]*predict_var/(predict_var + odo_var)
        predict_var = (predict_var * odo_var)/(predict_var + odo_var)**2
        predicts.append(position_predict)
    return predicts

if __name__ == '__main__':
    #test data
    data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17.000001,17.9999,19,20,21,22]
    print(data)
    data = K(data)
    print(data)