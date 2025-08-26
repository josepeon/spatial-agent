# Spatial Agent

**Spatial Agent** is a real-time, browser-based AI system that enables natural, face-to-face interaction with a lifelike 3D conversational avatar. It captures webcam and microphone input to track the user’s facial expressions and speech, processes those inputs through a series of AI components, and responds with intelligent dialogue, synchronized voice output, and expressive visual feedback. The system integrates multiple AI modalities, including speech-to-text (Whisper), large language model response generation (initially using OpenAI GPT-4, with later support for local open-weight models via Ollama or vLLM), emotional tone classification from either facial or textual input, and text-to-speech synthesis (via TorToiSe, Bark, or a fallback TTS system). On the frontend, the avatar is rendered and animated in real time using Three.js, with blendshape-based expression control and viseme-based lip sync to reflect the agent’s speech and tone. All communication between browser and backend occurs over a WebSocket API for low-latency, full-duplex interaction. The backend is structured as a single consolidated `backend.py` file running a FastAPI server that manages inference orchestration across all components. The frontend is similarly streamlined into a single `main.js` file, handling webcam and mic setup, expression tracking via MediaPipe, WebGL rendering, and UI management. The entire system is designed with a minimal file structure to reduce project bulk, improve maintainability, and prioritize functional clarity over unnecessary modularity. Spatial Agent serves as a high-level AI engineering project, demonstrating full-stack, multi-modal AI system design, and offers direct applications in immersive retail, virtual assistance, or embodied digital interfaces.

---

## Features

- Real-time face and voice input capture in the browser
- Emotion-aware conversational response using GPT-4 or local LLM
- Expressive 3D avatar animation with lip sync and facial expressions
- Whisper-based transcription of user speech
- Flexible TTS backend (TorToiSe, Bark, ElevenLabs, etc.)
- Local model routing (OpenAI API fallback to Ollama or vLLM)
- Clean and minimal file architecture
- WebSocket-based full-duplex communication

---

## System Architecture

### Frontend (Browser)

- **Webcam and Microphone**: Captured via WebRTC
- **Expression Detection**: MediaPipe FaceMesh or TensorFlow.js
- **Avatar Rendering**: Three.js with GLTF rigged avatar
- **UI**: index.html + minimal controls
- **Communication**: WebSocket (socket.io or native) – persistent connection used for full-duplex messaging between client and server

### Backend (Python)

- **Framework**: FastAPI with WebSocket support
- **Speech-to-Text**: Whisper (or Whisper.cpp)
- **LLM Response Generation**: GPT-4 (OpenAI) or local model (Ollama, vLLM)
- **Emotion Classification**: Text-based or audio-based emotion tagging
- **Text-to-Speech**: TorToiSe, Bark, or fallback TTS services such as ElevenLabs for lower latency
- **Expression Mapping**: Converts tone and speech to avatar animation controls

---

## Project Structure

spatial_agent/
├── backend.py             # Unified backend logic (API, STT, LLM, TTS, emotion)
├── frontend/
│   ├── index.html         # UI layout
│   ├── main.js            # Webcam, audio, tracking, animation logic
│   └── style.css          # Optional styles
├── public/
│   └── avatar.glb         # Rigged 3D avatar with blendshapes
├── config/
│   └── settings.json      # API keys, model config, toggles
├── assets/
│   └── demo.mp4           # Showcase video (optional)
├── requirements.txt       # Python dependencies
└── README.md

---

## Technology Stack

### Backend

- Python 3.10+
- FastAPI
- Uvicorn
- OpenAI API or local model via Ollama/vLLM
- Whisper / whisper.cpp
- TorToiSe, Bark, or ElevenLabs for TTS
- pydub, ffmpeg-python, torchaudio
- WebSocket (async)

### Frontend

- HTML / JavaScript
- MediaPipe or TensorFlow.js (FaceMesh)
- Three.js (WebGL 3D rendering)
- WebRTC (audio/video input)
- Optional React for expansion

---

## Development Timeline (Suggested)

| Week | Deliverables |
|------|--------------|
| 1 | Webcam + mic + basic UI |
| 2 | FastAPI + Whisper + GPT-4 round trip |
| 3 | Avatar load + expression + lip sync animation |
| 4 | Full WebSocket loop: user speaks, agent talks back |
| 5 | Switch to local LLM via Ollama/vLLM |
| 6 | Expression tuning, async error handling |
| 7 | UI polish, UX review |
| 8 | Demo export, GitHub cleanup, deployment prep |

---

## Setup Notes

- Install Python 3.10+ and Node.js
- Set up `requirements.txt` in a virtual environment
- Download avatar model to `public/avatar.glb`
- Replace API keys in `config/settings.json`
- Start with GPT-4, later switch to a local LLM backend
- Test frontend locally via `http-server` or any static server
- Run backend with `uvicorn backend:app --reload`

---

## Quickstart

```bash
conda create -n spatial_agent_env python=3.10 -y
conda activate spatial_agent_env
pip install -r requirements.txt
uvicorn backend:app --reload
```

---

## Future Work

- Agent memory with vector DB
- Multiplayer AI agents in 3D space
- Stylized avatars
- Multi-modal feedback (gesture, mood light, soundscape)
- Voice-based authentication
- OH platform integration

---

## License

Proprietary. All rights reserved. For research and portfolio use only unless otherwise licensed.
