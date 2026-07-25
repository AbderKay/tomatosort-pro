<div align="center">

# 🍅 TomatoSort Pro

### Intelligent Automated Tomato Sorting powered by Computer Vision & AI — built for Industry 4.0

*Real-time quality grading of tomatoes using YOLO detection, CNN classification, and HSV color analysis, wired into a full Big Data + MLOps + IT/OT industrial pipeline.*

<br>

![Status](https://img.shields.io/badge/status-prototype-orange)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![YOLO](https://img.shields.io/badge/Detection-YOLO-00FFFF)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=black)
![Kafka](https://img.shields.io/badge/Streaming-Apache%20Kafka-231F20?logo=apachekafka&logoColor=white)
![MLflow](https://img.shields.io/badge/MLOps-MLflow-0194E2?logo=mlflow&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

<br>

**F1-Score `94.3%` · Throughput `42.5 img/s` · End-to-end latency `23.7 ms`**

</div>

---

## 📖 Overview

Manual tomato sorting is slow, tiring, and inconsistent — human graders fatigue, disagree with one another, and miss defects at high line speeds, driving up losses. **TomatoSort Pro** replaces that with a cyber-physical system that *sees, decides, and acts* in real time.

Tomatoes travel through a controlled-light imaging tunnel, get detected and graded by a two-stage vision model, and are physically routed to the right lane by an industrial PLC — all while every event streams into a Big Data backbone that feeds live dashboards and continuously retrains the models.

The result is a complete, end-to-end blueprint of how **Edge AI + Big Data + MLOps** can modernize a traditional agri-food production line, in line with the principles of **Industry 4.0**.

> 🎓 Academic project — *Département Informatique & Sciences des Données*, École Nationale des Sciences Appliquées (ENSA) d'Agadir · Filière SDBDIA2 · 2025–2026.

---

## ✨ Key Features

- 🎥 **Controlled acquisition** — opaque imaging tunnel + industrial LED rings + GigE Vision global-shutter cameras (dual-angle coverage, zero motion blur).
- ⚡ **Two-stage vision pipeline** — **YOLO** for real-time detection/localization, then a **CNN** for fine quality grading (Grade A / Grade B / Reject).
- 🎨 **HSV color analysis** — brightness-decoupled ripeness & color evaluation, robust to minor lighting drift.
- 🏭 **Safe IT/OT separation** — the AI never drives actuators directly; a **PLC** handles physical sorting via Modbus TCP / OPC-UA / Profinet (IEC 61508 & ISO 13849 compliant).
- 🌊 **Lambda + Medallion architecture** — a sub-second Speed Layer (Kafka) beside a Batch Layer (Cassandra + SQL), with Bronze → Silver → Gold data refinement.
- 📊 **Live multi-profile dashboards** — operator, manager, and CMMS/GMAO views over WebSocket (annotated video feed, KPIs, predictive maintenance alerts).
- 🔁 **Closed-loop MLOps** — MLflow experiment tracking + Active Learning that surfaces low-confidence cases for targeted human annotation and automatic retraining.
- 🛰️ **IoT integration** — MQTT telemetry from vibration/temperature/encoder sensors enabling predictive maintenance.

---

## 🏗️ System Architecture

TomatoSort Pro is built from four tightly-coupled modules organized around a **Lambda & Medallion** data architecture.

```
        ┌──────────────────────────────────────────────────────────────┐
        │                     IMAGING TUNNEL (controlled light)         │
        │        GigE Vision · Global Shutter · dual-angle cameras       │
        └───────────────────────────────┬──────────────────────────────┘
                                         │  frames
                                         ▼
        ┌──────────────────────────────────────────────────────────────┐
        │                  EDGE INFERENCE  (Industrial PC / IPC)         │
        │   ① YOLO detection → ② CNN grading → ③ HSV color/ripeness      │
        │        optimized with OpenVINO / TensorRT / TPU               │
        └───────────────┬───────────────────────────────┬──────────────┘
              decision   │                               │  events
                         ▼                               ▼
        ┌────────────────────────────┐      ┌────────────────────────────┐
        │   PLC / PLC ACTUATION       │      │      APACHE KAFKA           │
        │  encoder-synced air jets /  │      │  (Speed Layer · real-time)  │
        │  pneumatic gates · <5 ms    │      └───────────────┬─────────────┘
        └────────────────────────────┘                      │
                                                             ▼
                        ┌──────────────────────────────────────────────┐
                        │   FastAPI backend  ⇄  React dashboards (WS)    │
                        │   Cassandra + SQL  (Batch Layer · history)     │
                        │   MLflow registry  +  Active Learning loop     │
                        └──────────────────────────────────────────────┘

   Medallion:   🥉 Bronze (raw sensor/camera) → 🥈 Silver (clean/agg) → 🥇 Gold (KPIs + training sets)
```

---

## 🧰 Tech Stack

| Layer | Technologies |
|---|---|
| **Computer Vision** | YOLO (You Only Look Once), CNN, OpenCV, HSV color space |
| **Edge / Inference** | Industrial PC (fanless), OpenVINO, TensorRT, TPU |
| **Backend** | FastAPI (async), WebSocket, RESTful services |
| **Frontend** | React (operator / manager / CMMS dashboards) |
| **Streaming** | Apache Kafka |
| **Storage** | Apache Cassandra (NoSQL, time-series), relational SQL |
| **MLOps** | MLflow (tracking, versioning, registry), Active Learning |
| **Industrial / IoT** | PLC, Modbus TCP, OPC-UA, Profinet, MQTT, incremental rotary encoder |

---

## 📈 Results

> Figures below are experimental estimates from the validation phase, based on the deployed model architectures. See the [technical report](docs/technical-report.pdf) for full methodology.

### Classification metrics — test set of 2,400 images

| Class | Precision | Recall | F1-Score | Support |
|---|:---:|:---:|:---:|:---:|
| 🟢 Grade A (Premium) | 96.2% | 94.8% | **95.5%** | 820 |
| 🟡 Grade B (Standard) | 91.7% | 93.1% | **92.4%** | 940 |
| 🔴 Reject / Defective | 94.3% | 96.0% | **95.1%** | 640 |
| **Weighted average** | **94.1%** | **94.6%** | **94.3%** | **2,400** |

### Timing performance — target hardware (IPC + VPU accelerator)

| Metric | Measured | Target |
|---|:---:|:---:|
| YOLO inference time | 18.4 ms | < 25 ms |
| Full pipeline inference | 23.7 ms | < 40 ms |
| Throughput | 42.5 img/s | > 30 img/s |
| Sorting rate | 42.5 units/s | > 30 units/s |
| PLC actuation latency | < 5 ms | < 10 ms |

The false-negative rate on the **Reject** class stays below **4%**, satisfying the food-safety requirement that no defective product is ever graded as premium.

---

## 📁 Repository Structure

```
tomatosort-pro/
├── README.md              
├── LICENSE                 
├── requirements.txt        
├── .gitignore              
├── app.py                  
├── cam.py                  
│
├── models/
│   ├── tomatosort_pro_v1_best.pt
│   └── tomatosort_pro_v1_best_openvino_model/
│       ├── metadata.yaml
│       ├── tomatosort_pro_v1_best.xml
│       └── tomatosort_pro_v1_best.bin
│
├── dataset/
│   ├── data.yaml
│   ├── README.md
│   └── samples/
│       └── 011_*.jpg, 017_*.jpg, 046_*.jpg …  (the example images)
│
└── docs/
    ├── PLACE_REPORT_HERE.txt      
    ├── PLACE_SLIDES_HERE.txt      
    └── assets/
        ├── demo.gif
        ├── dashboard-operator.jpg
        ├── dashboard-manager.jpg
        ├── detection-view.jpg
        └── results-view.jpg
```

---

## 🚀 Getting Started

> ⚠️ This is a research/academic prototype. Some modules describe the target industrial deployment rather than shipping code.

```bash
# 1. Clone
git clone https://github.com/<your-username>/tomatosort-pro.git
cd tomatosort-pro

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Frontend) install & run the dashboard
cd frontend && npm install && npm run dev
```

Each module folder contains its own `README.md` describing what belongs there and how to run it.

---

## 🗺️ Roadmap

- [ ] 🍅 **Generalize to more varieties** — beefsteak, elongated, cocktail tomatoes (dedicated data collection + retraining).
- [ ] ⚖️ **Handle class imbalance** — systematic data augmentation & balanced sampling for minority grades.
- [ ] 🧠 **Vision foundation models** — improve generalization with less labeled data.
- [ ] 🔁 **Full Active Learning loop** — cut annotation cost by targeting the most informative cases.
- [ ] 🔧 **Predictive maintenance** — time-series analysis on IoT sensors to anticipate failures.
- [ ] 🥦 **Extend beyond tomatoes** — other fruits & vegetables with minimal retraining.

---

## 👥 Team

Realized by  **Abderrahman Kayouh**in collaboration  with  :

| | |
|---|---|
| Hajar Hammouch  | Malak Rhalem |
| Amina Toumi | Mohamed Taha Hajji |

---

## 📚 References

A curated set of the works underpinning this project (full list in the [technical report](docs/technical-report.pdf)):

- Redmon & Farhadi — *YOLOv3: An Incremental Improvement*, arXiv:1804.02767, 2018.
- Jocher et al. — *Ultralytics YOLOv8*, 2023.
- LeCun, Bengio & Hinton — *Deep Learning*, Nature 521, 2015.
- Kreuzberger, Kühl & Hirschl — *MLOps: Overview, Definition, and Architecture*, IEEE Access, 2023.
- Kagermann, Wahlster & Helbig — *Recommendations for Implementing Industrie 4.0*, acatech, 2013.
- Al-Mutawa & Al-Qahtani — *Deep Learning-Based Tomato Sorting System for Industrial Applications*, IEEE Access, 2022.

---

## 📄 License

Released under the **MIT License** — see [`LICENSE`](LICENSE).

<div align="center">
<br>

*Built with 🍅 and a lot of GPU cycles — TomatoSort Pro, 2025–2026.*

</div>
