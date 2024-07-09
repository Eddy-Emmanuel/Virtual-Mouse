import cv2
import argparse
from utility import Utilities

project_utils = Utilities()


def main(src):
    # Load camera from source
    cam = cv2.VideoCapture(src)
    # Set camera size
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
    # Get hand utils
    hands = project_utils.GetHands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_tracking_confidence=0.6,
                                         min_detection_confidence=0.6)
    try:
        # Continue loop while camera is opened
        while cam.isOpened():
            suc, frame = cam.read()
            frame = cv2.flip(frame, 1)
            w, h = project_utils.GetScreenSize
            if not suc:
                print("Unable to capture frame")
            else:
                process_frames = hands.process(frame)
                hand_landmarks = process_frames.multi_hand_landmarks

                # Check for detected hands
                if hand_landmarks:
                    # Loop through detected hands
                    for hand_coordinates in hand_landmarks:
                        # Draw detected points on hands
                        project_utils.GetDrawingUtil.draw_landmarks(frame,
                                                                    hand_coordinates,
                                                                    project_utils.GetHands.HAND_CONNECTIONS)

                        # Get the index finger tip (8) and dip (7) landmarks
                        index_finger_tip = hand_coordinates.landmark[8]
                        index_finger_dip = hand_coordinates.landmark[7]
                        # Get the middle finger tip (12) and dip (11) landmarks
                        middle_finger_tip = hand_coordinates.landmark[12]
                        middle_finger_dip = hand_coordinates.landmark[11]

                        # Get the x and y coordinates with respect to the camera frame
                        index_tip_x, index_tip_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                        index_dip_x, index_dip_y = int(index_finger_dip.x * w), int(index_finger_dip.y * h)
                        middle_tip_x, middle_tip_y = int(middle_finger_tip.x * w), int(middle_finger_tip.y * h)
                        middle_dip_x, middle_dip_y = int(middle_finger_dip.x * w), int(middle_finger_dip.y * h)

                        # Check if the index finger tip is raised
                        index_raised = index_tip_y < index_dip_y #- 10
                        # Check if the middle finger tip is raised
                        middle_raised = middle_tip_y < middle_dip_y #- 10

                        if index_raised:
                            # Move cursor based on user's index finger location
                            project_utils.MoveMouse(x=index_tip_x, y=index_tip_y)

                        if index_raised and middle_raised:
                            # Trigger a click
                            project_utils.MouseClick(x=middle_tip_x, y=middle_tip_y)

                cv2.imshow("virtual_mouse", frame)
                if cv2.waitKey(1) == ord("q"):
                    break
    finally:
        cam.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--Source", type=project_utils.arg_type)
    args = parser.parse_args()
    main(src=args.Source)
