#low saturation can make hue meaningless, research this before making the change
#green rectangle appears on copy you perform calculations on, use frame.copy to avoid this
#use uint8 for the HSV thresholds
import cv2
import sys
import numpy as np

size = 40

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    sys.exit("couldn't open camera")

print("Place the object in the central square. Press 'c' to capture, 'q' to quit.")
count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        c_x, c_y = width//2, height//2
        cv2.rectangle(frame, (c_x-size, c_y-size), (c_x+size, c_y+size), (0, 255, 0), thickness=2)

        cv2.imshow("Calibration", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            roi_bgr = frame[c_y-size+1:c_y+size-1, c_x-size+1:c_x+size-1]
            roi = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)

            h_mean, s_mean, v_mean = roi[:,:,0].mean(), roi[:,:,1].mean(), roi[:,:,2].mean()
            h_std, s_std, v_std = roi[:,:,0].std(), roi[:,:,1].std(), roi[:,:,2].std()
            h_margin, s_margin, v_margin = max(h_std*2.5, 5), max(s_std*2.5, 15), max(v_std*2.5, 15) #adjust values based on trial and error

            lower = np.array([max(0, h_mean-h_margin), max(0, s_mean-s_margin), max(0, v_mean-v_margin)], dtype=int)
            upper = np.array([min(179, h_mean+h_margin), min(255, s_mean+s_margin), min(255, v_mean+v_margin)], dtype=int)

            count += 1
            print(f"Capture {count}:\nLower: {lower[0]}, {lower[1]}, {lower[2]}\nUpper: {upper[0]}, {upper[1]}, {upper[2]}\n")
        elif key == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()