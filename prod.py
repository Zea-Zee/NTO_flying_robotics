
def get_centers_cars(image):
    import cv2
    import numpy as np

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])

    lower_blue = np.array([100, 50, 50])  
    upper_blue = np.array([130, 255, 255])

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    white_mask = cv2.inRange(hsv_image, lower_white, upper_white)


    kernel = np.ones((7,7), np.uint8)
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, kernel)
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)

    combined_mask = cv2.bitwise_or(blue_mask, green_mask)
    combined_mask = cv2.bitwise_or(combined_mask, white_mask)


    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if 100 < area < 5000:
            cv2.drawContours(combined_mask, [contour], -1, 255, -1)
        else:
            cv2.drawContours(combined_mask, [contour], -1, 0, -1)
   
    

    centers = list()
    for contour in contours:
        M = cv2.moments(contour)
    
        if M["m00"] != 0: 
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            center = (center_x, center_y)
            centers.append(center)
            
    return centers

import cv2

image = cv2.imread("img.png")
print(get_centers_cars(image))