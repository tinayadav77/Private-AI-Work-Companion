from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from faster_whisper import WhisperModel
import tempfile
import os
import sys

# Allow Python to access project-level services
sys.path.append(os.path.abspath(".."))

from services.intent_service import detect_intent
from services.task_service import add_task, get_tasks
from services.semantic_search import search_documents
from services.activity_service import get_daily_activity

app = FastAPI(title="Private AI Work Companion")


# Load local speech-to-text model
model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)


@app.post("/voice")
async def transcribe_voice(file: UploadFile = File(...)):

    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".webm"
    ) as temp:

        audio_path = temp.name
        temp.write(await file.read())

    try:
        # Transcribe audio locally
        segments, info = model.transcribe(audio_path)

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        # Determine what the user intended
        intent = detect_intent(text)

        search_results = []

        if intent == "task":
            add_task(text)

        elif intent == "search":
            search_results = search_documents(text)

        return {
            "text": text,
            "intent": intent,
            "language": info.language,
            "results": search_results
}

    finally:
        # Delete temporary audio
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.get("/tasks")
async def tasks():
    return {
        "tasks": get_tasks()
    }

@app.get("/search")
async def search(q: str):
    return {
        "results": search_documents(q)
    }

@app.get("/activity")
async def activity():
    return {
        "activity": get_daily_activity()
    }

# Serve frontend
app.mount(
    "/",
    StaticFiles(directory="../frontend", html=True),
    name="frontend"
)