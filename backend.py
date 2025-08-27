

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()

# Allow frontend on different port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Spatial Agent backend is running."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            # Placeholder: Assume data contains base64 audio string
            print("Received audio data")

            # Simulate response text and audio
            response_text = "Hello, I am Spatial Agent."
            dummy_audio_path = "assets/response_sample.wav"

            # Read dummy audio and send as base64
            with open(dummy_audio_path, "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

            await websocket.send_json({
                "text": response_text,
                "audio_base64": audio_base64
            })

    except WebSocketDisconnect:
        print("WebSocket connection closed.")