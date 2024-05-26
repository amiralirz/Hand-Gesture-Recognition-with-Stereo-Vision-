import cv2
import glob
import numpy as np
import pickle as pkl

# This program gets the location of checkerborad corners from the user and the stores them in a pkl file

def select_corners(event, x, y, flags, param):
    global click_counter
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"X = {x}, Y = {y}, count = {click_counter}")
        click_counter += 1
        color = (10, 250 - (200/pattern_area) * click_counter, 50 + (200/pattern_area) * click_counter)
        cv2.circle(img, (x + x_offset, y + y_offset), 5, color, 1)
        cv2.imshow('Image', moved)  
        points.append(((x+x_offset)/scale, (y+y_offset)/scale))

pattern_size = (4, 4)
pattern_area = pattern_size[0] * pattern_size[1]
scale = 1.8
points = []
images = glob.glob('./images/*.jpg')
click_counter = 0

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 

# Defining the world coordinates for 3D points
objp = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:pattern_size[1],0:pattern_size[0]].T.reshape(-1,2)

for i, image_path in enumerate(images):
    img_original = cv2.imread(image_path)
    dim = (int(img_original.shape[1] * scale), int(img_original.shape[0] * scale))
    img = cv2.resize(img_original, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('Image', img)
    click_counter = 0
    cv2.setMouseCallback('Image', select_corners)
    x_offset = 0
    y_offset = 0
    points = []
    while True:
        if len(points) == pattern_area:
            break
        key = cv2.waitKey(1) & 0xff
        if key == ord('0'):
            break
        elif key == ord('a'):
            x_offset = max(0, x_offset - 10)
        elif key == ord('w'):
            y_offset = max(0, y_offset - 10)
        elif key == ord('d'):
            x_offset += 10  
        elif key == ord('s'):
             y_offset += 10
        moved = img[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]]
        cv2.imshow('Image', moved)
    imgpt = np.array(points).reshape((pattern_area, 1, 2))
    imgpoints.append(imgpt)
    objpoints.append(objp)


cv2.destroyAllWindows()

# objpoints = [x.reshape(1, pattern_area, pattern_size[1]) for x in objpoints]
# imgpoints = [np.float32(x) for x in imgpoints]

# storing the objects in pickle filses

objpoints = [x.reshape(1, pattern_area, 3) for x in objpoints]
imgpoints = [np.float32(x) for x in imgpoints]

with open('objpoint.pkl','wb') as f:
    pkl.dump(objpoints, f)

with open('imgpoints.pkl','wb') as f:
    pkl.dump(imgpoints, f)
