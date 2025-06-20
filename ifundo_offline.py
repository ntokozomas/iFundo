# ========== IMPORTS ==========
import sounddevice as sd
import subprocess
import queue
import json
import os
import numpy as np
from vosk import Model, KaldiRecognizer
import pyttsx3

# ========== CONFIG ==========
MODEL_PATH = "/home/kumkanikazi/ifundo/vosk-model-small-en-us-0.15"
EMBEDDINGS_FILE = "knowledge_base/embeddings.json"
WAKE_WORD = "hello teacher"
EXIT_WORD = "exit"
BEEP_FILE = "wake_beeps.mp3"

# ========== VOSK ==========
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
q = queue.Queue()

# ========== TEXT TO SPEECH ==========
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ========== AUDIO CALLBACK ==========
def callback(indata, frames, time, status):
    if recognizer.AcceptWaveform(bytes(indata)):
        result = json.loads(recognizer.Result())
        if result.get("text"):
            q.put(result["text"])

# ========== PLAY BEEP ==========
def play_beep():
    if os.path.exists(f"sounds/{BEEP_FILE}"):
        subprocess.run(["mpg123", f"sounds/{BEEP_FILE}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ========== COSINE SIMILARITY ==========
def cosine_similarity(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

# ========== LOAD EMBEDDINGS ==========
def load_embeddings():
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    vectors = [np.array(d["embedding"], dtype=np.float32) for d in data]
    texts = [d["text"] for d in data]
    return vectors, texts

# ========== FIND BEST MATCH ==========
def find_best_match(user_text):
    vectors, texts = load_embeddings()

    # For simplicity, embed the user text using simple keyword match
    # (since we’re not generating a 1536 vector locally)
    best_score = 0
    best_text = "I don't know that yet."

    for vec, body in zip(vectors, texts):
        score = sum(1 for word in user_text.split() if word in body.lower())
        if score > best_score:
            best_score = score
            best_text = body

    return best_text

# ========== LISTEN LOOP ==========
def listen():
    import time

    print("🚀 Offline Ifundo is listening...")

    # Wait until valid input device is available
    while True:
        try:
            devices = sd.query_devices()
            default_input = sd.default.device[0]
            if default_input is not None and default_input >= 0:
                print(f"🎙️ Audio input device detected: {devices[default_input]['name']}")
                break
        except Exception as e:
            print(f"Waiting for audio device... ({str(e)})")
        time.sleep(1)

    # Once valid device exists, open stream
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):

        while True:
            text = q.get().lower().strip()
            if WAKE_WORD in text:
                print("🎤 Wake word detected.")
                play_beep()
                print("🧠 Listening for user query...")

                while True:
                    text = q.get().lower().strip()
                    print(f"🧠 User asked: {text}")
                    if EXIT_WORD in text:
                        print("👋 Exiting.")
                        speak("Goodbye")
                        return
                    else:
                        reply = find_best_match(text)
                        print(f"🗣️ {reply}")
                        speak(reply)
                        break


# ========== RUN ==========
if __name__ == "__main__":
    listen()

