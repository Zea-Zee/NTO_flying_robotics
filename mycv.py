import cv2


# PIXEL_HEIGHT = 480
# PIXEL_WIDTH = 854
# PIXEL_HEIGHT = 480
# PIXEL_WIDTH = 854
PIXEL_HEIGHT = 240
PIXEL_WIDTH = 320

# REAL_HEIGHT = 4.5
# REAL_WIDTH = 6.5
REAL_HEIGHT = 3.9
REAL_WIDTH = 5.7
# REAL_HEIGHT = 4
# REAL_WIDTH = 6


def get_cars_positions():
    return 0


def pixels_to_coords(dots: list):
    real_dots = []
    #dots = [(0,0), (320, 0), (0, 240), (0, 0)]
    # dots.append((0, 0))
    # dots.append((320, 240))
    for dot in dots:
        px, py = PIXEL_WIDTH - dot[0], PIXEL_HEIGHT - dot[1]
        print(f"pixels: {px}, {py}")
        rx, ry = (py * REAL_HEIGHT) / PIXEL_HEIGHT - 0.25, (px * REAL_WIDTH) / PIXEL_WIDTH - 0.25
        print(f"coords: {rx}, {ry}")
        real_dots.append((rx, ry))
    return real_dots


def draw_dots(dots, image):
    cv2.circle(image, (0, 0), 3, (0, 0, 0), -1)
    for dot in dots:
        cv2.circle(image, dot, 3, (0, 0, 0), -1)
    cv2.imwrite("/home/clover/Desktop/drawed_centers.jpg", image)



def get_position_to_check_number():
    return 0