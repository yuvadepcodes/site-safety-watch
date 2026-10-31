import cv2
from ultralytics import YOLO

print("Loading YOLOv8-Pose model...")
model = YOLO("yolov8n-pose.pt")

# Your phone's IP Webcam stream URL
video_source = "http://10.42.0.82:8080/video"

print(f"Connecting to phone stream at {video_source}...")
cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print("Error: Could not open video stream. Check if IP Webcam is running and Wi-Fi matches.")
    exit()

print("Stream connected! Press 'q' in the video window to exit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from phone.")
        break

    # Run YOLOv8 pose estimation
    results = model(frame, stream=True, verbose=False)

    for r in results:
        annotated_frame = r.plot()
        cv2.imshow("Site Safety Watch - Phone Camera Test", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()