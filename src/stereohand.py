import pickle as pkl
import cv2
from undistort import calibrator
import mediapipe as mp
from stereovision import Stereo


class StereoHand:
    def __init__(self):
        self.calib = [calibrator("./calibration objects\cam1_calib.pkl"), calibrator("./calibration objects\cam2_calib.pkl")]
        print("calibration objects loaded successfully")

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles 
        self.mp_hands = mp.solutions.hands

        self.hands = [self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence= 0.5), self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence= 0.5)]
        print("mediapipe models created successfully")

        self.caps = [cv2.VideoCapture(0, cv2.CAP_DSHOW), cv2.VideoCapture(1, cv2.CAP_DSHOW)]
        self.successes = [0,0]
        self.images = [0,0]
        self.results = [0, 0]
        self.stereo_object = Stereo(9, 1.0157791196778294, 60)
        # self.stereo_object = Stereo(9, 1.0157791196778294, 0)
    
    def get_hand(self):
        self.successes[0], self.images[0] = self.caps[0].read()
        self.successes[1], self.images[1] = self.caps[1].read()

        self.cam_points = [[], []]

        if not self.successes[0] or not self.successes[1]:
            print("One of the cameras failed")
            return False, [(0, 0, 0)]
                
        
        for index, image in enumerate(self.images):
            image.flags.writeable = False
            image = self.calib[index].undistort(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            self.results[index] = self.hands[index].process(image)
            # Draw hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if self.results[index].multi_hand_landmarks:
                for hand_landmarks in self.results[index].multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style())
                # Flip the image horizontally for a selfie-view display.
            cv2.imshow(f'MediaPipe Hands - {index}', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        
        
        self.hands_found = True
        for i in range(2):
            if not self.results[i].multi_hand_landmarks:
                self.hands_found = False

        if not self.hands_found:
            return False, [(0, 0, 0)]
        
        for i in range(2):
            self.main_hand = self.results[i].multi_hand_landmarks[0]
            self.h = self.images[i].shape[0] # height of image
            self.w = self.images[i].shape[1] # width of image
            self.points = []
            for landmark in self.main_hand.landmark: 
                self.point = (landmark.x * self.w, landmark.y * self.h) # 
                self.points.append(self.point)
            
            self.cam_points[i] = self.points.copy()
        
        self.points3d = []

        for i in range(21):
            self.pos3d = self.stereo_object.locate(self.cam_points[0][i], self.cam_points[1][i])
            self.points3d.append(self.pos3d) 
        
        return True, self.points3d
