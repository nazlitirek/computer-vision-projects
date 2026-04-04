import cv2
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Ses kurulumu - yeni yöntem
from pycaw.utils import AudioUtilities as AU
device = AU.GetSpeakers()
volume_interface = device._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(volume_interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol, max_vol = vol_range[0], vol_range[1]

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    h, w, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark
            x1, y1 = int(lm[4].x * w), int(lm[4].y * h)
            x2, y2 = int(lm[8].x * w), int(lm[8].y * h)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            distance = np.hypot(x2 - x1, y2 - y1)

            vol = np.interp(distance, [20, 210], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)

            vol_percent = int(np.interp(distance, [20, 210], [0, 100]))

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

            cv2.putText(img, f'Vol: {vol_percent}%', (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()