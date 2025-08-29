import os
import base64
import json
import whisper
import openai
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
with open("config/secrets.json") as f:
    secrets = json.load(f)
client = openai.OpenAI(api_key=secrets["openai_api_key"])
use_openai = True
model = whisper.load_model("base")

@app.get("/")
async def root():
    return {"message": "Spatial Agent backend is running."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            audio_base64 = data.get("audio_base64")
            if not audio_base64:
                continue

            # Save incoming audio
            audio_bytes = base64.b64decode(audio_base64)
            os.makedirs("temp_audio", exist_ok=True)
            audio_path = "temp_audio/input.wav"
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)

            # Transcribe with Whisper
            print("Transcribing...")
            result = model.transcribe(audio_path)
            user_text = result["text"]
            print("User said:", user_text)

            # Get response from GPT-4
            if use_openai:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI avatar."},
                        {"role": "user", "content": user_text}
                    ]
                )
                response_text = response.choices[0].message.content.strip()
            else:
                response_text = "(Local LLM not yet implemented)"

            # Return real text, still using static audio
            dummy_audio_path = "assets/response_sample.wav"
            with open(dummy_audio_path, "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

            await websocket.send_json({
                "text": response_text,
                "audio_base64": audio_base64
            })

    except WebSocketDisconnect:
        print("WebSocket connection closed.")