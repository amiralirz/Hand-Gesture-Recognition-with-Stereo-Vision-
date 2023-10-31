import cv2
import glob

def select_corners(event, x, y, flags, param):
    global previous_point
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"X = {x}, Y = {y}")
        cv2.circle(img, (x, y), 5, (0, 0, 255), 1)
        cv2.imshow('Image', img)

pattern_size = (4,4)

criteria = (cv2.TERM_CRITERIA_EPS, 30, 0.001)

images = glob.glob('./images/*.jpg')

for i, image_path in enumerate(images):
    img = cv2.imread(image_path)
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', select_corners, (i))
    cv2.waitKey(0)

cv2.destroyAllWindows()