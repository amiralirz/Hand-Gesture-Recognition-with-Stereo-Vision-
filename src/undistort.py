import pickle as pkl
import cv2
import numpy as np

class calibrator:
    
    def __init__(self, calibration_data:str):
        with open(calibration_data,'rb') as f:
            self.ret, self.mtx, self.dist, self.rvecs, self.tvecs, self.w, self.h= pkl.load(f)
            self.newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.w,self.h), 1, (self.w,self.h))

    def undistort(self, img:np.ndarray)->np.ndarray:
        dst = cv2.undistort(img, self.mtx, self.dist, None, self.newcameramtx)
        x, y, w, h = self.roi
        return dst[y:y+h, x:x+w]
        # return dst
