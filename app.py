from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import boto3
import json
from users import USERS

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 🔒 Needed for session management

# Bedrock client 
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# S3 client 
s3 = boto3.client("s3", region_name="us-east-1")  
BUCKET_NAME = "ifundo-past-paper1"  

# Root route shows welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = USERS.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = USERS.get(session['username'])
    return render_template('index.html', user=user)

@app.route('/askifundo')
def askifundo():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = USERS.get(session['username'])
    return render_template('askifundo.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/ifundo', methods=['POST'])
def ifundo_response():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input.strip():
        return jsonify({"response": "Please ask something meaningful."})

    system_prompt = (
        "You are iFundo, an educational AI assistant. Answer like a friendly tutor speaking directly to the student. "
        "Never prefix your responses with 'Bot:', 'iFundo:', or similar labels. "
        "Simply give your answers naturally and directly, without repeating the user's question."
    )

    combined_prompt = f"{system_prompt}\n\nUser: {user_input}"

    body = json.dumps({
        "inputText": combined_prompt,
        "textGenerationConfig": {
            "maxTokenCount": 150,
            "temperature": 0.7,
            "topP": 0.9
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
        answer = result["results"][0]["outputText"].lstrip("Bot: ").strip()

        return jsonify({"response": answer})
    except Exception as e:
        print("❌ Titan error:", e)
        return jsonify({"response": "Oops! Something went wrong."})

#  Past Papers route
@app.route('/past-papers')
def past_papers():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        files = []
        for obj in response.get("Contents", []):
            key = obj["Key"]
            if key.endswith('.pdf'):
                files.append(key)

        return render_template('past_papers.html', files=files, bucket_name=BUCKET_NAME)

    except Exception as e:
        print("❌ S3 error:", e)
        return render_template('past_papers.html', files=[], bucket_name=BUCKET_NAME, error="Could not load past papers.")

@app.route('/flashcards')
def flashcards():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('flashcards.html', user=USERS.get(session['username']))

if __name__ == '__main__':
    app.run(debug=True)
