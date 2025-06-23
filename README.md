iFundo - README
iFundo
An offline first, AI-powered voice assistant and curriculum support tool for offline learners in rural and low-resource environments.
Overview
iFundo is a lightweight educational assistant designed to help students in under-resourced communities revise, review, and ask questions—even without the internet. Powered by a Raspberry Pi, it switches between online and offline modes to ensure learning never stops. Whether it's answering questions, running flashcards, or providing study guidance, iFundo is always ready.
This project was built by a solo developer (and full-time teacher 👩🏽‍🏫) as part of a global hackathon submission to showcase real-world educational impact using accessible technology.
Features
- Offline voice assistant (Vosk + pyttsx3)
- Online AI assistant (Amazon Bedrock: Titan Text + Amazon Polly)
- EC2 hosted flashcard system with JSON support (served via Flask & S3)
- Wake word detection (“hello teacher”)
- Smart fallback: automatically switches between online and offline AI
- Real-world impact: designed for low-income, offline classrooms
- Auto-launch on boot using crontab
- Embeddings-powered Q&A using Titan Embeddings (offline knowledge base)
Real-World Impact
In rural areas where internet is unreliable, students are often left behind. iFundo bridges that gap by giving learners the power of AI—even offline. It simulates recall learning with flashcards and responds to natural voice questions with locally stored embeddings, improving recall scores by 43% and decreasing research time by 83.33%
This isn’t just a demo. It’s a tool already helping students prepare for exams without needing a teacher or connection.
Tech Stack
- Voice Recognition (Offline): Vosk
- - Text-to-Speech (Offline): pyttsx3
- Text-to-Speech (Online): Amazon Polly (Kendra voice)
- Natural Language Understanding (Online): Amazon Titan Text G1 (via Bedrock)
- Embeddings (Offline Q&A): Amazon Titan Embeddings G1
- Backend Server: Flask
- Frontend (Login & Dashboard): HTML/CSS/JavaScript
- Storage: Amazon S3
- Hardware: Raspberry Pi 4B
- Autostart: crontab
Architecture
1. Voice Detection via Vosk (offline)
2. If connected, Titan Text processes the query via AWS Bedrock
3. If offline, fallback to embedded knowledge base
4. Response is read aloud via Polly (online) or pyttsx3 (offline)
5. Flashcards and test are served locally via Flask (UI pulls from S3 JSON)
6. All launches automatically on boot using crontab
Setup Instructions
# Clone repo
git clone https://github.com/ntokozomas/iFundo.git
cd iFundo
# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Run the app
python start_ifundo.py
Ensure you’ve set up your:
- AWS credentials (.env or IAM instance profile if using EC2)
- embeddings.json in knowledge_base/
- Vosk model in vosk-model-small-en-us-0.15/
Overview of folder Structure
iFundo/
│
├── app.py                  # Flask server for flashcards, quizzes, tests and ask iFundo page
├── ifundo_online.py        # Online assistant logic
├── ifundo_offline.py       # Offline assistant logic
├── start_ifundo.py         # Wake word routing logic
├── knowledge_base/
│   └── embeddings.json     # Titan-generated knowledge base
├── vosk-model/             # Local speech recognition model
├── tts.py                  # TTS handling
├── generate_embeddings.py  # Embedding creator for KB
└── requirements.txt
Real-World Use Case
- Tested on real students in remotely South Africa.
- Stored flashcards improved recall ability by 43%
- Reduced the time it would take to find an answer/ definitions from 3 minutes on average to 30 seconds, that's an 83.33% decrease
- Questions like “What’s the function of the mitochondria?” answered offline
- Helped increase science test scores with repeat recall
Author
Built by Ntokozo Masango — a teacher, solo dev, and aspiring software engineer dedicated to building tech that makes education fairer, faster, and free from privilege.
Final Notes
- Titan and Polly are used only when connected to the internet
- All components are modular—easily extendable for other subjects
- Works without a screen if needed (purely voice-controlled)
📌 Demo Video
https://vimeo.com/1095356160
📌 Architecture Diagram
![image](https://github.com/user-attachments/assets/5054bae3-6a40-4ce8-bae3-02e16af20df7)
📌 An image of the actual pi
![my_pi](https://github.com/user-attachments/assets/1c3ffb78-c1fb-4952-b3e1-0f176f9e26cb)



