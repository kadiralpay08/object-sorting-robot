import cv2

url = "http://192.168.1.104:4747/video"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Error: couldn't open camera stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: couldn't read frame")
        break

    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()