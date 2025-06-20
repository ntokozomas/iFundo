import pyaudio
import vosk
import json

model = vosk.Model("vosk_model/vosk-model-small-en-us-0.15")

p  = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000)

stream.start_stream()

rec = vosk.KaldiRecognizer(model,16000)

print("Listening... Press Ctrl+C to stop.")
try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if result.get("text"):
                print("You said:", result["text"])
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    stream.stop_stream()
    stream.close() 
    p.terminate()                   