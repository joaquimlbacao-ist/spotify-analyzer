import pytest
from src.loader import load_all_streams


class TestLoader:
    """Test cases for loader.py"""
    
    def test_load_streams(self):
        """Test loading JSON file."""
        streams = load_all_streams("tests/data")
        
        assert len(streams) == 2  # Only 2 valid tracks (filters out podcast and <15s)
    
    def test_filters_podcasts(self):
        """Test that podcasts (null track_name) are filtered."""
        streams = load_all_streams("tests/data")
        
        # No podcast should be in results
        assert all(s.track_name is not None for s in streams)
    
    def test_filters_short_plays(self):
        """Test that plays < 15 seconds are filtered."""
        streams = load_all_streams("tests/data")
        
        # All streams should be >= 15 seconds
        assert all(s.ms_played >= 15000 for s in streams)
    
    def test_parses_timestamps(self):
        """Test that timestamps are parsed correctly."""
        streams = load_all_streams("tests/data")
        
        assert len(streams) > 0
        first_stream = streams[0]
        assert first_stream.ts.year == 2023
        assert first_stream.ts.month == 6
    
    def test_missing_folder_raises_error(self):
        """Test that missing folder raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_all_streams("nonexistent/folder")