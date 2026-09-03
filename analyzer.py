from collections import defaultdict
from models import Stream, ArtistStats, TrackStats, AlbumStats


class StreamAnalyzer:
    """
    Analyzes Spotify streams with fast indexed queries.
    
    Handles filtering by year, month, artist, album and returns rankings.
    """
    
    def __init__(self, streams: list[Stream]):
        self.all_streams = streams
        self._build_indexes()
    
    def _build_indexes(self):
        """Create lookup tables for fast queries."""
        self.by_artist = defaultdict(list)
        self.by_year = defaultdict(list)
        self.by_month = defaultdict(list)  # (year, month) -> streams
        self.by_album = defaultdict(list)  # (artist, album) -> streams
        
        for stream in self.all_streams:
            self.by_artist[stream.artist].append(stream)
            self.by_year[stream.ts.year].append(stream)
            self.by_month[(stream.ts.year, stream.ts.month)].append(stream)
            self.by_album[(stream.artist, stream.album)].append(stream)
    
    def _filter_streams(
        self, 
        streams: list[Stream], 
        year: int = None, 
        month: int = None, 
        artist: str = None, 
        album: str = None
    ) -> list[Stream]:
        """
        Apply filters to a list of streams.
        
        Args:
            streams: List to filter
            year: Filter to specific year (None = all years)
            month: Filter to specific month (requires year)
            artist: Filter to specific artist
            album: Filter to specific album
        
        Returns:
            Filtered list of streams
        """
        filtered = streams
        
        if year:
            filtered = [s for s in filtered if s.ts.year == year]
        
        if month and year:
            filtered = [s for s in filtered if s.ts.year == year and s.ts.month == month]
        
        if artist:
            filtered = [s for s in filtered if s.artist == artist]
        
        if album:
            filtered = [s for s in filtered if s.album == album]
        
        return filtered
    
    def top_artists(self, limit: int = 10, year: int = None, month: int = None) -> list[ArtistStats]:
        """
        Get top artists by stream count.
        
        Args:
            limit: Number of results (default: 10)
            year: Filter to specific year
            month: Filter to specific month (requires year)
        
        Returns:
            List of ArtistStats sorted by stream count (descending)
        """
        streams = self.all_streams
        streams = self._filter_streams(streams, year=year, month=month)
        
        # Count streams per artist
        artist_counts = defaultdict(int)
        for stream in streams:
            artist_counts[stream.artist] += 1
        
        # Sort by count (descending)
        sorted_artists = sorted(
            artist_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        # Convert to ArtistStats objects
        results = [
            ArtistStats(name=name, stream_count=count)
            for name, count in sorted_artists
        ]
        return results
    
    def top_tracks(
        self, 
        limit: int = 10, 
        artist: str = None, 
        album: str = None,
        year: int = None, 
        month: int = None
    ) -> list[TrackStats]:
        """
        Get top tracks by stream count.
        
        Args:
            limit: Number of results
            artist: Filter to specific artist
            album: Filter to specific album
            year: Filter to specific year
            month: Filter to specific month (requires year)
        
        Returns:
            List of TrackStats sorted by stream count (descending)
        """
        streams = self.all_streams
        streams = self._filter_streams(streams, year=year, month=month, artist=artist, album=album)
        
        # Count streams per (artist, track_name)
        track_counts = defaultdict(int)
        track_artists = {}  # Keep track of artist for display
        
        for stream in streams:
            key = (stream.artist, stream.track_name)
            track_counts[key] += 1
            track_artists[key] = stream.artist
        
        # Sort by count (descending)
        sorted_tracks = sorted(
            track_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        # Convert to TrackStats objects
        results = [
            TrackStats(
                name=(artist_track[0][1]),  # track name
                artist=artist_track[0][0],  # artist name
                stream_count=artist_track[1]
            )
            for artist_track in sorted_tracks
        ]
        return results
    
    def top_albums(
        self, 
        limit: int = 10, 
        artist: str = None,
        year: int = None, 
        month: int = None
    ) -> list[AlbumStats]:
        """
        Get top albums by stream count.
        
        Args:
            limit: Number of results
            artist: Filter to specific artist
            year: Filter to specific year
            month: Filter to specific month (requires year)
        
        Returns:
            List of AlbumStats sorted by stream count (descending)
        """
        streams = self.all_streams
        streams = self._filter_streams(streams, year=year, month=month, artist=artist)
        
        # Count streams per (artist, album)
        album_counts = defaultdict(int)
        
        for stream in streams:
            key = (stream.artist, stream.album)
            album_counts[key] += 1
        
        # Sort by count (descending)
        sorted_albums = sorted(
            album_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        # Convert to AlbumStats objects
        results = [
            AlbumStats(
                name=artist_album[0][1],  # album name
                artist=artist_album[0][0],  # artist name
                stream_count=artist_album[1]
            )
            for artist_album in sorted_albums
        ]
        return results
    
    def get_all_artists(self) -> list[str]:
        """Return sorted list of all unique artists."""
        return sorted(self.by_artist.keys())
    
    def get_years(self) -> list[int]:
        """Return sorted list of all years with streams."""
        return sorted(self.by_year.keys())
