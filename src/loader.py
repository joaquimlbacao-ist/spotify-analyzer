import json
from pathlib import Path
from datetime import datetime
from src.models import Stream

class StreamLoader:
    """Parse raw JSON records into Stream objects"""
    
    @staticmethod
    def filter_streams(records: list) -> list[Stream]:
        """
        Filter and parse raw JSON records into Stream objects.
        
        Filters:
        - Skips podcasts and audiobooks (only tracks)
        - Skips plays < 15 seconds
        """
        streams = []
        
        for record in records:
            # Skip if not a music track
            if record.get("master_metadata_track_name") is None:
                continue
            
            # Skip if < 15 seconds
            if record.get("ms_played", 0) < 15000:
                continue
            
            # Parse timestamp
            ts_str = record.get("ts", "")
            if not ts_str:
                continue
            
            try:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except:
                continue
            
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
        
        return streams