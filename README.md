<div align="center">

# 🦺 Site Safety Watch

**Real-time AI-powered PPE compliance monitoring for construction sites**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-7-3178C6?style=flat&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Pose-FF4500?style=flat&logo=ultralytics&logoColor=white)](https://ultralytics.com)
[![Gemini](https://img.shields.io/badge/Gemini-Vision-8E75B2?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🏆 **1st Runners-Up — Hackathon 2026**

### 🌐 [Try the Live Demo →](https://site-safety-ppe.vercel.app/)
*Scan a QR, take a photo, get instant AI PPE analysis — no setup needed*

</div>

---

## 🔍 What is Site Safety Watch?

Construction sites are dangerous. Workers without proper PPE — hard hats and high-visibility vests — are at serious risk of injury. Manual supervision is inconsistent and expensive.

**Site Safety Watch** is a full-stack AI safety system built in two complementary modes to cover every real-world deployment scenario:

- 🖥️ **Monitoring Mode** — a high-performance local station that watches a live camera feed 24/7, running YOLOv8-Pose on every frame to flag violations in real time
- 📱 **Inspection Mode** — a deployed PWA any inspector can open on their phone, snap a photo, and get instant Gemini Vision analysis with per-worker bounding boxes and a compliance report

---

## ⚡ Two-Mode Architecture

| | 🖥️ Monitoring Mode *(this repo)* | 📱 Inspection Mode *([site_safety_ppe](https://github.com/yuvadepcodes/site_safety_ppe))* |
|---|---|---|
| **Input** | Live CCTV / phone camera stream | Single photo from any device |
| **AI Engine** | YOLOv8-Pose (local, real-time) | Gemini Vision API (cloud) |
| **Output** | Annotated live video feed | Per-worker bounding boxes + full risk report |
| **Deployment** | On-site machine (max FPS, zero cloud latency) | Vercel + PWA — scan a QR, works instantly |
| **Best for** | Dedicated site monitoring station | Field safety inspector, remote audit, demo |
| **Offline?** | Yes — runs fully local | PWA-ready, works offline after first load |

Both modes were presented at the hackathon. Judges scanned a QR code to try the live inspection on their own phones — while the monitoring station ran in real time on the demo laptop.

---

## ✨ Features

### 🖥️ Monitoring Mode (this repo)
| Feature | Details |
|---|---|
| **Real-time detection** | Threaded camera stream eliminates network lag; MJPEG streamed over FastAPI |
| **Pose-aware PPE check** | Uses skeleton keypoints to crop anatomically correct head/torso regions — not just the bounding box |
| **Multi-person tracking** | Detects and labels every worker in frame simultaneously |
| **Live compliance score** | Aggregated PPE compliance rate on the dashboard |
| **Risk signal feed** | Live alerts panel with severity levels (High / Medium / Low) |
| **Fullscreen camera mode** | One-click fullscreen for the live feed |
| **Daily report export** | Print-ready daily safety report from the browser |

### 📱 Inspection Mode ([live app](https://site-safety-ppe.vercel.app/))
| Feature | Details |
|---|---|
| **Gemini Vision AI** | Structured JSON output — per-worker helmet status, vest status, bounding boxes, hazard notes |
| **Interactive overlay** | Clickable bounding boxes on the photo for each detected worker |
| **PWA installable** | Add to home screen on any phone, works like a native app |
| **Daily risk report** | Log multiple inspections, build a report, export as PDF |
| **Offline capable** | Works after first load, syncs when back online |
| **Sample photos** | Built-in construction photos for instant one-click demo |

---

## 🏗️ System Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                     SITE SAFETY WATCH SYSTEM                      │
└───────────────────────────────────────────────────────────────────┘
                                  │
          ┌───────────────────────┴───────────────────────┐
          │                                               │
          ▼                                               ▼
┌─────────────────────┐                       ┌──────────────────────┐
│  🖥️ MONITORING MODE  │                       │  📱 INSPECTION MODE   │
│  (site-safety-watch) │                       │  (site_safety_ppe)   │
└─────────────────────┘                       └──────────────────────┘
          │                                               │
   Phone cam (Wi-Fi)                           Photo upload / camera
          │                                               │
   FastAPI backend                             Vercel serverless fn
          │                                               │
   YOLOv8-Pose (local)                         Gemini Vision API
          │                                               │
   Annotated MJPEG feed                        Structured JSON
          │                                               │
   React dashboard                             React PWA + overlay
```

---

## 🛠️ Tech Stack

**Monitoring Mode (this repo)**
- [Python 3.10+](https://python.org) · [FastAPI](https://fastapi.tiangolo.com) · [Uvicorn](https://www.uvicorn.org)
- [Ultralytics YOLOv8-Pose](https://ultralytics.com) · [OpenCV](https://opencv.org)
- [React 19](https://react.dev) · [TypeScript 7](https://typescriptlang.org) · [Tailwind CSS 4](https://tailwindcss.com) · [Vite 8](https://vitejs.dev)

**Inspection Mode ([site_safety_ppe](https://github.com/yuvadepcodes/site_safety_ppe))**
- [Gemini Vision API](https://ai.google.dev) (`gemini-flash` with structured output schema)
- [Vercel](https://vercel.com) serverless functions · [React 19](https://react.dev) · [TypeScript](https://typescriptlang.org)
- PWA (installable, offline-capable) · PDF report generation

---

## 🚀 Getting Started — Monitoring Mode

### Prerequisites

- Python 3.10+
- Node.js 18+
- An Android phone with the **[IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam)** app installed
- Phone and laptop on the **same Wi-Fi network**

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

> **For the Inspection Mode (deployed PWA):** visit [site-safety-ppe.vercel.app](https://site-safety-ppe.vercel.app/) — no setup needed. See the [site_safety_ppe repo](https://github.com/yuvadepcodes/site_safety_ppe) for self-hosting instructions.

---

## 📡 How the PPE Detection Works

### Monitoring Mode — YOLOv8-Pose (local)

For each detected person, the model extracts 17 body keypoints. We then:

1. **Hard Hat check** — Crop a region above the nose keypoint. Run HSV color masking for yellow/orange (`[20–35°]`) and white (`high V, low S`) helmet colors.
2. **Hi-Vis Vest check** — Crop the torso between the shoulder keypoints. Run HSV masking for the characteristic orange/yellow reflective vest range (`[15–38°]`).
3. **Status overlay** — 🟢 green box = compliant, 🔴 red box = violation, with a live badge: `HELMET: OK | VEST: OK`.

### Inspection Mode — Gemini Vision (cloud)

A single photo is sent to the Gemini Vision API with a structured output schema. The model returns:
- Per-worker `helmetStatus` and `vestStatus` (`worn` / `missing` / `improper` / `not_visible`)
- YOLO-style bounding boxes `[ymin, xmin, ymax, xmax]` for each worker, their helmet, and their vest
- Overall `safetyScore` (0–100), `overallRiskLevel`, site hazards, and immediate action recommendations

Server-side validation enforces compliance rules — if the model marks a worker missing a helmet but `isCompliant: true`, the API corrects it before sending the response.

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

## 🔗 Related

- 📱 **Inspection Mode (Live PWA):** [site-safety-ppe.vercel.app](https://site-safety-ppe.vercel.app/)
- 💻 **Inspection Mode (Repo):** [github.com/yuvadepcodes/site_safety_ppe](https://github.com/yuvadepcodes/site_safety_ppe)

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
