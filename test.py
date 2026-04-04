import cv2

cap = cv2.VideoCapture(0)
print(f"Kamera genişlik: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
print(f"Kamera yükseklik: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
cap.release()
import pyautogui
print(pyautogui.size())