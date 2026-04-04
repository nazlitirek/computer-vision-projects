###THIS IS NOT WORKING PROPERLY, DO NOT USE THIS CODE.###

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from collections import deque

cap = cv2.VideoCapture(0)
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Son 5 karenin ortalamasını al
buffer = deque(maxlen=5)

pyautogui.FAILSAFE = False

while True:
    success, img = cap.read()
    h, w, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            lm = face_landmarks.landmark

            left_corner  = (int(lm[33].x * w),  int(lm[33].y * h))
            right_corner = (int(lm[133].x * w), int(lm[133].y * h))
            pupil        = (int(lm[468].x * w), int(lm[468].y * h))

            eye_width = right_corner[0] - left_corner[0]
            pupil_ratio_x = (pupil[0] - left_corner[0]) / eye_width

            buffer.append(pupil_ratio_x)
            smooth_ratio = sum(buffer) / len(buffer)

            mouse_x = int(np.interp(smooth_ratio, [0.42, 0.68], [0, screen_w]))
            mouse_x = max(0, min(screen_w, mouse_x))

            pyautogui.moveTo(mouse_x, screen_h // 2, duration=0.05)

            cv2.circle(img, left_corner,  3, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, right_corner, 3, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, pupil,        5, (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f"Ratio: {smooth_ratio:.2f}", (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Eye Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()