from dataclasses import dataclass
from datetime import datetime


@dataclass
class Stream:
    """A single play event from Spotify history."""
    ts: datetime
    track_name: str
    artist: str
    album: str
    ms_played: int
    track_uri: str


@dataclass
class ArtistStats:
    """Aggregated statistics for an artist."""
    name: str
    stream_count: int
    total_ms: int = 0

@dataclass
class TrackStats:
    """Aggregated statistics for a track."""
    name: str
    artist: str
    stream_count: int
    total_ms: int = 0

@dataclass
class AlbumStats:
    """Aggregated statistics for an album."""
    name: str
    artist: str
    stream_count: int
    total_ms: int = 0