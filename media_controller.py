import cv2
import time
import keyboard
from gesture_detection import HandGestureDetector

detector = HandGestureDetector(detection_confidence=0.8)

cap = cv2.VideoCapture(0)
prev_action = None
action_cooldown = 1.5  # seconds
last_action_time = time.time()

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)

    if lmList:
        fingers = detector.fingers_up()

        current_time = time.time()

        # Play/Pause - All fingers up
        if fingers == [1, 1, 1, 1, 1] and (current_time - last_action_time > action_cooldown):
            keyboard.send("play/pause media")
            prev_action = "play/pause"
            last_action_time = current_time

        # Next Track - Only Index finger up
        elif fingers == [0, 1, 0, 0, 0] and (current_time - last_action_time > action_cooldown):
            keyboard.send("next track")
            prev_action = "next"
            last_action_time = current_time

        # Previous Track - Only Index and Middle finger up
        elif fingers == [0, 1, 1, 0, 0] and (current_time - last_action_time > action_cooldown):
            keyboard.send("previous track")
            prev_action = "previous"
            last_action_time = current_time

        if prev_action:
            cv2.putText(img, f"Action: {prev_action}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Media Controller", img)
    if cv2.waitKey(1) == ord('q'):
        break
