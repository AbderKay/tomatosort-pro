import cv2
import time
import numpy as np
from ultralytics import YOLO

def main():
    model = YOLO("models/tomatosort_pro_v1_best_openvino_model/", task='detect')

    cam_source = 0 
    cap = cv2.VideoCapture(cam_source)
    
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    if not cap.isOpened():
        return

    TOMATO_CLASS_ID = 0  
    prev_frame_time = 0
    frame_count = 0
    SKIP_FRAMES = 2  
    
    last_boxes = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        new_frame_time = time.time()
        time_diff = new_frame_time - prev_frame_time
        fps = 1 / time_diff if time_diff > 0 else 30
        prev_frame_time = new_frame_time

        if frame_count % SKIP_FRAMES == 0 or last_boxes is None:
            results = model.predict(source=frame, conf=0.20, verbose=False)[0]
            last_boxes = results.boxes
            
        tomato_count = 0
        foreign_count = 0

        annotated_frame = frame.copy()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_dark = np.array([0, 0, 0])
        upper_dark = np.array([180, 255, 80])
        dark_mask = cv2.inRange(hsv, lower_dark, upper_dark)
        
        kernel = np.ones((5,5), np.uint8)
        dark_mask = cv2.morphologyEx(dark_mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 1500:
                x, y, w, h = cv2.boundingRect(contour)
                if w < (FRAME_WIDTH * 0.8) and h < (FRAME_HEIGHT * 0.8):
                    foreign_count += 1
                    cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(annotated_frame, "Intrus", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if last_boxes is not None:
            for box in last_boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                xyxy = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = map(int, xyxy)

                box_width = x2 - x1

                is_too_large = box_width > (FRAME_WIDTH * 0.15)

                if cls == TOMATO_CLASS_ID and conf >= 0.70 and not is_too_large:
                    tomato_count += 1
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f"Tomate {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                
                else:
                    foreign_count += 1
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(annotated_frame, "Intrus", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(annotated_frame, f"FPS: {int(fps)} (Intel OpenVINO)", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(annotated_frame, f"Tomates valides: {tomato_count}", (20, 75), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Alertes Intrus: {foreign_count}", (20, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if foreign_count > 0:
            cv2.rectangle(annotated_frame, (0, 0), (640, 480), (0, 0, 255), 5) 
            cv2.putText(annotated_frame, f"ALERTE FLUX : {foreign_count} INTRUS", (20, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Tomato Sort - Intel Optimized', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()