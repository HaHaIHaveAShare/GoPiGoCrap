import gopigo3
import time
from di_sensors.easy_distance_sensor import EasyDistanceSensor
import easygopigo3 as easy

mrBean = gopigo3.GoPiGo3()
easyBean = easy.EasyGoPiGo3()

maximum = 255

p = 1
k = .2
d = .4

controllMode = 0

mrDisty = EasyDistanceSensor()

corrective = 1.7888571428571 # this constant corrects for error in the physical robot

while True:

    mrBean.offset_motor_encoder(mrBean.MOTOR_LEFT, mrBean.get_motor_encoder(mrBean.MOTOR_LEFT))
    mrBean.offset_motor_encoder(mrBean.MOTOR_RIGHT, mrBean.get_motor_encoder(mrBean.MOTOR_RIGHT))

    c = 0
    
    error = 0
    oldError = 0
    integral = 0
    feedForward = 1
    try:
        point = (float(input("Enter a distance in millimeters: ")))
    except:
        point = 0;

    truePoint = point

    if point == 0:
        controllMode += 1

        if controllMode == 1:
            print("Switching to lft/rght drive mode")
        if controllMode == 2:
            print("Switching to fwd/back drive mode")
            controllMode = 0
        continue
        
    goBackward = False
    if point <= 0:
        goBackward = True
        point *= -1
        
    point *= corrective

    if controllMode == 1 and goBackward:
        truePoint *= -1
    
    readDisty = mrDisty.read()

    while True:
        readDisty = mrDisty.read()
        if controllMode == 0 and goBackward == False:
            error = point - mrBean.get_motor_encoder(mrBean.MOTOR_LEFT)
        elif controllMode == 0 and goBackward:
            error = point - mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) * -1
        elif controllMode == 1 and goBackward == False:
            error = point - mrBean.get_motor_encoder(mrBean.MOTOR_RIGHT)
        elif controllMode == 1 and goBackward:
            error = point - mrBean.get_motor_encoder(mrBean.MOTOR_LEFT)
        integral += error
        derivative = error - oldError
        oldError = error
        c = (error * p) + (integral * k) + (derivative * d)
        if c > maximum:
            c = maximum
        easyBean.set_speed(c)
        if (mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) >= truePoint * corrective - 3 and mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) <= truePoint * corrective + 3 or mrBean.get_motor_encoder(mrBean.MOTOR_RIGHT) >= truePoint * corrective - 3 and mrBean.get_motor_encoder(mrBean.MOTOR_RIGHT) <= truePoint * corrective + 3):
            print("Goal Achieved (more or less)")
            easyBean.set_speed(0)
            break
        if readDisty <= 10:
            print("Error, wall within 10 cm")
            easyBean.set_speed(0)
            break
        if goBackward == False and controllMode == 0:
            easyBean.forward()
        elif goBackward and controllMode == 0:
            easyBean.backward()
        elif goBackward == True and controllMode == 1:
            easyBean.right()
        else:
            easyBean.left()
        if controllMode == 0 or goBackward:
            print("Distance: %d Goal: %d Wall Distance: %d" % (mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) / corrective, truePoint, readDisty))
        else:
            print("Distance: %d Goal: %d Wall Distance: %d" % (mrBean.get_motor_encoder(mrBean.MOTOR_RIGHT) / corrective, truePoint, readDisty))
    easyBean.stop()