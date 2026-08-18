import cv2
import serial
import time
import sys

#values found for specific lighting using calibrate_color.py
color_ranges = {
    #"red": (np.array([, ,]), np.array([, ,]))
    #"green": (np.array([, ,]), np.array([, ,]))
    #"blue": (np.array([, ,]), np.array([, ,]))
    #"white": (np.array([, ,]), np.array([, ,]))
}

def setup_arduino(port='COM5', baud=9600):
    try:
        arduino = serial.Serial(port, baud, timeout=1)
    except serial.SerialException as e:
        sys.exit(f"couldn't open {port}: {e}")
    time.sleep(2)  #arduino resets
    return arduino

def setup_camera():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        sys.exit("couldn't open camera")
    return cap

def main():
    arduino = setup_arduino()
    cap = setup_camera()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: couldn't read frame")
            break

        #TODO: hsv_roi using aruco
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        color = "misc"
        best_area = 500 #set to minimum area first 500 seems good

        for color_name, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                continue
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            if area > best_area:
                color = color_name
                best_area = area
        
        
        #TODO: arduino.write(b"")

        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): #escape if 'q' pressed and wait 1 millisecond for frame to load and such
            break

    cap.release()
    cv2.destroyAllWindows()