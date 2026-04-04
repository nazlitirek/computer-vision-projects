import numpy as np

PINCH_THRESHOLD = 30
RIGHT_CLICK_THRESHOLD = 25
SCROLL_THRESHOLD = 20

class GestureDetector:
    def __init__(self):
        self.prev_scroll_y = None

    def get_point(self, lm, idx, w, h):
        if lm is None:
            return 0, 0
        return int(lm[idx].x * w), int(lm[idx].y * h)

    def is_pinch(self, lm, w, h):
        # Başparmak (4) ve işaret parmağı (8)
        x1, y1 = self.get_point(lm, 4, w, h)
        x2, y2 = self.get_point(lm, 8, w, h)
        dist = np.hypot(x2 - x1, y2 - y1)
        return dist < PINCH_THRESHOLD

    def is_right_click(self, lm, w, h):
        x1, y1 = self.get_point(lm, 4, w, h)
        x2, y2 = self.get_point(lm, 12, w, h)
        dist = np.hypot(x2 - x1, y2 - y1)
        return dist < RIGHT_CLICK_THRESHOLD

    def get_scroll(self, lm, w, h):
        # İşaret (8) ve orta parmak (12) birlikte hareket edince scroll
        _, y1 = self.get_point(lm, 8, w, h)
        _, y2 = self.get_point(lm, 12, w, h)
        mid_y = (y1 + y2) // 2

        scroll = 0
        if self.prev_scroll_y is not None:
            diff = self.prev_scroll_y - mid_y
            if abs(diff) > SCROLL_THRESHOLD:
                scroll = int(diff / 10)
                self.prev_scroll_y = mid_y
        else:
            self.prev_scroll_y = mid_y

        return scroll

    def is_hand_open(self, lm):
        tips =  [8,  12, 16, 20]
        bases = [6,  10, 14, 18]
        
        for tip, base in zip(tips, bases):
            if lm[tip].y > lm[base].y:  # herhangi bir parmak kapalıysa
                return False
        return True

    def get_pinch_distance(self, lm, w, h, finger_tip):
        # başparmak (4) ile istenen parmak arası mesafe
        x1, y1 = self.get_point(lm, 4, w, h)
        x2, y2 = self.get_point(lm, finger_tip, w, h)
        return np.hypot(x2 - x1, y2 - y1)
    
    def is_two_fingers_together(self, lm, w, h):
        # işaret ve orta parmak uçları birbirine yakınsa
        x1, y1 = self.get_point(lm, 8, w, h)
        x2, y2 = self.get_point(lm, 12, w, h)
        dist = np.hypot(x2 - x1, y2 - y1)
        return dist < 40