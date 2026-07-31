import numpy as np
import cv2

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()

prev_Img = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

hsv_mask = np.zeros_like(frame1)
hsv_mask[:,:, 1] = 255

while True:
    ret, frame2 = cap.read()
    next_Img = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(
        prev_Img,
        next_Img,
        np.zeros((prev_Img.shape[0], prev_Img.shape[1], 2), dtype=np.float32),
        0.5,
        3,
        15,
        3,
        5,
        1.2,
        0,
    )

    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv_mask[:,:, 0] = ang / 2
    #burda mag demek hareketin büyüklüğü demek. yani hareketin ne kadar hızlı olduğunu gösterir. norm_mag ise mag değerini normalize eder. yani 0 ile 255 arasında bir değer verir. bu sayede hsv_mask[:,:, 2] ye atayabiliriz. hsv_mask[:,:, 2] ise hsv renk uzayında value (değer) kanalını temsil eder. yani hareketin büyüklüğünü renk olarak gösterebiliriz.
    norm_mag = np.zeros_like(mag, dtype=np.float32)
    cv2.normalize(mag, norm_mag, 0, 255, cv2.NORM_MINMAX)
    hsv_mask[:,:, 2] = norm_mag

    bgr_flow = cv2.cvtColor(hsv_mask, cv2.COLOR_HSV2BGR)
    cv2.imshow("Optical Flow", bgr_flow)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    prev_Img = next_Img

cap.release()
cv2.destroyAllWindows()
