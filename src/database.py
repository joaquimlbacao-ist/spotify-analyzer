import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'spotify-analyzer.db'
)

def init_db():
    """Initialize database schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Streams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT NOT NULL,
            track_name TEXT NOT NULL,
            album TEXT NOT NULL,
            ms_played INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    ''')
    
    # Indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_artist ON streams(artist)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_album ON streams(album)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON streams(timestamp)')
    
    # Album groupings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS album_groupings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canonical_album TEXT NOT NULL,
            artist TEXT NOT NULL,
            constituents TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(canonical_album, artist)
        )
    ''')
    
    conn.commit()
    conn.close()

# ===== STREAMS =====

def clear_streams():
    """Delete all streams"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM streams')
    conn.commit()
    conn.close()

def insert_stream(artist, track_name, album, ms_played, timestamp):
    """Insert single stream"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO streams (artist, track_name, album, ms_played, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (artist, track_name, album, ms_played, timestamp))
    conn.commit()
    conn.close()

def insert_streams_bulk(streams_list):
    """Bulk insert streams. streams_list: list of (artist, track_name, album, ms_played, timestamp)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO streams (artist, track_name, album, ms_played, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', streams_list)
    conn.commit()
    conn.close()

def get_all_streams():
    """Fetch all streams from DB"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT artist, track_name, album, ms_played, timestamp
        FROM streams
        ORDER BY timestamp
    ''')
    results = cursor.fetchall()
    conn.close()
    return results

def get_stream_count():
    """Get total number of streams"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM streams')
    count = cursor.fetchone()[0]
    conn.close()
    return count

# ===== ALBUM GROUPINGS =====

def save_grouping(canonical_album, artist, constituent_albums):
    """Save user custom grouping"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    constituents_json = json.dumps(constituent_albums)
    
    cursor.execute('''
        INSERT OR REPLACE INTO album_groupings 
        (canonical_album, artist, constituents, modified_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (canonical_album, artist, constituents_json))
    
    conn.commit()
    conn.close()

def load_grouping(artist):
    """Load all groupings for an artist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT canonical_album, constituents 
        FROM album_groupings 
        WHERE artist = ?
    ''', (artist,))
    
    results = cursor.fetchall()
    conn.close()
    
    groupings = {}
    for canonical, constituents_json in results:
        groupings[canonical] = json.loads(constituents_json)
    
    return groupings

def delete_grouping(canonical_album, artist):
    """Delete a grouping"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM album_groupings 
        WHERE canonical_album = ? AND artist = ?
    ''', (canonical_album, artist))
    
    conn.commit()
    conn.close()

def clear_groupings():
    """Delete all groupings"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM album_groupings')
    conn.commit()
    conn.close()

# Initialize on import
if not os.path.exists(DB_PATH):
    init_db()