import json
from pathlib import Path
from datetime import datetime
from src.models import Stream


def load_all_streams(data_folder: str) -> list[Stream]:
    """
    Load and parse all JSON files from Spotify export folder.
    
    Filters:
    - Skips podcasts and audiobooks (only tracks)
    - Skips plays < 15 seconds
    
    Args:
        data_folder: Path to folder containing StreamingHistory JSON files
    
    Returns:
        List of Stream objects
    """
    streams = []
    data_path = Path(data_folder)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data folder not found: {data_folder}")
    
    # Find all JSON files matching Spotify export pattern
    json_files = sorted(data_path.glob("Streaming_History_Audio*.json"))
    
    if not json_files:
        raise FileNotFoundError(f"No Streaming_History_Audio JSON files found in {data_folder}")
    
    for json_file in json_files:
        print(f"  Loading {json_file.name}...", end=" ")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            records = json.load(f)
        
        file_streams = 0
        for record in records:
            # Skip if not a music track (ignore podcasts/audiobooks)
            if record.get("master_metadata_track_name") is None:
                continue
            
            # Skip if < 15 seconds
            if record.get("ms_played", 0) < 15000:
                continue
            
            # Parse timestamp
            ts_str = record.get("ts", "")
            if not ts_str:
                continue
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            
            # Create Stream object
            stream = Stream(
                ts=ts,
                track_name=record["master_metadata_track_name"],
                artist=record["master_metadata_album_artist_name"],
                album=record["master_metadata_album_album_name"],
                ms_played=record["ms_played"],
                track_uri=record["spotify_track_uri"]
            )
            streams.append(stream)
            file_streams += 1
        
        print(f"{file_streams} valid streams")
    
    return streams
