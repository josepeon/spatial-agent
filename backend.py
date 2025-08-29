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

import logging

# Load config
try:
    with open("config/secrets.json") as f:
        secrets = json.load(f)
    client = openai.OpenAI(api_key=secrets["openai_api_key"])
except Exception as e:
    raise RuntimeError(f"Failed to load API key: {e}")
use_openai = True
model = whisper.load_model("base")

message_history = [{"role": "system", "content": "You are a helpful AI avatar."}]

# Function to generate speech using OpenAI TTS
def generate_speech_openai(text, voice="nova", output_path="temp_audio/response.wav"):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
        )
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    except Exception as e:
        print(f"Speech generation failed: {e}")
        return None

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
            try:
                print("Transcribing...")
                result = model.transcribe(audio_path)
                user_text = result["text"]
                print("User said:", user_text)
            except Exception as e:
                print(f"Transcription failed: {e}")
                continue

            # Get response from GPT-4
            if use_openai:
                message_history.append({"role": "user", "content": user_text})
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=message_history
                    )
                    response_text = response.choices[0].message.content.strip()
                    message_history.append({"role": "assistant", "content": response_text})
                    message_history[:] = message_history[-10:]  # Limit history to last 10 messages
                except Exception as e:
                    print(f"GPT-4 response generation failed: {e}")
                    response_text = "Sorry, something went wrong."
            else:
                response_text = "(Local LLM not yet implemented)"

            # Generate TTS response from GPT-4 reply
            audio_path = generate_speech_openai(response_text)
            if audio_path:
                try:
                    with open(audio_path, "rb") as f:
                        audio_bytes = f.read()
                        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                except Exception as e:
                    print(f"Failed to read generated audio: {e}")
                    audio_base64 = ""
            else:
                audio_base64 = ""

            await websocket.send_json({
                "text": response_text,
                "audio_base64": audio_base64
            })

    except WebSocketDisconnect:
        print("WebSocket connection closed.")