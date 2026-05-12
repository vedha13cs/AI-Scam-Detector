from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database Connection
conn = sqlite3.connect('scam.db', check_same_thread=False)
cursor = conn.cursor()

# Create Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    result TEXT,
    score INTEGER
)
''')

conn.commit()

# Scam Keywords
scam_keywords = [
    'urgent',
    'click here',
    'bank account',
    'otp',
    'lottery',
    'winner',
    'claim now',
    'free money',
    'verify account',
    'password'
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_message():

    message = request.form['message'].lower()

    score = 0
    found_keywords = []

    for word in scam_keywords:
        if word in message:
            score += 10
            found_keywords.append(word)

    if score >= 30:
        result = 'SCAM ALERT ⚠️'
    else:
        result = 'SAFE MESSAGE ✅'

    # Save to Database
    cursor.execute(
        'INSERT INTO reports(message, result, score) VALUES (?, ?, ?)',
        (message, result, score)
    )

    conn.commit()

    return render_template(
        'result.html',
        result=result,
        score=score,
        keywords=found_keywords
    )


if __name__ == '__main__':
    app.run(debug=True)
