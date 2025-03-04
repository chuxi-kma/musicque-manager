from models.database import get_connection

def add_song(name, album_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Song (name, album_id) VALUES (?, ?)', (name, album_id))
    conn.commit()
    conn.close()

def search_songs_by_name(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Song WHERE name LIKE ?', (f'%{keyword}%',))
    songs = cursor.fetchall()
    conn.close()
    return songs