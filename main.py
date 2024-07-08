# import cv2
# import random
# import argparse
# import mediapipe as mp


# import sys
# sys.path.append("./")
# from utility import Util


# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils

# hand_tracker = mp_hands.Hands(static_image_mode=False,
#                               max_num_hands=2,
#                               min_detection_confidence=0.7, 
#                               min_tracking_confidence=0.7)

# mouse = Controller()

# screen_width, screen_height = pyautogui.size()

# def arg_type(value):
#     try:
#         return int(value)
#     except ValueError:
#         return value


# def RunMain(src):
#     print("Running program...")
#     cam = cv2.VideoCapture(src)
    
#     if cam.isOpened():
#         Loop = True
#         while Loop:
#             success, frame = cam.read()
#             frame = cv2.flip(frame, 1)
#             if success:
#                 detect_hands = hand_tracker.process(frame)
#                 if detect_hands.multi_hand_landmarks:
#                     for hand_landmarks in detect_hands.multi_hand_landmarks:
#                         mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
#                 cv2.imshow("Display", frame)
#                 if cv2.waitKey(1) == ord("q"):
#                     Loop = False
#     cam.release()
#     cv2.destroyAllWindows()
    
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-s", "--Source", type=arg_type)
#     args = parser.parse_args()
#     RunMain(src=args.Source)




import numpy as np
import cv2
import mediapipe as mp
import random
from PIL import ImageGrab
from pynput.mouse import Button, Controller

mouse = Controller()

screen_width, screen_height = ImageGrab.grab().size

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):
    if len(landmark_list) < 2:
        return
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2 - x1, y2 - y1)
    return np.interp(L, [0, 1], [0, 1000])

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None, None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        mouse.position = (x, y)

def is_left_click(landmark_list, thumb_index_dist):
    return (
        get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmark_list, thumb_index_dist):
    return (
        get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
        thumb_index_dist > 50
    )

def is_double_click(landmark_list, thumb_index_dist):
    return (
        get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist > 50
    )

def is_screenshot(landmark_list, thumb_index_dist):
    return (
        get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist < 50
    )

def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = get_distance([landmark_list[4], landmark_list[5]])

        if get_distance([landmark_list[4], landmark_list[5]]) < 50 and get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.click(Button.left, 1)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.click(Button.right, 1)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            mouse.click(Button.left, 2)
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list, thumb_index_dist):
            im1 = ImageGrab.grab()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
