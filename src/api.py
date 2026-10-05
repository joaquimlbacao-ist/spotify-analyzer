from flask import Flask, request, jsonify, send_from_directory
from src.loader import load_all_streams, StreamLoader
from src.analyzer import StreamAnalyzer
from flask_cors import CORS
import json
import os
import sys
from src.database import clear_streams, insert_streams_bulk
from src.music_service import get_album_cover
from src.database import get_stream_count


def get_frontend_path():
    """Get the path to the React build, both in development and PyInstaller."""
    if getattr(sys, 'frozen', False):
        # PyInstaller
        base_path = sys._MEIPASS
    else:
        # Normal development
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, 'spotify-frontend', 'build')


FRONTEND_BUILD = get_frontend_path()

app = Flask(
    __name__,
    static_folder=FRONTEND_BUILD,
    static_url_path=''
)

CORS(app)

analyzer = None

def init_analyzer():
    """Initialize analyzer from database"""
    global analyzer
    from src.database import get_stream_count
    if get_stream_count() > 0:
        analyzer = StreamAnalyzer()

# Initialize on startup
init_analyzer()

def process_json_files(file_objects):
    """Parse JSON files and return stream list"""
    streams = []
    for file_obj in file_objects:
        try:
            data = json.load(file_obj)
            if isinstance(data, list):
                streams.extend(data)
        except:
            continue
    return streams

@app.route('/api/artists', methods=['GET'])
def get_artists():
    """GET /api/artists?limit=10&year=2023&month=6"""
    limit = int(request.args.get('limit', 10))
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'streams')  # Default: streams
    
    results = analyzer.top_artists(limit=limit, year=year, month=month, start_date=start_date, end_date=end_date, sort_by=sort_by)
    return jsonify([{'name': r.name, 'stream_count': r.stream_count, 'total_ms': r.total_ms} for r in results])


@app.route('/api/tracks', methods=['GET'])
def get_tracks():
    """GET /api/tracks?limit=10&artist=The Weeknd&year=2023"""
    limit = int(request.args.get('limit', 10))
    artist = request.args.get('artist')
    album = request.args.get('album')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'streams')  # Default: streams

    results = analyzer.top_tracks(limit=limit, artist=artist, album=album, year=year, month=month, start_date=start_date, end_date= end_date, sort_by=sort_by)
    return jsonify([{'name': r.name, 'artist': r.artist, 'stream_count': r.stream_count, 'total_ms': r.total_ms} for r in results])


@app.route('/api/albums', methods=['GET'])
def get_albums():
    """GET /api/albums?limit=10&artist=The Weeknd&year=2023&aggregate=false"""
    limit = int(request.args.get('limit', 10))
    artist = request.args.get('artist')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'streams')
    aggregate = request.args.get('aggregate', 'false').lower() == 'true'  # ADD THIS
    
    results = analyzer.top_albums(limit=limit, artist=artist, year=year, month=month, start_date=start_date, end_date=end_date, sort_by=sort_by, aggregate=aggregate)
    return jsonify([{'name': r.name, 'artist': r.artist, 'stream_count': r.stream_count, 'total_ms': r.total_ms, 'is_aggregated': r.is_aggregated} for r in results])

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Upload and process Spotify JSON files (append mode with duplicate detection)"""
    global analyzer
    
    try:
        if 'files' not in request.files or len(request.files.getlist('files')) == 0:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        streams_data = process_json_files(files)
        
        if not streams_data:
            return jsonify({'error': 'No valid data found'}), 400
        
        loader = StreamLoader()
        filtered_streams = loader.filter_streams(streams_data)
        
        # Insert; the database skips rows that already exist
        streams_to_insert = [
            (s.artist, s.track_name, s.album, s.ms_played, s.ts)
            for s in filtered_streams
        ]
        added = insert_streams_bulk(streams_to_insert)
        duplicates = len(filtered_streams) - added
        
        # Reload analyzer
        analyzer = StreamAnalyzer()
        
        from src.database import get_stream_count
        total = get_stream_count()
        
        return jsonify({
            'added': added,
            'duplicates': duplicates,
            'total': total,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/has-data', methods=['GET'])
def has_data():
    """Check if database has any streams"""
    from src.database import get_stream_count
    count = get_stream_count()
    return jsonify({'has_streams': count > 0, 'count': count})

@app.route('/api/stream-info', methods=['GET'])
def stream_info():
    """Get stream count and date range"""
    from src.database import get_stream_count, get_stream_date_range
    count = get_stream_count()
    min_ts, max_ts = get_stream_date_range()
    return jsonify({
        'count': count,
        'min_date': min_ts,
        'max_date': max_ts
    })

@app.route('/api/streams', methods=['DELETE'])
def delete_streams():
    """Delete all streams from database"""
    global analyzer
    try:
        from src.database import clear_streams
        clear_streams()
        analyzer = StreamAnalyzer()
        return jsonify({'status': 'success', 'message': 'All streams deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# @app.route('/api/upload', methods=['POST'])
# def upload_files():
#     """Upload and process Spotify JSON files"""
#     global current_data
    
#     if 'files' not in request.files or len(request.files.getlist('files')) == 0:
#         return jsonify({'error': 'No files provided'}), 400
    
#     files = request.files.getlist('files')
#     streams_data = process_json_files(files)
    
#     if not streams_data:
#         return jsonify({'error': 'No valid data found'}), 400
    
#     # Load data into analyzer
#     try:
#         global analyzer
#         loader = StreamLoader()
#         filtered_streams = loader.filter_streams(streams_data)
#         analyzer = StreamAnalyzer(filtered_streams)
        
#         return jsonify({'count': len(filtered_streams), 'status': 'success'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/albums/grid', methods=['GET'])
def get_albums_grid():
    """GET /api/albums/grid?limit=9 - top albums with cached cover URLs"""
    limit = int(request.args.get('limit', 9))
    artist = request.args.get('artist')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'streams')
    aggregate = request.args.get('aggregate', 'false').lower() == 'true'
    
    try:
        results = analyzer.top_albums(limit=limit, artist=artist, year=year, month=month, start_date=start_date, end_date=end_date, sort_by=sort_by, aggregate=aggregate)
        
        albums_with_covers = []
        for album in results:
            cover_url = get_album_cover(album.artist, album.name)
            albums_with_covers.append({
                'name': album.name,
                'artist': album.artist,
                'stream_count': album.stream_count,
                'total_ms': album.total_ms,
                'is_aggregated': album.is_aggregated,
                'cover_url': cover_url
            })
        
        return jsonify(albums_with_covers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/album_covers/<filename>')
def serve_album_cover(filename):
    """Serve album covers from local cache"""
    covers_dir = os.path.join(os.path.dirname(__file__), '../album_covers')
    return send_from_directory(covers_dir, filename)

@app.route("/api/artists/timeline")
def artists_timeline():
    top = request.args.get("top", 5, type=int)
    start = request.args.get("start_date")
    end = request.args.get("end_date")
    metric = request.args.get("metric", "streams")
    bucket = request.args.get("bucket", "month")
    if bucket not in ("month", "year"):
        bucket = "month"
    artists = request.args.getlist("artist")
    return jsonify(analyzer.artist_timeline(top, start, end, metric, bucket, artists=artists or None))

@app.route("/api/artists/names")
def artist_names():
    return jsonify(analyzer.get_artists_by_popularity())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve the React frontend."""
    file_path = os.path.join(FRONTEND_BUILD, path)

    if path and os.path.isfile(file_path):
        return send_from_directory(FRONTEND_BUILD, path)

    return send_from_directory(FRONTEND_BUILD, 'index.html')

