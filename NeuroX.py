from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}
messages = []

# Load users from file
if os.path.exists('users.json'):
    with open('users.json', 'r') as f:
        users = json.load(f)
else:
    with open('users.json', 'w') as f:
        json.dump({}, f)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if user in users and users[user] == password:
            session['user'] = user
            return redirect('/chat')
        return "Login failed!"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        users[user] = password
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return redirect('/login')
    return render_template('signup.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/login')
    return render_template('chat.html', user=session['user'])

@app.route('/send', methods=['POST'])
def send_message():
    if 'user' in session:
        msg = request.form['message']
        messages.append({'user': session['user'], 'msg': msg})
        return '', 204
    return 'Unauthorized', 401

@app.route('/messages')
def get_messages():
    return jsonify(messages)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
