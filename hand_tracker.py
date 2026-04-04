import cv2
import mediapipe as mp

BUFFER_SIZE = 5
MAX_NUM_HANDS = 2
CROP_TOP = 60
CROP_BOTTOM = 420

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=MAX_NUM_HANDS)
        self.draw = mp.solutions.drawing_utils

    def process(self, img):
        img = cv2.flip(img, 1)
        img = img[CROP_TOP:CROP_BOTTOM, 0:640]

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        right_hand = None
        left_hand = None

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                self.draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                label = handedness.classification[0].label

                if label == "Right":
                    right_hand = hand_landmarks.landmark
                else:
                    left_hand = hand_landmarks.landmark

        return img, right_hand, left_hand