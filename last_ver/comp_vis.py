def find_cars(image):
    
    if image is None:
        print(f"Find cars func got empty image and skipped it")
        return None
    
    import cv2
    import numpy as np
    

    crop_size = 240

    image_height, image_width = image.shape[:2]

    x1 = (image_width - crop_size) // 2
    y1 = (image_height - crop_size) // 2

    x2 = x1 + crop_size
    y2 = y1 + crop_size

    image_cropped = image
    # image_cropped = image[y1:y2, x1:x2]

    rgb_image = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2RGB)
    
    rgb_image = cv2.GaussianBlur(rgb_image, (9, 9), 0)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([130, 130, 130])

    black_mask = cv2.inRange(image_cropped, lower_black, upper_black)

    kernel = np.ones((11,11), np.uint8)
    mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    mask = cv2.bitwise_not(mask)
    
    
    
    center = (0, 0)
    M = cv2.moments(mask)
    if M["m00"] != 0: 
        center_x =  int(M["m10"] / M["m00"]) 
        center_y = int(M["m01"] / M["m00"]) 
        center = (center_x + (image_width - crop_size) // 2, center_y + (image_height - crop_size) // 2)
    cv2.circle(image, center, 10, (0, 255, 0), -1)
            
    return np.count_nonzero(mask == 255) / (160**2) >= 0.12
    # return cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    
    
def show_mask(image):
    if image is None:
        print(f"Find cars func got empty image and skipped it")
        return None
    
    import cv2
    import numpy as np
    

    crop_size = 240

    image_height, image_width = image.shape[:2]

    x1 = (image_width - crop_size) // 2
    y1 = (image_height - crop_size) // 2

    x2 = x1 + crop_size
    y2 = y1 + crop_size

    # image_cropped = image[y1:y2, x1:x2]
    image_cropped = image

    rgb_image = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2RGB)
    
    rgb_image = cv2.GaussianBlur(rgb_image, (11, 11), 0)
    # cv2.imshow('na', rgb_image)
    
    lower_black = np.array([200, 200, 200])
    upper_black = np.array([250, 250, 250])

    black_mask = cv2.inRange(rgb_image, lower_black, upper_black)

    kernel = np.ones((11,11), np.uint8)
    mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    mask = mask    
    
    

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            centers.append((center_x, center_y))
    
    for center in centers:
        cv2.circle(image, center, 5, (255, 0 , 0), -1)
            
    return cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)  #np.count_nonzero(mask == 255) / (160**2) >= 0.15


# def get_number(image, nums):
#     import cv2
#     import numpy as np
    
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     lower_black = np.array([0, 0, 0])
#     upper_black = np.array([180, 255, 100])

#     black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
        
#     contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     filtered_contours = []
#     min_contour_area = 1000 

#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if  200 < area and area < min_contour_area:
#             filtered_contours.append(contour)
            


#     black_mask = np.zeros_like(black_mask)
#     cv2.drawContours(black_mask, filtered_contours, -1, (255), thickness=cv2.FILLED)
#     black_mask = cv2.bitwise_not(black_mask)

#     orig_len = len(nums)
    
#     for angle in range(0, 360, 45):
        
#         height, width = black_mask.shape[:2]
#         center = (width / 2, height / 2)
#         rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
#         rotated_image = cv2.warpAffine(black_mask, rotation_matrix, (width, height))

#         orig_height, orig_width = black_mask.shape[:2]
#         rotated_orig_image = cv2.warpAffine(image, rotation_matrix, (orig_width, orig_height))
        
#         import pytesseract

#         custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABEKMHOPCTYXabekmhopctyx'
#         text = pytesseract.image_to_string(rotated_image, config=custom_config)  
#         text_from_orig = pytesseract.image_to_string(rotated_orig_image, config=custom_config)  
        
#         for string in text.split('\n'):
#             for substring in string.split(' '):
#                 if len(substring) < 4 :
#                     continue
#                 nums.add(string)
#             if orig_len < len(nums):
#                 break
        
#         for string in text_from_orig.split('\n'):
#             for substring in string.split(' '):
#                 if len(substring) < 4 :
#                     continue
#                 nums.add(string)
#             if orig_len < len(nums):
#                 break
#     return nums


def get_num(image, nums):
    import cv2
    import numpy as np
            

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)[1]   #THRESH_OTSU


    for angle in range(0, 360, 45):
        
        height, width = thresh.shape[:2]
        center = (width / 2, height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        rotated_image = cv2.warpAffine(thresh, rotation_matrix, (width, height))
        
        import pytesseract

        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABEKMHOPCTYXmopcyx'
        text = pytesseract.image_to_string(rotated_image, config=custom_config)  
        import re
        filtered = re.sub(r'[^0123456789ABEKMHOPCTYXabekmhopctyx\n\s]', '', text)
        result = re.split(r'[^a-zA-Z0-9]', filtered)
        for substring in result:
            if len(substring) > 3 :
                nums.add(substring.upper())
                return nums


        # for string in text.split('\n'):
        #     for substring in string.split(' '):
        #         if len(substring) > 4 :
        #             nums.add(string)
        #             return nums
        
    return nums