import pyautogui
import numpy as np
from collections import deque
from pynput.mouse import Controller as MouseCtrl

BUFFER_SIZE = 5

pyautogui.FAILSAFE = False

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        self.buffer_x = deque(maxlen=BUFFER_SIZE)
        self.buffer_y = deque(maxlen=BUFFER_SIZE)
        self.pynput_mouse = MouseCtrl()

    def move(self, lm):
        self.buffer_x.append(lm[8].x)
        self.buffer_y.append(lm[8].y)

        smooth_x = sum(self.buffer_x) / len(self.buffer_x)
        smooth_y = sum(self.buffer_y) / len(self.buffer_y)

        mouse_x = int(np.interp(smooth_x, [0.05, 0.95], [0, self.screen_w]))
        mouse_y = int(np.interp(smooth_y, [0.05, 0.95], [0, self.screen_h]))

        mouse_x = max(0, min(self.screen_w, mouse_x))
        mouse_y = max(0, min(self.screen_h, mouse_y))

        pyautogui.moveTo(mouse_x, mouse_y, duration=0.05)

    def left_click(self):
        pyautogui.click()

    def right_click(self):
        pyautogui.rightClick()

    def scroll(self, amount):
        if amount != 0:
            self.pynput_mouse.scroll(0, amount)