import sqlite3
import config_chatgpt as config
from datetime import datetime

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(config.DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            title TEXT,
            video_path TEXT,
            youtube_id TEXT,
            uploaded_at TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    """)
    
    conn.commit()
    conn.close()

def add_video(topic, title, video_path):
    """Add video to database"""
    conn = sqlite3.connect(config.DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO videos (topic, title, video_path, status)
        VALUES (?, ?, ?, 'pending')
    """, (topic, title, video_path))
    
    video_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return video_id

def update_video_status(video_id, status, youtube_id=None):
    """Update video status"""
    conn = sqlite3.connect(config.DB_FILE)
    cursor = conn.cursor()
    
    if youtube_id:
        cursor.execute("""
            UPDATE videos 
            SET status = ?, youtube_id = ?, uploaded_at = ?
            WHERE id = ?
        """, (status, youtube_id, datetime.now(), video_id))
    else:
        cursor.execute("""
            UPDATE videos 
            SET status = ?
            WHERE id = ?
        """, (status, video_id))
    
    conn.commit()
    conn.close()

def get_pending_videos():
    """Get pending videos"""
    conn = sqlite3.connect(config.DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, topic, title, video_path
        FROM videos
        WHERE status = 'pending'
        ORDER BY id ASC
    """)
    
    videos = cursor.fetchall()
    conn.close()
    
    return videos

def get_used_topics():
    """Get list of used topics"""
    conn = sqlite3.connect(config.DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT topic FROM videos")
    topics = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return topics
