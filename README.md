<div align="center">

# 🛡️ SentryAI

**Real-time AI-powered PPE compliance monitoring for construction sites**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-7-3178C6?style=flat&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Pose-FF4500?style=flat&logo=ultralytics&logoColor=white)](https://ultralytics.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🏆 **1st Runners-Up — Hackathon 2026**

</div>

---

## 🔍 What is SentryAI?

Construction sites are dangerous. Workers without proper PPE — hard hats and high-visibility vests — are at serious risk of injury. Manual supervision is inconsistent and expensive.

**SentryAI** solves this with a live AI detection pipeline that:

- 📡 Streams video from a phone camera over Wi-Fi
- 🤖 Runs **YOLOv8-Pose** to detect workers and extract 17 body keypoints per person
- 🦺 Checks each detected worker for a **hard hat** and **hi-vis vest** using HSV color analysis on anatomically-precise regions (head ROI from nose keypoint, torso ROI from shoulder keypoints)
- 🟢 / 🔴 Labels every worker **COMPLIANT** or **VIOLATION** in real time
- 📊 Streams the annotated feed to a **React dashboard** that shows live stats, risk signals, compliance scores, and a daily PDF-ready report

---

## ✨ Features

| Feature | Details |
|---|---|
| **Real-time detection** | Threaded camera stream eliminates network lag; MJPEG streamed over FastAPI |
| **Pose-aware PPE check** | Uses skeleton keypoints to crop anatomically correct head/torso regions — not just the bounding box |
| **Multi-person tracking** | Detects and labels every worker in frame simultaneously |
| **Live compliance score** | Aggregated PPE compliance rate displayed on the dashboard |
| **Risk signal feed** | Live alerts panel with severity levels (High / Medium / Low) |
| **Fullscreen camera mode** | One-click fullscreen for the live feed |
| **Daily report export** | Print-ready daily safety report from the browser |
| **Offline fallback** | Dashboard gracefully handles backend being offline |

---

## 🏗️ Architecture

```
┌─────────────────────┐        MJPEG stream        ┌──────────────────────────┐
│   📱 Phone Camera   │ ──── Wi-Fi / IP Webcam ──► │   🐍 FastAPI Backend      │
│  (IP Webcam app)    │                             │                          │
└─────────────────────┘                             │  ┌────────────────────┐  │
                                                    │  │  CameraStream      │  │
                                                    │  │  (Threaded reader) │  │
                                                    │  └────────┬───────────┘  │
                                                    │           │              │
                                                    │  ┌────────▼───────────┐  │
                                                    │  │  YOLOv8-Pose       │  │
                                                    │  │  Inference         │  │
                                                    │  └────────┬───────────┘  │
                                                    │           │              │
                                                    │  ┌────────▼───────────┐  │
                                                    │  │  HSV PPE Checker   │  │
                                                    │  │  (Helmet + Vest)   │  │
                                                    │  └────────┬───────────┘  │
                                                    │           │              │
                                                    │   /video_feed (MJPEG)    │
                                                    └───────────┼──────────────┘
                                                                │
                                                    ┌───────────▼──────────────┐
                                                    │   ⚛️  React Dashboard     │
                                                    │   (Vite + TypeScript +   │
                                                    │    Tailwind CSS)         │
                                                    └──────────────────────────┘
```

---

## 🛠️ Tech Stack

**Backend**
- [Python 3.10+](https://python.org)
- [FastAPI](https://fastapi.tiangolo.com) — async REST + MJPEG streaming
- [Ultralytics YOLOv8-Pose](https://ultralytics.com) — real-time pose estimation
- [OpenCV](https://opencv.org) — video capture, HSV color analysis, frame annotation
- [Uvicorn](https://www.uvicorn.org) — ASGI server

**Frontend**
- [React 19](https://react.dev) + [TypeScript 7](https://typescriptlang.org)
- [Vite 8](https://vitejs.dev) — lightning-fast dev + build
- [Tailwind CSS 4](https://tailwindcss.com) — utility-first styling
- Custom glass-morphism dark dashboard UI

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- An Android phone with the **[IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam)** app installed
- Phone and laptop on the **same Wi-Fi network**

---

### 1. Clone the repo

```bash
git clone https://github.com/yuvadepcodes/site-safety-watch.git
cd site-safety-watch
```

### 2. Backend setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# The YOLOv8-Pose weights download automatically on first run
```

Configure your environment:

```bash
cp .env.example .env
# Edit .env and set VIDEO_SOURCE to your phone's IP Webcam stream URL
# e.g. VIDEO_SOURCE=http://192.168.1.42:8080/video
```

Start the backend:

```bash
python main.py
# API running at http://127.0.0.1:8000
# Live annotated feed at http://127.0.0.1:8000/video_feed
```

### 3. Frontend setup

```bash
# In a new terminal
npm install
npm run dev
# Dashboard running at http://localhost:5173
```

---

## 📡 How the PPE Detection Works

For each detected person, the model extracts 17 body keypoints. We then:

1. **Hard Hat check** — Crop a region above the nose keypoint. Run HSV color masking for yellow/orange (`[20–35°]`) and white (`high V, low S`) helmet colors. Flag compliant if pixel count exceeds threshold.

2. **Hi-Vis Vest check** — Crop the torso region between the shoulder keypoints. Run HSV masking for the characteristic orange/yellow reflective vest range (`[15–38°]`). Flag compliant if pixel count exceeds threshold.

3. **Status overlay** — Draw a colored bounding box (🟢 green = compliant, 🔴 red = violation) with a status badge: `HELMET: OK | VEST: OK` or the specific missing items.

---

## 📂 Project Structure

```
site-safety-watch/
├── main.py               # FastAPI backend — camera stream + YOLOv8 inference
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── src/
│   ├── App.tsx           # Main React dashboard component
│   ├── index.css         # Global styles + glass-morphism UI
│   └── main.tsx          # React entry point
├── public/
│   └── favicon.svg
├── package.json
└── vite.config.ts
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ for safer construction sites &nbsp;•&nbsp; 🏆 Hackathon 2026 — 1st Runners-Up

</div>
