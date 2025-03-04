import sqlite3
import os

def get_connection():
    return sqlite3.connect('music_manager.db')

def reset_database():
    # Xóa file database cũ nếu tồn tại
    if os.path.exists('music_manager.db'):
        os.remove('music_manager.db')
    # Tạo database mới
    setup_database()

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Bảng Album
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Album (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('album', 'mini_album')),
        artist TEXT
    )''')
    
    # Bảng Song
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Song (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT,
        duration INTEGER,
        album_id INTEGER,
        FOREIGN KEY (album_id) REFERENCES Album(id) ON DELETE CASCADE
    )''')
    
    # Bảng SongFormat
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SongFormat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_id INTEGER,
        format TEXT NOT NULL CHECK(format IN ('MP3', 'FLAC', 'WAV', 'AAC')),
        file_path TEXT,
        bitrate INTEGER,
        size INTEGER,
        FOREIGN KEY (song_id) REFERENCES Song(id) ON DELETE CASCADE
    )''')
    
    conn.commit()
    conn.close()