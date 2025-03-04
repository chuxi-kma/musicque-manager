from models.database import get_connection

def add_album(name, album_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Album (name, type) VALUES (?, ?)', (name, album_type))
    conn.commit()
    conn.close()