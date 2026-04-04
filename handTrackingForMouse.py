import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from collections import deque

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

buffer_x = deque(maxlen=5)
buffer_y = deque(maxlen=5)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # aynalı görüntü

    # Kameradan gelen görüntüyü 16:9'a kırp
    crop_top = 60   # üstten 60 piksel kes
    crop_bottom = 420  # alta kadar

    img = img[crop_top:crop_bottom, 0:640]
    h, w, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark

            # İşaret parmağı ucu
            x = lm[8].x
            y = lm[8].y

            buffer_x.append(x)
            buffer_y.append(y)

            smooth_x = sum(buffer_x) / len(buffer_x)
            smooth_y = sum(buffer_y) / len(buffer_y)

            mouse_x = int(np.interp(smooth_x, [0, 1], [0, screen_w]))
            mouse_y = int(np.interp(smooth_y, [crop_top/480, crop_bottom/480], [0, screen_h]))
            pyautogui.moveTo(mouse_x, mouse_y, duration=0.05)

    cv2.imshow("Hand Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()