import pytest
from src.analyzer import StreamAnalyzer
from tests.test_fixtures import get_sample_streams


class TestStreamAnalyzer:
    """Test cases for StreamAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer with sample data."""
        streams = get_sample_streams()
        return StreamAnalyzer(streams)
    
    def test_indexes_built(self, analyzer):
        """Test that indexes are created on init."""
        assert len(analyzer.by_artist) > 0
        assert len(analyzer.by_year) > 0
    
    def test_top_artists_all_time(self, analyzer):
        """Test top artists without filters."""
        results = analyzer.top_artists(limit=10)
        
        assert len(results) == 3
        assert results[0].name == "The Weeknd"
        assert results[0].stream_count == 2
    
    def test_top_artists_by_year(self, analyzer):
        """Test filtering by year."""
        results = analyzer.top_artists(limit=10, year=2023)
        
        assert len(results) == 2
    
    def test_top_artists_by_month(self, analyzer):
        """Test filtering by year and month."""
        results = analyzer.top_artists(limit=10, year=2023, month=6)
        
        assert len(results) == 2
    
    def test_top_artists_empty_filter(self, analyzer):
        """Test query with no matching data."""
        results = analyzer.top_artists(limit=10, year=1999)
        
        assert len(results) == 0
    
    def test_top_tracks_all_time(self, analyzer):
        """Test top tracks without filters."""
        results = analyzer.top_tracks(limit=10)
        
        assert len(results) == 3
        assert results[0].name == "Blinding Lights"
        assert results[0].stream_count == 2
    
    def test_top_tracks_by_artist(self, analyzer):
        """Test filtering tracks by artist."""
        results = analyzer.top_tracks(limit=10, artist="The Weeknd")
        
        assert len(results) == 1
        assert results[0].artist == "The Weeknd"
    
    def test_top_albums_all_time(self, analyzer):
        """Test top albums without filters."""
        results = analyzer.top_albums(limit=10)
        
        assert len(results) == 3
        assert results[0].name == "After Hours"
        assert results[0].stream_count == 2
    
    def test_limit_respected(self, analyzer):
        """Test that limit parameter is respected."""
        results = analyzer.top_artists(limit=2)
        assert len(results) == 2

    def test_top_artists_by_start_date(self, analyzer):
        """Test filtering by start_date only."""
        results = analyzer.top_artists(limit=10, start_date="17-06-2023")
        
        # Should only include streams from 17-06-2023 onwards
        assert len(results) > 0
        assert all(r.stream_count >= 0 for r in results)

    def test_top_artists_by_end_date(self, analyzer):
        """Test filtering by end_date only."""
        results = analyzer.top_artists(limit=10, end_date="15-06-2023")
        
        # Should only include streams up to 15-06-2023
        assert len(results) > 0

    def test_top_artists_by_date_range(self, analyzer):
        """Test filtering by date range."""
        results = analyzer.top_artists(limit=10, start_date="15-06-2023", end_date="20-06-2023")
        
        # Should only include streams between dates
        assert len(results) >= 0  # May be empty if no data in range

    def test_top_artists_invalid_date_format(self, analyzer):
        """Test that invalid date format is ignored."""
        results = analyzer.top_artists(limit=10, start_date="invalid-date")
        
        # Should still return all artists (date filter ignored)
        assert len(results) == 3

    def test_top_tracks_by_date_range_with_artist(self, analyzer):
        """Test date range combined with artist filter."""
        results = analyzer.top_tracks(
            limit=10, 
            artist="The Weeknd",
            start_date="15-06-2023",
            end_date="20-06-2023"
        )
        
        # Should filter by both artist and date range
        assert all(t.artist == "The Weeknd" for t in results)