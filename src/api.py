import sys
from flask import Flask, request, jsonify
from src.loader import load_all_streams
from src.analyzer import StreamAnalyzer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
analyzer = None



def init_analyzer(data_folder=None):
    if data_folder is None:
        data_folder = sys.argv[1] if len(sys.argv) > 1 else "./data"
    global analyzer
    print(f"Loading streams from {data_folder}...")
    streams = load_all_streams(data_folder)
    analyzer = StreamAnalyzer(streams)
    print(f"✓ Loaded {len(streams):,} streams")


@app.route('/api/artists', methods=['GET'])
def get_artists():
    """GET /api/artists?limit=10&year=2023&month=6"""
    limit = int(request.args.get('limit', 10))
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    results = analyzer.top_artists(limit=limit, year=year, month=month)
    return jsonify([{'name': r.name, 'stream_count': r.stream_count} for r in results])


@app.route('/api/tracks', methods=['GET'])
def get_tracks():
    """GET /api/tracks?limit=10&artist=The Weeknd&year=2023"""
    limit = int(request.args.get('limit', 10))
    artist = request.args.get('artist')
    album = request.args.get('album')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    results = analyzer.top_tracks(limit=limit, artist=artist, album=album, year=year, month=month)
    return jsonify([{'name': r.name, 'artist': r.artist, 'stream_count': r.stream_count} for r in results])


@app.route('/api/albums', methods=['GET'])
def get_albums():
    """GET /api/albums?limit=10&artist=The Weeknd&year=2023"""
    limit = int(request.args.get('limit', 10))
    artist = request.args.get('artist')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    results = analyzer.top_albums(limit=limit, artist=artist, year=year, month=month)
    return jsonify([{'name': r.name, 'artist': r.artist, 'stream_count': r.stream_count} for r in results])


if __name__ == '__main__':
    init_analyzer()
    app.run(debug=True, port=8000)