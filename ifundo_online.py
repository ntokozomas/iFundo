import os, json, boto3, queue, subprocess, sounddevice as sd
from vosk import Model, KaldiRecognizer
import threading

WAKE_WORD = "hello teacher"
SAMPLE_RATE = 16000
q = queue.Queue()
listening = True  # 🔒 Flag to control mic input during Polly playback

vosk_model = Model("/home/kumkanikazi/ifundo/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
polly = boto3.client("polly", region_name="us-east-1")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def play_beep(filename):
    subprocess.run(["mpg123", os.path.join("sounds", filename)])

def speak_online(text):
    global listening
    listening = False  # 🔇 Pause mic input
    play_beep("thinking_beep.mp3")

    # Use SSML to control speech speed
    ssml_text = f"<speak><prosody rate='145%'>{text}</prosody></speak>"

    response = polly.synthesize_speech(
        Text=ssml_text,
        OutputFormat="mp3",
        VoiceId="Kendra",
        TextType="ssml"
    )

    with open("response.mp3", "wb") as f:
        f.write(response["AudioStream"].read())

    subprocess.run(["mpg123", "response.mp3"])
    play_beep("done_beep.mp3")
    listening = True  # 🎤 Resume mic input


def query_titan(user_input):
    system_prompt = (
        "You are ifundo, a helpful AI-powered classroom assistant. "
        "You assist students with learning by explaining concepts clearly, using simple language, and providing examples. "
        "Always remain educational, positive, and guide students to focus on learning topics."
    )

    combined_prompt = f"{system_prompt}\n\nUser: {user_input}"

    body = json.dumps({
        "inputText": combined_prompt,
        "textGenerationConfig": {
            "maxTokenCount": 100,
            "temperature": 0.6,
            "topP": 0.8
        }
    })

    try:
        response = bedrock.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body=body,
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response["body"].read())
        return result["results"][0]["outputText"]
    except Exception as e:
        print("❌ Titan failed:", e)
        return "I'm not sure."

def callback(indata, frames, time_info, status):
    if listening:  # Only process mic input when not speaking
        if recognizer.AcceptWaveform(bytes(indata)):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip().lower()
            if text:
                q.put(text)

def listen():
    import time

    print("🚀 Ifundo Online is listening...")

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
            text = q.get()
            if WAKE_WORD in text:
                print("🎤 Wake word detected.")
                play_beep("wake_beeps.mp3")
                speak_online("Hello, how can I you?")
                
                user_input = q.get()
                print("🧠 User asked:", user_input)

                if "exit" in user_input:
                    speak_online("Okay, thank you, goodbye.")
                    break  # 🛑 Shut down the loop

                reply = query_titan(user_input)
                speak_online(reply)

listen()

























