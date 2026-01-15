from flask import Flask, request, send_from_directory, jsonify
import sqlite3
import os

# Setting up the server to recognize the local folder as the home for assets
app = Flask(__name__, static_folder='.', static_url_path='')

# Database setup for the Newsletter section in the HTML
def init_db():
    conn = sqlite3.connect('blackmon_data.db')
    conn.execute('CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT)')
    conn.commit()
    conn.close()

init_db()

# ROUTE 1: Serves the HTML file
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# ROUTE 2: Dynamic Asset Handler 
# This matches the <img src="/assests/..."> paths HTML
@app.route('/assests/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assests', filename)

# ROUTE 3: Newsletter Logic
@app.route('/join-newsletter', methods=['POST'])
def join_newsletter():
    data = request.json
    email = data.get('email')
    if email:
        conn = sqlite3.connect('blackmon_data.db')
        conn.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Email saved to database"}), 200
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
