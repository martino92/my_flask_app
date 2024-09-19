#!/usr/bin/env python3

from flask import Flask, request, render_template
import requests
import sqlite3
from rq import Queue
from redis import Redis
import os

app = Flask(__name__)

# Configure Redis
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_conn = Redis.from_url(redis_url)
q = Queue(connection=redis_conn)

def init_db():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, title TEXT, body TEXT, 
                  title_length INTEGER, body_length INTEGER)''')
    conn.commit()
    conn.close()

def fetch_and_store_posts():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    
    for post in posts:
        title_length = len(post['title'])
        body_length = len(post['body'])
        c.execute('''INSERT OR REPLACE INTO posts 
                     (id, title, body, title_length, body_length) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (post['id'], post['title'], post['body'], title_length, body_length))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_posts', methods=['POST'])
def fetch_posts():
    job = q.enqueue(fetch_and_store_posts)
    return 'Posts are being fetched and stored in the background.'

@app.route('/api/stats')
def get_stats():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM posts')
    total_posts = c.fetchone()[0]
    
    c.execute('SELECT AVG(title_length) FROM posts')
    avg_title_length = c.fetchone()[0]
    
    c.execute('SELECT AVG(body_length) FROM posts')
    avg_body_length = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_posts': total_posts,
        'avg_title_length': round(avg_title_length, 2) if avg_title_length else 0,
        'avg_body_length': round(avg_body_length, 2) if avg_body_length else 0
    }

if __name__ == '__main__':
    init_db()
    app.run(debug=True)