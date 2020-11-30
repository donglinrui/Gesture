## Gesture recognition based on Raspberry pi 

### **Research Background**

With the development of technology, the technology of gesture recognition is become one of the most important part of Human-computer Interaction.

There are two main ways to recognize gesture. One is basing on image recognize, the other is basing on acceleration sensors. The first way needs camera and is sensitive to environment and light. By using acceleration sensors, gesture recognition will not be influenced by these conditions. For example, by using acceleration sensors can recognize gesture under the water or without light, which is difficult to recognize by using image recognition. In my research, I built a gesture recognition system based on acceleration sensors.

### **Data collection**

The ADXL345 is a small, thin, ultralow power, 3-axis accelerometer with high resolution (13-bit) measurement at up to ±16 g. 

The Raspberry Pi is a series of small single-board computers developed in the United Kingdom by the Raspberry Pi Foundation to promote teaching of basic computer science in schools and in developing countries.

This system use ADXL345 to collect acceleration Data and transfer to Raspberry Pi. On raspberry, the acceleration will be processed and the result of gesture type can be work out. 

![image-20201130100328520](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100328520.png)

### **How to draw gesture line**

![image-20201130100431310](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100431310.png)

![image-20201130100442032](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100442032.png)

To draw gesture line, I integrate(積分) the accelerate data on 3 axis to get displacement data and velocity data. Since the interval of acceleration data is 0.02s, the gesture line can be drawn. 

### **Noise filter**

![image-20201130100537068](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100537068.png)

![image-20201130100543692](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100543692.png)

To reduce the noise in the gesture recognition system, this system uses several kinds of filter methods.

The filter noise reduction method includes neighborhood average method, median method and Kalman method.

These two pictures show the result of these methods. Obviously, after filtering noise, the system can get relatively smooth gesture line.

### **Gesture Model**

#### Model 1

![image-20201130100700903](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100700903.png)

#### Model 2

![image-20201130100723633](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100723633.png)

#### Model 3

![image-20201130100744741](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100744741.png)

#### Model 4

![image-20201130100808016](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100808016.png)

### **8 test gesture**

![image-20201130100854189](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100854189.png)

![image-20201130100902604](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100902604.png)

### **Test result**

![image-20201130100931332](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100931332.png)

![image-20201130100940049](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201130100940049.png)

（1）The tester after training is more adapt for this system. And this kind of tester will improve the accuracy of this system.(Training means that the tester have used this gesture recognition system for several times before)

（2）The data on Z axis (vertical axis) is more accurate than the other two axis. It may be influenced by the Gravitational acceleration.

（3）The accuracy of model 1(straight model) and model 3(shake and wave hand model) is higher than the other two models. Probably because the movement of gesture is only one axis. 

（4）The accuracy of model 4(cycle model) is relatively lower. Probably because when the gesture data move as a cycle the acceleration on 3 axis will become more complex. 

### **Summary**

This system can transfer the acceleration data to gesture line and draw it. Using this system can analyze the gesture more directly, because the researcher can directly see the movement in graphics. After classifying the gesture to 4 models, the system can recognize the type of gesture. The users after train can use this system to recognize some type of gestures based on the four models. And this gesture recognition system can be widely apply in no light environment and underwater environment, which cannot use traditional gesture recognition based on image processing. 

##### **Insufficiency**

(1)The system can just recognize one gesture. It cannot separate a series of gesture.

(2)The system is still influenced by the noise. The noise filter system should be improved.

(3)The system can only describe the shape of the gesture. The accuracy of the distance of gesture movement is very low. 

##### **Improvement**

(1)Add more sensors in the system to reduce the noise from one sensor. 

(2)Improve the filter methods.

(3)Design a gesture separate function.

