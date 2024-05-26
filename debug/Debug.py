import pickle as pkl
import cv2
from undistort import calibrator
import mediapipe as mp
from Stereo_vision import stereo

calib = [calibrator("./calibration objects\cam1_calib.pkl"), calibrator("./calibration objects\cam2_calib.pkl")]
print("calibration objects loaded successfully")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles 
mp_hands = mp.solutions.hands

hands = [mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence= 0.5), mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence= 0.5)]
print("mediapipe models created successfully")

caps = [cv2.VideoCapture(0, cv2.CAP_DSHOW), cv2.VideoCapture(1, cv2.CAP_DSHOW)]
successes = [0,0]
images = [0,0]
results = [0, 0]
stereo_object = stereo(9, 1.0157791196778294, 60)

while True:
    successes[0], images[0] = caps[0].read()
    successes[1], images[1] = caps[1].read()

    cam_points = [[], []]

    if not successes[0] or not successes[1]:
        print("One of the cameras failed")
        exit()    
    
    for index, image in enumerate(images):
        image.flags.writeable = False
        image = calib[index].undistort(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        results[index] = hands[index].process(image)
        # Draw hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results[index].multi_hand_landmarks:
            for hand_landmarks in results[index].multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
            # Flip the image horizontally for a selfie-view display.
        cv2.imshow(f'MediaPipe Hands - {index}', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
    
    hands_found = True
    for i in range(2):
        if not results[i].multi_hand_landmarks:
            hands_found = False

    if not hands_found:
        continue    
    
    for i in range(2):
        main_hand = results[i].multi_hand_landmarks[0]
        h = images[i].shape[0] # height of image
        w = images[i].shape[1] # width of image
        points = []
        for landmark in main_hand.landmark: 
            point = (landmark.x * w, landmark.y * h) # 
            points.append(point)
        
        cam_points[i] = points.copy()
    
    points3d = []

    for i in range(21):
        pos3d = stereo_object.locate(cam_points[0][i], cam_points[1][i])
        points3d.append(pos3d)        
        