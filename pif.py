import gopigo3
import time
from di_sensors.easy_distance_sensor import EasyDistanceSensor
import easygopigo3 as easy

mrBean = gopigo3.GoPiGo3()
easyBean = easy.EasyGoPiGo3()

maximum = 255

p = .4
k = .1

mrDisty = EasyDistanceSensor()

corrective = 1.7888571428571 # this constant corrects for error in the physical robot

while True:

    mrBean.offset_motor_encoder(mrBean.MOTOR_LEFT, mrBean.get_motor_encoder(mrBean.MOTOR_LEFT))

    c = 0
    
    error = 0
    integral = 0
    feedForward = 1
    try:
        point = (float(input("Enter a distance in millimeters: ")))
    except:
        point = 0;
    goBackward = False
    if point <= 0:
        goBackward = True
        point *= -1
        
    point *= corrective
    
    readDisty = mrDisty.read()

    while (goBackward == False and mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) <= point or goBackward and mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) >= point * -1) and (readDisty >= 10 or goBackward):
        readDisty = mrDisty.read()
        error = (point - mrBean.get_motor_encoder(mrBean.MOTOR_LEFT))
        integral += error
        c = (error * p) + (integral * k) + feedForward
        if c > maximum:
            c = maximum
        easyBean.set_speed(c)
        if goBackward == False:
            easyBean.forward()
        else:
            easyBean.backward()
        print("Distance: %d Goal: %d Wall Distance: %d" % (mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) / corrective, point / corrective, readDisty))
    easyBean.stop()
