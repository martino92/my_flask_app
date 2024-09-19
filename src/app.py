#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify, g
import requests
import sqlite3
from rq import Queue
from redis import Redis
import os

app = Flask(__name__)

# Configure Redis
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
try:
    redis_conn = Redis.from_url(redis_url)
    q = Queue(connection=redis_conn)
except:
    redis_conn = None
    q = None

# Database configuration
DATABASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'posts.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def fetch_and_store_posts():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    
    db = get_db()
    c = db.cursor()
    
    for post in posts:
        title_length = len(post['title'])
        body_length = len(post['body'])
        c.execute('''INSERT OR REPLACE INTO posts 
                     (id, title, body, title_length, body_length) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (post['id'], post['title'], post['body'], title_length, body_length))
    
    db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_posts', methods=['POST'])
def fetch_posts():
    if q is None:
        # If Redis is not available, run the task synchronously
        fetch_and_store_posts()
        return jsonify({'message': 'Posts have been fetched and stored.'}), 200
    else:
        job = q.enqueue(fetch_and_store_posts)
        return jsonify({'message': 'Posts are being fetched and stored in the background.'}), 202

@app.route('/api/stats')
def get_stats():
    db = get_db()
    c = db.cursor()
    
    c.execute('SELECT COUNT(*) FROM posts')
    total_posts = c.fetchone()[0]
    
    c.execute('SELECT AVG(title_length) FROM posts')
    avg_title_length = c.fetchone()[0]
    
    c.execute('SELECT AVG(body_length) FROM posts')
    avg_body_length = c.fetchone()[0]
    
    return jsonify({
        'total_posts': total_posts,
        'avg_title_length': round(avg_title_length, 2) if avg_title_length else 0,
        'avg_body_length': round(avg_body_length, 2) if avg_body_length else 0
    })

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)