from .database import get_connection

class SongFormat:
    def __init__(self, id=None, song_id=None, format="MP3", file_path="", bitrate=0, size=0):
        self.id = id
        self.song_id = song_id
        self.format = format
        self.file_path = file_path
        self.bitrate = bitrate
        self.size = size

    @staticmethod
    def create(song_id, format, file_path="", bitrate=0, size=0):
        if format not in ['MP3', 'FLAC', 'WAV', 'AAC']:
            raise ValueError("Format must be one of: MP3, FLAC, WAV, AAC")
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO SongFormat (song_id, format, file_path, bitrate, size)
            VALUES (?, ?, ?, ?, ?)
        ''', (song_id, format, file_path, bitrate, size))
        format_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return SongFormat(format_id, song_id, format, file_path, bitrate, size)

    @staticmethod
    def get_by_song_id(song_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM SongFormat WHERE song_id = ?', (song_id,))
        rows = cursor.fetchall()
        conn.close()
        return [SongFormat(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]

    def update(self):
        if self.format not in ['MP3', 'FLAC', 'WAV', 'AAC']:
            raise ValueError("Format must be one of: MP3, FLAC, WAV, AAC")
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE SongFormat 
            SET format = ?, file_path = ?, bitrate = ?, size = ?
            WHERE id = ?
        ''', (self.format, self.file_path, self.bitrate, self.size, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM SongFormat WHERE id = ?', (self.id,))
        conn.commit()
        conn.close() 