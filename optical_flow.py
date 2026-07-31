import numpy as np
import cv2

#shi tomasi corner detection parametreleri
corner_track_params = {
    "maxCorners": 10,
    "qualityLevel": 0.3,
    "minDistance": 7,
    "blockSize": 7,
}

#burda max level 2 demek, 2 katmanlı piramit kullan demek. yani 2 katmanlı optik akış kullan demek. winSize ise pencere boyutu. criteria ise durma kriteri.
lk_params = dict(winSize=(100, 100), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

cap = cv2.VideoCapture(0)
#burda ret false ise kamera açılamadı demek
ret, prev_frame = cap.read()
ret, prev_frame = cap.read()
if not ret:
    raise RuntimeError("Kamera açılamadı")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prevPts = cv2.goodFeaturesToTrack(
    prev_gray,
    maxCorners=corner_track_params["maxCorners"],
    qualityLevel=corner_track_params["qualityLevel"],
    minDistance=corner_track_params["minDistance"],
    blockSize=corner_track_params["blockSize"],
    useHarrisDetector=False,
)

mask = np.zeros_like(prev_frame)

while True: 
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    nextPts = np.empty_like(prevPts)
    nextPts, status, err = cv2.calcOpticalFlowPyrLK(
        prev_gray,
        frame_gray,
        prevPts,
        nextPts,
        winSize=(100, 100),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
    )

    good_new = nextPts[status == 1]
    good_prev = prevPts[status == 1]

    for i, (new, prev) in enumerate(zip(good_new, good_prev)):

        x_new, y_new = new.ravel()
        x_prev, y_prev = prev.ravel()

        mask = cv2.line(mask, (int(x_new), int(y_new)), (int(x_prev), int(y_prev)), (0, 255, 0), 2)
        frame = cv2.circle(frame, (int(x_new), int(y_new)), 5, (0, 0, 255), 2)

    img = cv2.add(frame, mask)
    cv2.imshow("Optical Flow", img)
    #burda 0XFF demek, sadece son 8 biti al demek. yani sadece son 8 bitin değerini al demek. ord('q') ise q tuşuna basıldığında çıkış yap demek. yani q tuşuna basıldığında break ile döngüden çık demek.
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break