from gtts import gTTS
import subprocess
import uuid
import os

def speak(text):
    print("🗣️ Speaking:", text)
    filename = f"/tmp/{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    try:
        subprocess.run(["mpg123", filename], check=True)
    except Exception as e:
        print("💥 Failed to play audio:", e)
    finally:
        os.remove(filename)


