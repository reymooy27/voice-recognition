import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import pyautogui
import time
# from pynput.keyboard import Controller, Key

# Initialize Mediapipe Hand Module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize keyboard controller
# keyboard = Controller()

# Function to simulate key press
# def scroll_up():
#     keyboard.press(Key.page_down)
#     keyboard.release(Key.page_down)
#
# def scroll_down():
#     keyboard.press(Key.page_up)
#     keyboard.release(Key.page_up)

# Start webcam feed
cap = cv2.VideoCapture(0)

# Get screen size for mouse control
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]

            hand_x = int(middle_finger_mcp.x * screen_width)
            hand_y = int(middle_finger_mcp.y * screen_height * 1.2)

            height, width, _ = frame.shape
            middle_x, middle_y = int(middle_finger_tip.x * width), int(middle_finger_tip.y * height)
            middle_mcp_x, middle_mcp_y = int(middle_finger_mcp.x * width), int(middle_finger_mcp.y * height)
            index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)
            thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
            ring_x, ring_y = int(ring_tip.x * width), int(ring_tip.y * height)
            ring_mcp_x, ring_mcp_y = int(ring_mcp.x * width), int(ring_mcp.y * height)

            distance_md_th = ((thumb_x - middle_x) ** 2 + (thumb_y - middle_y) ** 2) ** 0.5
            distance_ind_th = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

            if distance_ind_th < 40:
                pyautogui.click()

            if middle_y < middle_mcp_y and index_y < middle_mcp_y and ring_y > ring_mcp_y:
                print("scroll down")
                pyautogui.scroll(300)
            elif middle_y > middle_mcp_y and index_y > middle_mcp_y :
                print("scroll up")
                pyautogui.scroll(-300)

            # if finger_x < 400:
            #     finger_x -= 200

            pyautogui.moveTo(hand_x, hand_y, tween=pyautogui.easeInOutQuad)

            cv2.putText(frame, f"middle: ({middle_x}, {middle_y})", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"thumb: ({thumb_x}, {thumb_y})", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"index: ({index_x}, {index_y})", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.putText(frame, f"Hand: ({hand_x}, {hand_y})",
                        (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Display finger states
            # fingers = [thumb_up, index_up, middle_up]
            # finger_names = ["Thumb", "Index", "Middle"]
            # for i, is_up in enumerate(fingers):
            #     cv2.putText(frame, f"{finger_names[i]}: {'Up' if is_up else 'Down'}",
            #                 (10, 30 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if is_up else (0, 0, 255), 2)
            #
    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
