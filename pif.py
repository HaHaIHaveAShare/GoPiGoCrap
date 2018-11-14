import gopigo3
import time
import easygopigo3 as easy

mrBean = gopigo3.GoPiGo3()
easyBean = easy.EasyGoPiGo3()

c = 0

error = 0
integral = 0
feedForward = 1

maximum = 255

point = 4000.0

p = .2
k = .2

mrBean.offset_motor_encoder(mrBean.MOTOR_LEFT, mrBean.get_motor_encoder(mrBean.MOTOR_LEFT))

while mrBean.get_motor_encoder(mrBean.MOTOR_LEFT) <= point:
    error = (point - mrBean.get_motor_encoder(mrBean.MOTOR_LEFT)) * p
    integral += error
    c = (error * p) + (integral * k) + feedForward
    if c > maximum:
        c = maximum
    easyBean.set_speed(c)
    easyBean.forward()
    print("Distance: %d" % (mrBean.get_motor_encoder(mrBean.MOTOR_LEFT)))
easyBean.stop()
