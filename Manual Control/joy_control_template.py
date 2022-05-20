#!/usr/bin/env python

import rospy

from sensor_msgs.msg import Joy

def axe1(data):  #x-axis
    print("x-axis=",data)

def axe2(data):  #y-axis
    print("y-axis=",data)

def axe3(data):  #x_angle
    print("x_angle=",data)

def axe4(data):  #y_angle
    print("y_angle=",data)

def axe5(data):  #little_x
    print("little_x=",data)

def axe6(data):  #little_y
    print("little_y=",data)

axe_func_dict = {"1" : axe1,
                "2" : axe2,
                "3" : axe3,
                "4" : axe4,
                "5" : axe5,
                "6" : axe6,
                }


def button1():
    print("1")

def button2():
    print("2")

def button3():
    print("3")

def button4():
    print("4")

def button5():
    print("5")

def button6():
    print("6")

def button7():
    print("7")

def button8():
    print("8")

def button9():
    print("9")

def button10():
    print("10")

def button11():
    print("11")

def button12():
    print("12")

button_func_dict = {"1" : button1,
                    "2" : button2,
                    "3" : button3,
                    "4" : button4,
                    "5" : button5,
                    "6" : button6,
                    "7" : button7,
                    "8" : button8,
                    "9" : button9,
                    "10" : button10,
                    "11" : button11,
                    "12" : button12}

def callback(data):

    for button in data.buttons:
        if button == 1:
            msg = data.buttons.index(button)
            #fcall = "button" + str(msg+1)
            #print(fcall)
            button_func_dict[str(msg+1)]()

    for axe in data.axes:
        if axe != 0:
            msg = data.axes.index(axe)
            axe_func_dict[str(msg+1)](axe)
            

def joy_listener():
    rospy.init_node("listener", anonymous=True)
    rospy.Subscriber("/joy", Joy, callback)
    rospy.spin()

if __name__ == "__main__":
    joy_listener()
