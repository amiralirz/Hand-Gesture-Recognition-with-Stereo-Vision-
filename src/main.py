import threading
import time
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles 
mp_hands = mp.solutions.hands

hands = [mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence= 0.5), mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence= 0.5)]

caps = [cv2.VideoCapture(0, cv2.CAP_DSHOW), cv2.VideoCapture(1, cv2.CAP_DSHOW)]
successes = [0,0]
images = [0,0]

while True:
    successes[0], images[0] = caps[0].read()
    successes[1], images[1] = caps[1].read()

    if not successes[0] or not successes[1]:
        print("One of the cameras failed")
        continue
    
    for index, image in enumerate(images):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands[index].process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
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
