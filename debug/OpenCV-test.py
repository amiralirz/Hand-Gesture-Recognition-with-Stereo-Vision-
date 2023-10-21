import cv2 as cv
import numpy as np
import time

class timeit():
    import time
    def __enter__(self):
        self.tic = self.time.perf_counter()
    def __exit__(self, *args, **kwargs):
        print(f'runtime: {self.time.perf_counter() - self.tic} seconds')


# img = np.zeros((512,512,3), np.uint8)
# cv.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv.LINE_AA)
# cv.imshow('hi',img)
# cv.waitKey(0)

font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 2
font_thickness = 3
text_position = (0, 100)
text_color = (255, 255, 255)
pt = time.time()

with timeit():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    # image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    fps = 1/(time.time() - pt)
    pt = time.time()
    image = cv.putText(image,f'fps : {fps:.2f}', text_position, font, font_scale, text_color, font_thickness, cv.LINE_AA)
    cv.imshow('MediaPipe Hands', image)
    if cv.waitKey(5) & 0xFF == 27:
      break
    