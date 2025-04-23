from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, requests

load_dotenv()

app = FastAPI()

# CORS kalau kamu mau akses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan domain frontend kalau perlu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-voice/")
async def upload_voice(
    file: UploadFile = File(...),
    name: str = Form("User Voice"),
    description: str = Form("Voice uploaded via API")
):
    api_key = os.getenv("ELEVEN_API_KEY")
    headers = {"xi-api-key": api_key}

    files = {
        "files": (file.filename, await file.read(), file.content_type)
    }

    data = {
        "name": name,
        "description": description,
        "labels": '{"project":"voice-cloning"}'
    }

    response = requests.post(
        "https://api.elevenlabs.io/v1/voices/add",
        headers=headers,
        files=files,
        data=data
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": response.text,
            "status": response.status_code
        }
