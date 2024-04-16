import cv2
import glob
import numpy as np
import pickle as pkl

images_address = glob.glob("./images/*.jpg") # path to images folder
pattern_size = (7, 10)
pattern_area = pattern_size[0] * pattern_size[1]

objp = np.zeros((pattern_area,3), np.float32)
objp[:,:2] = np.mgrid[0:pattern_size[0],0:pattern_size[1]].T.reshape(-1,2)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 3
text_position = (0, 100)
text_color = (0, 0, 255)

for i, address in enumerate(images_address):
    img = cv2.imread(address)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(img, pattern_size)
    if not found:
        continue
    objpoints.append(objp)
    imgpoints.append(cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria))
    cv2.drawChessboardCorners(img, pattern_size, corners, found)
    output_image = cv2.putText(img,f'No. : {i+1}', (0, img.shape[0]-20), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
    cv2.imshow('Chessboard',output_image)
    cv2.waitKey(0)


gray = cv2.cvtColor(cv2.imread(images_address[0]), cv2.COLOR_BGR2GRAY)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

with open('calibration_data.pkl','wb') as f:
    pkl.dump((ret, mtx, dist, rvecs, tvecs), f)
