from flask import Flask, request, jsonify
from src.loader import load_all_streams, StreamLoader
from src.analyzer import StreamAnalyzer
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
CORS(app)
analyzer = None

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
    """GET /api/albums?limit=10&artist=The Weeknd&year=2023"""
    limit = int(request.args.get('limit', 10))
    artist = request.args.get('artist')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'streams')  # Default: streams
    
    results = analyzer.top_albums(limit=limit, artist=artist, year=year, month=month, start_date=start_date, end_date= end_date, sort_by=sort_by)
    return jsonify([{'name': r.name, 'artist': r.artist, 'stream_count': r.stream_count, 'total_ms': r.total_ms} for r in results])

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Upload and process Spotify JSON files"""
    global current_data
    
    if 'files' not in request.files or len(request.files.getlist('files')) == 0:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    streams_data = process_json_files(files)
    
    if not streams_data:
        return jsonify({'error': 'No valid data found'}), 400
    
    # Load data into analyzer
    try:
        global analyzer
        loader = StreamLoader()
        filtered_streams = loader.filter_streams(streams_data)
        analyzer = StreamAnalyzer(filtered_streams)
        
        return jsonify({'count': len(filtered_streams), 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)