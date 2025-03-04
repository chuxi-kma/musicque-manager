from .database import get_connection

class Song:
    def __init__(self, id=None, title="", artist="", duration=0, album_id=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.duration = duration
        self.album_id = album_id

    @staticmethod
    def create(title, artist, duration, album_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Song (title, artist, duration, album_id)
            VALUES (?, ?, ?, ?)
        ''', (title, artist, duration, album_id))
        song_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Song(song_id, title, artist, duration, album_id)

    @staticmethod
    def get_by_id(song_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Song WHERE id = ?', (song_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Song(row[0], row[1], row[2], row[3], row[4])
        return None

    @staticmethod
    def search_by_title(title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Song WHERE title LIKE ?', (f'%{title}%',))
        rows = cursor.fetchall()
        conn.close()
        return [Song(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    @staticmethod
    def get_by_album(album_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Song WHERE album_id = ?', (album_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Song(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    def update(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Song 
            SET title = ?, artist = ?, duration = ?, album_id = ?
            WHERE id = ?
        ''', (self.title, self.artist, self.duration, self.album_id, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Song WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()

    def get_formats(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM SongFormat WHERE song_id = ?', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return rows  # Trả về danh sách các định dạng 