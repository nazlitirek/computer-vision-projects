import cv2


def _create_tracker(tracker_name: str):
    factory = getattr(cv2, f"Tracker{tracker_name}_create", None)
    if callable(factory):
        return factory()

    legacy_module = getattr(cv2, "legacy", None)
    if legacy_module is not None:
        legacy_factory = getattr(legacy_module, f"Tracker{tracker_name}_create", None)
        if callable(legacy_factory):
            return legacy_factory()

    try:
        return cv2.Tracker_create(tracker_name)
    except Exception:
        raise AttributeError(f"Tracker '{tracker_name}' is not available in this OpenCV build.")


def ask_for_tracker():
    print("choose tacker type")
    print("0 boosting")
    print("1 mil")
    print("2 kcf")
    print("3 tld")
    print("4 medianflow")
    choice = input("Enter your choice (0-4): ")

    tracker_map = {
        "0": "Boosting",
        "1": "MIL",
        "2": "KCF",
        "3": "TLD",
        "4": "MedianFlow",
    }

    tracker_name = tracker_map.get(choice)
    if tracker_name is None:
        print("Invalid choice, defaulting to KCF tracker.")
        tracker_name = "KCF"

    return _create_tracker(tracker_name)


def run_tracker_from_camera():
    tracker = ask_for_tracker()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Kamera açılamadı.")

    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Kameradan görüntü okunamadı.")

    bbox = cv2.selectROI("Select Object", frame, False)
    cv2.destroyWindow("Select Object")

    if all(v == 0 for v in bbox):
        raise RuntimeError("Geçersiz ROI seçimi yaptınız.")

    try:
        tracker.init(frame, bbox)
    except Exception as exc:
        raise RuntimeError(f"Tracker başlatılamadı: {exc}") from exc

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ok, bbox = tracker.update(frame)
        if ok:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Tracking lost", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        cv2.imshow("Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_tracker_from_camera()