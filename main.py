import cv2
import mediapipe as mp
import pyautogui
import subprocess
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Gesture action mapping
def perform_action(gesture_name):
    if gesture_name == "PINCH":
        pyautogui.click()
    elif gesture_name == "OPEN_PALM":
        subprocess.Popen("explorer")
    elif gesture_name == "FIST":
        pyautogui.hotkey('win', 'd')
    elif gesture_name == "VICTORY":
        pyautogui.hotkey('ctrl', 'tab')
    elif gesture_name == "THUMB_UP":
        pyautogui.press("volumeup")
    elif gesture_name == "THUMB_DOWN":
        pyautogui.press("volumedown")

# Detect gesture name
def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark

    # Calculate distances
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    wrist = landmarks[0]

    thumb_index_dist = math.dist(
        (thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y)
    )
    index_middle_dist = math.dist(
        (index_tip.x, index_tip.y), (middle_tip.x, middle_tip.y)
    )

    # Gesture classification (simple logic)
    if thumb_index_dist < 0.05:  # Pinch
        return "PINCH"
    elif all(landmarks[i].y < wrist.y for i in [8, 12, 16, 20]):
        return "OPEN_PALM"
    elif all(landmarks[i].y > wrist.y for i in [8, 12, 16, 20]):
        return "FIST"
    elif (landmarks[8].y < wrist.y and landmarks[12].y < wrist.y and
          landmarks[16].y > wrist.y and landmarks[20].y > wrist.y):
        return "VICTORY"
    elif landmarks[4].y < wrist.y and landmarks[8].y > wrist.y:
        return "THUMB_UP"
    elif landmarks[4].y > wrist.y and landmarks[8].y > wrist.y:
        return "THUMB_DOWN"

    return None

# Main program
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                gesture = detect_gesture(hand_landmarks)
                if gesture:
                    cv2.putText(image, gesture, (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    perform_action(gesture)

        cv2.imshow('Air Control - Rhythm', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit
            break

cap.release()
cv2.destroyAllWindows()
