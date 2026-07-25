import streamlit as st
import cv2
import time
import numpy as np
from ultralytics import YOLO

# --------------------------------------------------
# Configuration Streamlit
# --------------------------------------------------

st.set_page_config(
    page_title="Tomato Sort Dashboard",
    layout="wide"
)

st.title("🍅 Tomato Sort Dashboard")

# --------------------------------------------------
# Modèle
# --------------------------------------------------

@st.cache_resource
def load_model():
    return YOLO(
        "models/tomatosort_pro_v1_best_openvino_model/",
        task="detect"
    )

model = load_model()

# --------------------------------------------------
# Interface
# --------------------------------------------------

left_col, right_col = st.columns([3, 1])

with left_col:
    st.subheader("📹 Flux vidéo")
    video_placeholder = st.empty()

with right_col:
    st.subheader("📊 Statistiques")

    tomato_metric = st.empty()
    anomaly_metric = st.empty()
    rate_metric = st.empty()
    fps_metric = st.empty()

st.subheader("📋 Logs")
log_placeholder = st.empty()

# --------------------------------------------------
# Caméra
# --------------------------------------------------

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not cap.isOpened():
    st.error("Impossible d'ouvrir la caméra")
    st.stop()

# --------------------------------------------------
# Variables
# --------------------------------------------------

TOMATO_CLASS_ID = 0

prev_frame_time = 0
frame_count = 0
SKIP_FRAMES = 2

last_boxes = None
logs = []

# --------------------------------------------------
# Boucle principale
# --------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        st.error("Erreur caméra")
        break

    frame_count += 1

    # FPS
    new_frame_time = time.time()
    time_diff = new_frame_time - prev_frame_time

    fps = 1 / time_diff if time_diff > 0 else 0
    prev_frame_time = new_frame_time

    # YOLO
    if frame_count % SKIP_FRAMES == 0 or last_boxes is None:

        results = model.predict(
            source=frame,
            conf=0.20,
            verbose=False
        )[0]

        last_boxes = results.boxes

    tomato_count = 0
    foreign_count = 0

    annotated_frame = frame.copy()

    # --------------------------------------------------
    # Détection objets sombres
    # --------------------------------------------------

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 80])

    dark_mask = cv2.inRange(
        hsv,
        lower_dark,
        upper_dark
    )

    kernel = np.ones((5, 5), np.uint8)

    dark_mask = cv2.morphologyEx(
        dark_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        dark_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:

        if cv2.contourArea(contour) > 1500:

            x, y, w, h = cv2.boundingRect(contour)

            if (
                w < FRAME_WIDTH * 0.8
                and h < FRAME_HEIGHT * 0.8
            ):

                foreign_count += 1

                cv2.rectangle(
                    annotated_frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    annotated_frame,
                    "Intrus",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )

    # --------------------------------------------------
    # Analyse YOLO
    # --------------------------------------------------

    if last_boxes is not None:

        for box in last_boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].cpu().numpy()
            )

            box_width = x2 - x1

            is_too_large = (
                box_width > FRAME_WIDTH * 0.15
            )

            if (
                cls == TOMATO_CLASS_ID
                and conf >= 0.70
                and not is_too_large
            ):

                tomato_count += 1

                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    annotated_frame,
                    f"Tomate {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            else:

                foreign_count += 1

                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    annotated_frame,
                    "Intrus",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )

    # --------------------------------------------------
    # Taux de détection
    # --------------------------------------------------

    total = tomato_count + foreign_count

    detection_rate = (
        tomato_count / total * 100
        if total > 0 else 0
    )

    # --------------------------------------------------
    # Logs
    # --------------------------------------------------

    current_time = time.strftime("%H:%M:%S")

    if tomato_count > 0:
        logs.append(
            f"{current_time} | 🍅 {tomato_count} tomate(s)"
        )

    if foreign_count > 0:
        logs.append(
            f"{current_time} | ⚠️ {foreign_count} intrus"
        )

    logs = logs[-20:]

    # --------------------------------------------------
    # Affichage vidéo
    # --------------------------------------------------

    frame_rgb = cv2.cvtColor(
        annotated_frame,
        cv2.COLOR_BGR2RGB
    )

    video_placeholder.image(
        frame_rgb,
        channels="RGB",
        width=700
    )

    # --------------------------------------------------
    # Statistiques
    # --------------------------------------------------

    tomato_metric.metric(
        "🍅 Tomates",
        tomato_count
    )

    anomaly_metric.metric(
        "⚠️ Intrus",
        foreign_count
    )

    rate_metric.metric(
        "🎯 Taux",
        f"{detection_rate:.1f}%"
    )

    fps_metric.metric(
        "🚀 FPS",
        int(fps)
    )

    # --------------------------------------------------
    # Logs affichés
    # --------------------------------------------------

    log_placeholder.text(
        "\n".join(logs)
    )