import cv2  # type: ignore

cap = cv2.VideoCapture("output.mp4")
last_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    last_frame = frame

cap.release()

if last_frame is not None:
    print("frame shape:", last_frame.shape)  # (h, w, c)
    cv2.imwrite("last_frame.png", last_frame)
