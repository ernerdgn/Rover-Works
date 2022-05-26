#!/usr/bin/python3
from operator import is_
from time import sleep
from turtle import goto
import actionlib
import math
from nav_msgs.msg import Odometry
import rospy
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult, MoveBaseActionResult

def solve2 (m, midx, midy, carpan, artis_miktari, hedefler_arasi_uzaklik):
    r = [midx, midy]

    uzaklik = 0
    while (uzaklik < hedefler_arasi_uzaklik):
        r[0] += artis_miktari * 1 * carpan
        r[1] += artis_miktari * m * carpan
        uzaklik = math.sqrt((r[0]-midx)**2 + (r[1]-midy)**2)

    return r


def solve(rx, ry, ra, ca1, ca2, side1, side2, point1_distance, point2_distance):
    #1
    aci_derece_nokta_bir = ra + side1*ca1
    aci_derece_nokta_iki = ra + side2*ca2

    #2
    ax = point1_distance * math.cos(math.radians(aci_derece_nokta_bir)) + rx
    ay = point1_distance * math.sin(math.radians(aci_derece_nokta_bir)) + ry

    bx = point2_distance * math.cos(math.radians(aci_derece_nokta_iki)) + rx
    by = point2_distance * math.sin(math.radians(aci_derece_nokta_iki)) + ry

    #3
    midx = (ax + bx) / 2
    midy = (ay + by) / 2

    m = (ax - bx) / (by - ay)

    hedefler_arasi_uzaklik = 1

    #4
    des1 = solve2 (m, midx, midy, 1, 0.01, hedefler_arasi_uzaklik)
    des2 = [midx, midy]
    des3 = solve2 (m, midx, midy, -1, 0.01, hedefler_arasi_uzaklik)

    aci = math.degrees(math.atan(m))

    #5 (optimal?)
    if (((rx-des1[0])**2 + (ry-des1[1])**2) > ((rx-des2[0])**2 + (ry-des2[1])**2)):
        des1, des3 = des3, des1
        aci+=180
        aci%=360

    #6
    des1.append(aci)
    des2.append(aci)
    des3.append(aci)
    #print("goal ", des1, des2, des3)
    return [des1, des2, des3]


def movebase_client(targetX, targetY, targetW):
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = targetX
    goal.target_pose.pose.poisiton.y = targetY
    goal.target_pose.pose.orientation.w = targetW

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


def callback_data(data):
    pose_w_c = data.pose  #geometry_msgs/PoseWithCovariance

    pose = pose_w_c.pose

    #orientation data (inside the pose msg) contains the angle info: x,y,z,w
    #x - horizontal angle in radians
    #normalization x = rad(angle) / 10

    orientation = pose.orientation
    position = pose.position

    robot_x = position.x
    robot_y = position.y

    robot_angle = orientation.x  #may be orientation.z

    aruco1_pixel = 768  #EXAMPLE
    aruco2_pixel = 672

    if aruco1_pixel < aruco2_pixel:
        aruco1_pixel, aruco2_pixel = aruco2_pixel, aruco1_pixel

    max_pixel = 1280
    max_angle = 110
    rate = max_angle / max_pixel
    all_left = False
    all_right = False

    if aruco1_pixel >= 640 & aruco2_pixel >= 640:
        side1, side2 = -1, -1
        all_right = True
    elif aruco1_pixel < 640 & aruco2_pixel >= 640:
        side1, side2 = 1, -1
    elif aruco1_pixel < 640 & aruco2_pixel < 640:
        side1, side2 = 1, 1
        all_left = True

    if all_right:
        beta = 55 - (max_angle - (rate * aruco1_pixel))  #BETA (ca1)
        theta = 55 - (max_angle - (rate * aruco2_pixel)) #THETA + BETA (ca2)
                                                         # ca1 < ca2
    if all_left:
        beta = (max_angle - (rate * aruco1_pixel)) - 55
        theta = (max_angle - (rate * aruco2_pixel)) - 55

    points = []
    points = solve(robot_x, robot_y, robot_angle, beta, theta, side1, side2, depth1, depth2) # 13**(1/2), 6*(2**(1/2))
    global is_over
    if is_over:
        print(points)
    is_over = False
    # for point in points:
    #     for i in range(0,2):
    #         movebase_client(point[0], point[1]-17, point[2])                             #!!!!!!!!!!!!!!!!!          -17
    #         result = movebase_client(point[0], point[1], point[2])
    #         print("Goal execution status : ", result)


    #solve(1, 2, 30, angle11, angle12, 1, 13**(1/2), 6*(2**(1/2)))  # solunda ise kameraya_gore_sol_sag 1 ; saginda ise kameraya_gore_sol_sag -1

    # result = movebase_client(tx,tw)
    #     if result:
    #         rospy.loginfo("Goal execution done!")


def gate_passing(t1, t2):
    global depth1
    global depth2
    depth1 = t1
    depth2 = t2
    rospy.init_node('listener', anonymous=True)
    while is_over:
        rospy.Subscriber("/zed/zed_nodelet/odom", Odometry, callback_data)  # 1280x720


depth1=10
depth2=3
is_over = True
gate_passing(13**(1/2), 6*(2**(1/2)))
