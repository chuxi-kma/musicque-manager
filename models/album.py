from .database import get_connection

class Album:
    def __init__(self, id=None, name="", type="album", artist=""):
        self.id = id
        self.name = name
        self.type = type
        self.artist = artist

    @staticmethod
    def create(name, type, artist=""):
        if type not in ['album', 'mini_album']:
            raise ValueError("Type must be either 'album' or 'mini_album'")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Album (name, type, artist)
            VALUES (?, ?, ?)
        ''', (name, type, artist))
        album_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Album(album_id, name, type, artist)

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Album')
        rows = cursor.fetchall()
        conn.close()
        return [Album(row[0], row[1], row[2], row[3]) for row in rows]

    @staticmethod
    def get_by_id(album_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Album WHERE id = ?', (album_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Album(row[0], row[1], row[2], row[3])
        return None

    def update(self):
        if self.type not in ['album', 'mini_album']:
            raise ValueError("Type must be either 'album' or 'mini_album'")
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Album 
            SET name = ?, type = ?, artist = ?
            WHERE id = ?
        ''', (self.name, self.type, self.artist, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Album WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()

    def get_songs(self):
        from .song import Song
        return Song.get_by_album(self.id) 