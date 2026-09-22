from collections import defaultdict
from src.models import Stream, ArtistStats, TrackStats, AlbumStats
from datetime import datetime, timezone
import re
from src.database import get_all_streams

def are_album_versions(album1, album2):
    """
    Check whether two album titles are likely different versions
    of the same album.
    """

    def normalize(title):
        title = title.lower().strip()

        # Ignore leading articles
        title = re.sub(r'^(the|a|an)\s+', '', title)

        # Treat common separators as word boundaries
        title = re.sub(r'[\(\)\[\],:]', ' ', title)
        title = re.sub(r'\s*-\s*', ' ', title)

        # Normalize whitespace
        title = re.sub(r'\s+', ' ', title).strip()

        return title

    a = normalize(album1)
    b = normalize(album2)

    if not a or not b:
        return False

    # Split into words
    words_a = a.split()
    words_b = b.split()

    # Find longest common prefix
    common = []

    for word_a, word_b in zip(words_a, words_b):
        if word_a != word_b:
            break
        common.append(word_a)

    # No common prefix
    if not common:
        return False

    # If the titles are identical, they're obviously the same album
    if a == b:
        return True

    # Any shared prefix is considered sufficient
    return True


class StreamAnalyzer:
    """
    Analyzes Spotify streams with fast indexed queries.
    
    Handles filtering by year, month, artist, album and returns rankings.
    """

    def __init__(self):
        # Load streams from database
        db_streams = get_all_streams()
        
        # Convert database rows to Stream objects
        self.all_streams = [
            Stream(
                artist=row[0],
                track_name=row[1],
                album=row[2],
                ms_played=row[3],
                ts=datetime.fromisoformat(row[4]) if isinstance(row[4], str) else row[4]
            )
            for row in db_streams
        ]
        
        self._build_album_canonical()
        self._build_indexes()
    # def __init__(self, streams: list[Stream]):
    #     self.all_streams = streams
    #     self._build_album_canonical()
    #     self._build_indexes()

    def _build_album_canonical(self):
        """Build mapping of album variants to canonical names (preferring shortest)."""
        self.album_canonical = {}  # (artist, album) -> canonical_name
        seen_albums = {}  # artist -> list of canonical names
        canonical_map = {}  # canonical -> set of all variants
        
        for stream in self.all_streams:
            key = (stream.artist, stream.album)
            
            # Already processed
            if key in self.album_canonical:
                continue
            
            # Check if this album matches an existing canonical one
            canonical = stream.album
            artist_albums = seen_albums.get(stream.artist, [])
            
            matched_canonical = None
            for existing_canonical in artist_albums:
                if are_album_versions(stream.album, existing_canonical):
                    # Found a match - use the shorter name
                    if len(stream.album) < len(existing_canonical):
                        # Current version is simpler, promote it
                        canonical = stream.album
                        matched_canonical = existing_canonical
                    else:
                        canonical = existing_canonical
                    break
            
            # If we promoted a new canonical, update all existing variants
            if matched_canonical and canonical != matched_canonical:
                for (artist, album), old_canonical in list(self.album_canonical.items()):
                    if old_canonical == matched_canonical and artist == stream.artist:
                        self.album_canonical[(artist, album)] = canonical
                # Update canonical_map
                if matched_canonical in canonical_map:
                    canonical_map[canonical] = canonical_map.pop(matched_canonical)
            
            self.album_canonical[key] = canonical
            
            if canonical not in seen_albums.get(stream.artist, []):
                seen_albums.setdefault(stream.artist, []).append(canonical)
            
            canonical_map.setdefault(canonical, set()).add(stream.album)

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
        album: str = None,
        start_date: str = None,
        end_date: str = None
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
            filtered = [s for s in filtered if s.artist.lower() == artist.lower()]

        if album:
            filtered = [s for s in filtered if s.album.lower() == album.lower()]

        if start_date or end_date:
            try:
                if start_date:
                    start = datetime.strptime(start_date, "%d-%m-%Y").replace(tzinfo=timezone.utc)
                    filtered = [s for s in filtered if s.ts >= start]
                
                if end_date:
                    end = datetime.strptime(end_date, "%d-%m-%Y").replace(tzinfo=timezone.utc)
                    filtered = [s for s in filtered if s.ts <= end]
            except ValueError:
                pass
        
        return filtered
    
    def top_artists(self, limit: int = 10, year: int = None, month: int = None, start_date: str = None, end_date: str = None, sort_by: str = 'streams') -> list[ArtistStats]:
        """
        Get top artists by stream count.
        
        Args:
            limit: Number of results (default: 10)
            year: Filter to specific year
            month: Filter to specific month (requires year)
            start_date: Filter from date (format: DD-MM-YYYY)
            end_date: Filter to date (format: DD-MM-YYYY)
            sort_by: 'streams' (default) or 'time' (by total_ms)
        
        Returns:
            List of ArtistStats sorted by chosen metric (descending)
        """
        streams = self.all_streams
        streams = self._filter_streams(streams, year=year, month=month, start_date=start_date, end_date=end_date)
        
        # Count streams and sum ms per artist
        artist_counts = defaultdict(int)
        artist_ms = defaultdict(int)
        for stream in streams:
            artist_counts[stream.artist] += 1
            artist_ms[stream.artist] += stream.ms_played
        
        # Sort by chosen metric
        sort_key = lambda x: artist_ms[x[0]] if sort_by == 'time' else x[1]
        sorted_artists = sorted(
            artist_counts.items(),
            key=sort_key,
            reverse=True
        )[:limit]
        
        # Convert to ArtistStats objects
        results = [
            ArtistStats(name=name, stream_count=count, total_ms=artist_ms[name])
            for name, count in sorted_artists
        ]
        return results
    
    def top_tracks(
        self, 
        limit: int = 10, 
        artist: str = None, 
        album: str = None,
        year: int = None, 
        month: int = None,
        start_date: str = None,
        end_date: str = None,
        sort_by: str = 'streams'
    ) -> list[TrackStats]:
        """
        Get top tracks by stream count.
        
        Args:
            limit: Number of results
            artist: Filter to specific artist
            album: Filter to specific album
            year: Filter to specific year
            month: Filter to specific month (requires year)
            start_date: Filter from date (format: DD-MM-YYYY)
            end_date: Filter to date (format: DD-MM-YYYY)
            sort_by: 'streams' (default) or 'time' (by total_ms)
        
        Returns:
            List of TrackStats sorted by chosen metric (descending)
        """
        streams = self.all_streams
        streams = self._filter_streams(streams, year=year, month=month, artist=artist, album=album, start_date=start_date, end_date=end_date)
        
        # Count streams per (artist, track_name)
        track_counts = defaultdict(int)
        track_ms = defaultdict(int)
        
        for stream in streams:
            key = (stream.artist, stream.track_name)
            track_counts[key] += 1
            track_ms[key] += stream.ms_played
        
        # Sort by chosen metric
        sort_key = lambda x: track_ms[x[0]] if sort_by == 'time' else x[1]
        sorted_tracks = sorted(
            track_counts.items(),
            key=sort_key,
            reverse=True
        )[:limit]
        
        # Convert to TrackStats objects
        results = [
            TrackStats(
                name=(artist_track[0][1]),  # track name
                artist=artist_track[0][0],  # artist name
                stream_count=artist_track[1],
                total_ms=track_ms[artist_track[0]]
            )
            for artist_track in sorted_tracks
        ]
        return results
    
    def top_albums(
        self, 
        limit: int = 10, 
        artist: str = None,
        year: int = None, 
        month: int = None,
        start_date: str = None,
        end_date: str = None,
        sort_by: str = 'streams',
        aggregate: bool = False
    ) -> list[AlbumStats]:
        """
        Get top albums by stream count.
        
        Args:
            limit: Number of results
            artist: Filter to specific artist
            year: Filter to specific year
            month: Filter to specific month (requires year)
            start_date: Filter from date (format: DD-MM-YYYY)
            end_date: Filter to date (format: DD-MM-YYYY)
            sort_by: 'streams' (default) or 'time' (by total_ms)
            aggregate: If True, combine album versions into canonical names
        
        Returns:
            List of AlbumStats sorted by chosen metric (descending)
        """
        streams = self.all_streams
        streams = self._filter_streams(streams, year=year, month=month, artist=artist, start_date=start_date, end_date=end_date)
        
        # Count streams per (artist, album)
        album_counts = defaultdict(int)
        album_ms = defaultdict(int)
        album_variants = defaultdict(set)  # Track original names per canonical
        
        for stream in streams:
            if aggregate:
                # Use canonical name
                key = (stream.artist, self.album_canonical[(stream.artist, stream.album)])
                album_variants[key].add(stream.album)
            else:
                # Use original name
                key = (stream.artist, stream.album)
                album_variants[key].add(stream.album)
            
            album_counts[key] += 1
            album_ms[key] += stream.ms_played
        
        # Sort by chosen metric
        sort_key = lambda x: album_ms[x[0]] if sort_by == 'time' else x[1]
        sorted_albums = sorted(
            album_counts.items(),
            key=sort_key,
            reverse=True
        )[:limit]
        
        # Convert to AlbumStats objects
        results = [
            AlbumStats(
                name=artist_album[0][1],  # album name
                artist=artist_album[0][0],  # artist name
                stream_count=artist_album[1],
                total_ms=album_ms[artist_album[0]],
                is_aggregated=aggregate and len(album_variants[artist_album[0]]) > 1
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
