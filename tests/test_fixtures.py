from datetime import datetime
from src.models import Stream

def get_sample_streams():
    """Return test data."""
    return [
        Stream(
            ts=datetime(2023, 6, 15, 10, 30),
            track_name="Blinding Lights",
            artist="The Weeknd",
            album="After Hours",
            ms_played=180000,
            track_uri="spotify:track:123"
        ),
        Stream(
            ts=datetime(2023, 6, 15, 11, 0),
            track_name="505",
            artist="Arctic Monkeys",
            album="AM",
            ms_played=258000,
            track_uri="spotify:track:124"
        ),
        Stream(
            ts=datetime(2023, 6, 20, 14, 0),
            track_name="Blinding Lights",
            artist="The Weeknd",
            album="After Hours",
            ms_played=180000,
            track_uri="spotify:track:123"
        ),
        Stream(
            ts=datetime(2022, 12, 1, 10, 0),
            track_name="The Less I Know The Better",
            artist="Tame Impala",
            album="Lonerism",
            ms_played=216000,
            track_uri="spotify:track:125"
        ),
    ]