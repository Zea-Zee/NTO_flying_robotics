import time
from PIL import Image
import rospy
import math
from clover import srv
from std_srvs.srv import Trigger
from clover.srv import SetLEDEffect
import time
import cv2
from sensor_msgs.msg import Image as Img
from clover import long_callback
import numpy as np
from cv_bridge import CvBridge


import comp_vis
import server_processing
# import prod

CAM_HEIGHT = 1.5   #for 320x240
# CAM_HEIGHT = 1.72   #for 320x240
# CAM_HEIGHT = 1.96   #for 854x480


rospy.init_node('cv')
bridge = CvBridge()
image_pub = rospy.Publisher('cv', Img, queue_size=5)
debug_pub = rospy.Publisher('stairwayToHeaven', Img, queue_size=5)


get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)  # define proxy to ROS-service
# motor_control = rospy.ServiceProxy('/path/to/motor_control/service', srv.SetLEDSignal)
start = time.time()


def navigate_wait(x=0, y=0, z=0, speed=0.2, frame_id='body', auto_arm=False, tolerance=0.1):
    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while not rospy.is_shutdown(): # Чтобы было всегда активно
        telem = get_telemetry(frame_id='navigate_target') # Получение координат куда двигается дрон
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.0125)


# def spot_all_markers(dots):
#     myset = set()
#     for dot in dots:
#         navigate_wait(x=dot[0], y=dot[1], z=CAM_HEIGHT, speed=0.5, frame_id='aruco_map', auto_arm=True)
#         top_img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Img), 'bgr8')
#         myset = prod.get_number(top_img, myset)
#     for num, val in enumerate(myset):
#         print(f"Car {num}: {val}")


def check_zones():
    zone_one_seacrh_coords = [
        (0, 0.9),
        (0, 1.8),
        (0, 2.7),
        (0, 3.6),
    ]
    road_seacrh_coords = [
        (1.35, 5.4), 
        (1.35, 4.5), 
        (1.35, 3.6), 
        (1.35, 2.7), 
        (1.35, 1.8), 
        (1.35, 0.9),
        
        (2.25, 0.9),
        (2.25, 1.8),
        (2.25, 2.7),
        (2.25, 3.6),
        (2.25, 4.5),
        (2.25, 5.4),
    ]
    zone_two_seacrh_coords = [
        (3.9, 4.5),
        (3.9, 3.6),
        (3.9, 2.7),
        (3.9, 1.8),
        (3.9, 0.9),
        (3.9, 0.0)
    ]

    text = ''

    res = check_zone('Zone 1', zone_one_seacrh_coords, 0)
    text += res[1]
    if time.time() - start > 350:
        return text
    res = check_zone('Road', road_seacrh_coords, res[0])
    text += res[1]
    if time.time() - start > 350:
        return text
    res = check_zone('Zone 2', zone_two_seacrh_coords, res[0])
    text += res[1]
    return text


def check_zone(zone_name: str, zone_coords, car_counter):
    text = ''
    numbers_set = set()
    print(f"Checking {zone_name}")
    for dot in zone_coords:
        if time.time() - start > 370:
            break
        navigate_wait(x=dot[0], y=dot[1], z=1.3, speed=0.4, frame_id='aruco_map', auto_arm=True, tolerance=0.1)
        # navigate(x=0, y=0, z=-0.3, speed=0.2, frame_id="body", auto_arm=False)
        top_img = bridge.imgmsg_to_cv2(rospy.wait_for_message('/main_camera/image_raw', Img), 'bgr8')
        res_img = comp_vis.find_cars(top_img)
        if res_img:
            numbers_set = comp_vis.get_num(top_img, numbers_set)
        # if res_img is not None:
        #     pub_img = bridge.cv2_to_imgmsg(res_img, encoding="bgr8")
        #     debug_pub.publish(pub_img)

        # print(f"Trying to recogn number in area about {dot}")

    print(f"{zone_name} cars list:")
    # text += zone_numbers_set = comp_vis.get_num(top_img, numbers_set)name
    for number in numbers_set:
        car_counter += 1
        text += f"{car_counter}. {number}, car on {zone_name}\n"
        text += server_processing.get_car_payment_status(number)
        print(f"{car_counter}. {number}, car on {zone_name}")
    print(f"Time remained: {420 - (time.time() - start)}s")
    return (car_counter, text)
    


print('Taking off')
rospy.sleep(1)
set_effect(effect='blink', r=0, g=0, b=255)
navigate(x=0, y=0, z=2, speed=0.5, frame_id='body', auto_arm=True)
rospy.sleep(3)


# print("Flying to center for debug")
# set_effect(effect='blink', r=0, g=255, b=0)
# navigate_wait(x=1.7, y=2.6, z=2.8, speed=0.4, frame_id='aruco_map', auto_arm=True)

# # print(f"wait for img")
# top_img = bridge.imgmsg_to_cv2(rospy.wait_for_message('/main_camera/image_raw', Img), 'bgr8')
# # print(f"got img")
# res_img = comp_vis.show_mask(top_img)
# if res_img is not None:
#     # print(f"mask")
#     pub_img = bridge.cv2_to_imgmsg(res_img, encoding="bgr8")
#     debug_pub.publish(pub_img)
# rospy.sleep(2)

# pub_img = bridge.cv2_to_imgmsg(top_img, encoding="bgr8")
# debug_pub.publish(pub_img)
# rospy.sleep(2)
# navigate_wait(x=1.7, y=2.6, z=2, speed=0.4, frame_id='aruco_map', auto_arm=True)


print('Starting check')
result = check_zones()


print("Flying to landing spot")
set_effect(effect='blink', r=0, g=255, b=0)
navigate_wait(x=0, y=0, z=1.5, speed=0.4, frame_id='aruco_map', auto_arm=True)


print("Landing")
set_effect(effect='blink', r=255, g=0, b=0)
navigate(x=0, y=0, z=-1.5, speed=0.5, frame_id="body", auto_arm=False)
rospy.sleep(3)
land()
set_effect(effect='rainbow')
print(f"_______RESULT_______:\n{result}")
exit(0)
