from gtts import gTTS
from playsound import playsound

# Step 1: Create the mp3
tts = gTTS("Ifundo is finally speaking.", lang='en')
tts.save("ifundo_test.mp3")

print("✅ MP3 saved")

# Step 2: Play it
print("🔊 Trying to play sound...")
playsound("ifundo_test.mp3")
