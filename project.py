from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

# We set static_folder to '.' so Flask looks in your main project folder for style.css and script.js
app = Flask(__name__, static_folder='.', static_url_path='')

DB_NAME = 'tutoring.db'

def init_db():
    """Creates the database and table for leads if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Table to store email signups from the footer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database immediately
init_db()

# 1. MAIN ROUTE: Serves your teammates' HTML file
@app.route('/')
def index():
    # Change 'index.html' to whatever your teammate named the file
    return send_from_directory('.', 'index.html')

# 2. ASSET ROUTE: Fixes the image paths (/assests/...)
@app.route('/assests/<path:filename>')
def serve_assets(filename):
    # This ensures images in the /assests/ folder load correctly
    return send_from_directory('assests', filename)

# 3. DATA ROUTE: Captures the 'Join Our Newsletter' email
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        try:
            conn = sqlite3.connect(DB_NAME)
            conn.execute('INSERT INTO leads (email) VALUES (?)', (email,))
            conn.commit()
            conn.close()
            # Professional response after saving to DB
            return "<h2>Registration Successful!</h2><p>We will contact you soon.</p><a href='/'>Return to Home</a>"
        except Exception as e:
            return f"Database Error: {str(e)}", 500
    return "Error: Email is required.", 400

if __name__ == '__main__':
    # Running on port 5000 - the standard for web development
    print("Blackmon Tutoring Server Starting...")
    app.run(debug=True, port=5000)
