def get_centers_cars(image, nums):
    import cv2
    import numpy as np
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 100])

    black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
        
    contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = []
    min_contour_area = 1000 

    for contour in contours:
        area = cv2.contourArea(contour)
        if  200 < area and area < min_contour_area:
            filtered_contours.append(contour)
            


    black_mask = np.zeros_like(black_mask)
    cv2.drawContours(black_mask, filtered_contours, -1, (255), thickness=cv2.FILLED)
    black_mask = cv2.bitwise_not(black_mask)
    
    for angle in range(0, 360, 45):
        
        height, width = black_mask.shape[:2]
        center = (width / 2, height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        rotated_image = cv2.warpAffine(black_mask, rotation_matrix, (width, height))
        
        import pytesseract

        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABEKMHOPCTYX'

        text = pytesseract.image_to_string(rotated_image, config=custom_config)  
        
        for string in text.split('\n'):
            if len(string) != 6 :
                continue
            nums.add(string)
    

    return nums