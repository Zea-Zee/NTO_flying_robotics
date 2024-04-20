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


import mycv
import prod

CAM_HEIGHT = 1.5   #for 320x240
# CAM_HEIGHT = 1.72   #for 320x240
# CAM_HEIGHT = 1.96   #for 854x480


coordinates = [
    (0.0, 0.0),

    (1.8, 0.0),

    (3.6, 0.0),
    (0.0, 0.9),

    (1.8, 0.9),

    (3.6, 0.9),
    (0.0, 1.8),

    (1.8, 1.8),

    (3.6, 1.8),
    (0.0, 2.7),

    (1.8, 2.7),

    (3.6, 2.7),
    (0.0, 3.6),

    (1.8, 3.6),

    (3.6, 3.6),
    (0.0, 4.5),

    (1.8, 4.5),

    (3.6, 4.5),
    (0.0, 5.4),

    (1.8, 5.4),

    (3.6, 5.4)
]


rospy.init_node('cv')
bridge = CvBridge()
image_pub = rospy.Publisher('cv', Img, queue_size=5)
res_pub = rospy.Publisher('stairwayToHeaven', Img, queue_size=5)


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


def navigate_wait(x=0, y=0, z=0, speed=0.2, frame_id='body', auto_arm=False, tolerance=0.0125):
    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    while not rospy.is_shutdown(): # Чтобы было всегда активно
        telem = get_telemetry(frame_id='navigate_target') # Получение координат куда двигается дрон
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break # Если не в центре координат, по которым хочется передвигаться, будет повторяться
        rospy.sleep(0.0125) # Каждые 0.2 секунды делать проверку


def spot_all_markers(dots):
    myset = set()
    for dot in dots:
        navigate_wait(x=dot[0], y=dot[1], z=CAM_HEIGHT, speed=0.5, frame_id='aruco_map', auto_arm=True)
        top_img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Img), 'bgr8')
        myset = prod.get_number(top_img, myset)
    for num, val in enumerate(myset):
        print(f"Car {num}: {val}")


print('Taking off')
rospy.sleep(1)
set_effect(effect='blink', r=0, g=0, b=255)
navigate(x=0, y=0, z=2, speed=0.4, frame_id='body', auto_arm=True)
rospy.sleep(3)
print("Starting recognize")
spot_all_markers(coordinates)
print("Flying to landing spot")
set_effect(effect='blink', r=0, g=255, b=0)
navigate_wait(x=0, y=0, z=1.5, speed=0.4, frame_id='aruco_map', auto_arm=True)
print("Landing")
set_effect(effect='blink', r=255, g=0, b=0)
# navigate_wait(x=0, y=0, z=-1.5, speed=0.5, frame_id='body', led_mode="landing", auto_arm=True)
navigate(x=0, y=0, z=-1.5, speed=0.5, frame_id="body", auto_arm=False)
rospy.sleep(3)
# motor_control(speed=0)
# explore_field()
land()
set_effect(effect='rainbow')
exit(0)
