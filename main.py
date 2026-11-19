"""
Site Safety Watch — Computer Vision Backend
YOLOv8-Pose Anatomical Keypoint Detection & PPE Compliance Analysis
EWIT 2026 Hackathon (1st Runner-Up)
"""
import os
import cv2
import numpy as np
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ultralytics import YOLO
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Site Safety Watch API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load YOLOv8-Pose model
model = YOLO('yolov8n-pose.pt')

# Set VIDEO_SOURCE in your .env file (see .env.example)
VIDEO_SOURCE = os.getenv("VIDEO_SOURCE", "http://192.168.1.100:8080/video")

# --- THREADED VIDEO STREAM TO ELIMINATE NETWORK LAG ---
class CameraStream:
    def __init__(self, src):
        self.stream = cv2.VideoCapture(src)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.lock = threading.Lock()
        
    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self
        
    def update(self):
        while not self.stopped:
            if self.stream.isOpened():
                grabbed, frame = self.stream.read()
                if grabbed:
                    with self.lock:
                        self.grabbed = grabbed
                        self.frame = frame
            else:
                self.stream = cv2.VideoCapture(VIDEO_SOURCE)
                
    def read(self):
        with self.lock:
            if self.frame is None:
                return False, None
            return self.grabbed, self.frame.copy()
            
    def stop(self):
        self.stopped = True
        self.stream.release()

# Start background stream thread
cam = CameraStream(VIDEO_SOURCE).start()

def generate_frames():
    while not cam.stopped:
        success, frame = cam.read()
        if not success or frame is None:
            continue
            
        # Optional: Resize frame slightly for lightning-fast YOLO inference if needed
        # frame = cv2.resize(frame, (640, 480))
        
        # Run YOLOv8-Pose inference (verbose=False speeds it up)
        results = model(frame, conf=0.5, verbose=False)
        
        # Draw skeleton and keypoints automatically without default box labels
        annotated_frame = results[0].plot(boxes=False) 
        
        if results[0].boxes is not None and results[0].keypoints is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            keypoints = results[0].keypoints.xy.cpu().numpy()
            
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box[:4])
                kpts = keypoints[i] if i < len(keypoints) else None
                
                has_helmet = False
                has_vest = False
                
                if kpts is not None and len(kpts) > 12:
                    nose = kpts[0]
                    left_shoulder = kpts[5]
                    right_shoulder = kpts[6]
                    
                    # --- 1. HARD HAT CHECK ---
                    if nose[0] > 0 and nose[1] > 0:
                        hat_y2 = int(nose[1]) - 5
                        hat_y1 = max(0, hat_y2 - int((y2 - y1) * 0.22))
                        hat_x1 = max(0, int(nose[0] - 35))
                        hat_x2 = min(frame.shape[1], int(nose[0] + 35))
                        
                        if hat_y1 < hat_y2 and hat_x1 < hat_x2:
                            head_region = frame[hat_y1:hat_y2, hat_x1:hat_x2]
                            if head_region.size > 0:
                                hsv_head = cv2.cvtColor(head_region, cv2.COLOR_BGR2HSV)
                                
                                lower_hat = np.array([20, 140, 180])
                                upper_hat = np.array([35, 255, 255])
                                mask_hat1 = cv2.inRange(hsv_head, lower_hat, upper_hat)
                                
                                lower_white = np.array([0, 0, 220])
                                upper_white = np.array([180, 25, 255])
                                mask_hat2 = cv2.inRange(hsv_head, lower_white, upper_white)
                                
                                total_hat = cv2.countNonZero(mask_hat1) + cv2.countNonZero(mask_hat2)
                                has_helmet = total_hat > 45 
                    
                    # --- 2. VEST CHECK ---
                    if left_shoulder[0] > 0 and right_shoulder[0] > 0:
                        torso_y1 = int(min(left_shoulder[1], right_shoulder[1]))
                        torso_y2 = int(torso_y1 + (y2 - y1) * 0.40)
                        torso_x1 = max(0, int(min(left_shoulder[0], right_shoulder[0]) - 15))
                        torso_x2 = min(frame.shape[1], int(max(left_shoulder[0], right_shoulder[0]) + 15))
                        
                        if torso_y1 < torso_y2 and torso_x1 < torso_x2:
                            torso_region = frame[torso_y1:torso_y2, torso_x1:torso_x2]
                            if torso_region.size > 0:
                                hsv_torso = cv2.cvtColor(torso_region, cv2.COLOR_BGR2HSV)
                                lower_vest = np.array([15, 100, 100])
                                upper_vest = np.array([38, 255, 255])
                                mask_vest = cv2.inRange(hsv_torso, lower_vest, upper_vest)
                                has_vest = cv2.countNonZero(mask_vest) > 80

                # Compliance Status styling
                all_safe = has_helmet and has_vest
                box_color = (0, 255, 0) if all_safe else (0, 0, 255)
                
                helmet_text = "HELMET: OK" if has_helmet else "NO HELMET!"
                vest_text = "VEST: OK" if has_vest else "NO VEST!"
                
                # Draw sleek person bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), box_color, 2)
                
                # POSITION TEXT SAFELY ABOVE THE BOX (NO OVERLAP)
                badge_y = max(35, y1 - 15)
                combined_status = f"{helmet_text}  |  {vest_text}"
                badge_color = (0, 255, 0) if all_safe else (0, 0, 255)
                
                # Draw background banner and text
                (text_w, text_h), _ = cv2.getTextSize(combined_status, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(annotated_frame, (x1, badge_y - text_h - 10), (x1 + text_w + 10, badge_y + 5), (0, 0, 0), -1)
                cv2.rectangle(annotated_frame, (x1, badge_y - text_h - 10), (x1 + text_w + 10, badge_y + 5), badge_color, 2)
                cv2.putText(annotated_frame, combined_status, (x1 + 5, badge_y - 2), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, badge_color, 2)

        # Compress JPEG quality slightly (e.g. 80%) for rapid browser network transfer
        ret, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=host, port=port)