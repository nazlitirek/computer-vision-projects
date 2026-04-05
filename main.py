import cv2
import numpy as np
from hand_tracker import HandTracker
from gestures import GestureDetector
from mouse_control import MouseController
from volume_brightness_control import VolumeController

tracker = HandTracker()
gesture = GestureDetector()
mouse = MouseController()
volume = VolumeController()

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img, right_hand, left_hand = tracker.process(img)
    h, w, _ = img.shape

    # Sağ el → mouse kontrolü
    if right_hand:
        if gesture.is_two_fingers_together(right_hand, w, h):
            scroll = gesture.get_scroll(right_hand, w, h)
            if scroll != 0:
                mouse.scroll(scroll)
                cv2.putText(img, f"SCROLL: {scroll}", (40, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            gesture.prev_scroll_y = None
            if not gesture.is_pinch(right_hand, w, h) and not gesture.is_right_click(right_hand, w, h):
                mouse.move(right_hand)

            if gesture.is_right_click(right_hand, w, h):
                mouse.right_click()
                cv2.putText(img, "SAG TIKLAMA", (40, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif gesture.is_pinch(right_hand, w, h):
                mouse.left_click()
                cv2.putText(img, "SOL TIKLAMA", (40, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Sol el → volume / parlaklık kontrolü
    if left_hand:
        if gesture.is_hand_open(left_hand):
            if gesture.is_two_fingers_together(left_hand, w, h):
                brightness = volume.set_brightness(left_hand, w, h)
                cv2.putText(img, f"BRIGHTNESS: {brightness}%", (400, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            else:
                vol_percent = volume.set_volume(left_hand, w, h)
                cv2.putText(img, f"VOL: {vol_percent}%", (400, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Hand Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()