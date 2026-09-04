# Spotify Analyzer

Analyze your Spotify listening history from your exported data.

## Setup

1. **Get your Spotify data:**
   - Go to https://www.spotify.com/account/privacy/
   - Request your data download
   - Wait for email, download the archive
   - Extract it locally

2. **Prepare the data folder:**
   - Find the folder containing `Streaming_History_Audio_*.json` files
   - Note the path (e.g., `/Users/joaquim/Downloads/MySpotifyData`)

## Running

```bash
# Using default ./data folder
python main.py

# Using custom folder
python main.py /path/to/spotify/data
```

## Usage

The app will show an interactive menu:

```
=== SPOTIFY ANALYZER ===
1. Top Artists
2. Top Tracks
3. Top Albums
4. Exit
```

For each query, you can optionally filter by:
- **Year** and **Month**
- **Artist** and **Album** (depending on query type)
- **Number of results** (default: 10)

## Example

```
Select (1-4): 1
Filter by year? (2015-2024, or leave blank): 2023
Filter by month? (1-12, or leave blank): 6
How many results? (default: 10): 5

=== TOP ARTISTS ===
Year 2023

#  | Artist              | Streams
----|---------------------|----------
1  | The Weeknd          | 145
2  | Arctic Monkeys      | 98
3  | Tame Impala         | 87
4  | Frank Ocean         | 76
5  | Tyler, The Creator  | 65
```

## Data Processing

- **Filters out:**
  - Podcasts and audiobooks
  - Plays shorter than 15 seconds
  
- **Keeps:** All music tracks from your export

- **Metrics:** Stream count (total number of plays)

## Files

- `models.py` — Data structures
- `loader.py` — Parse JSON exports
- `analyzer.py` — Query engine with indexing
- `ui.py` — Terminal interface
- `main.py` — Entry point

## Future Features

- Time-based metrics (hours listened, not just plays)
- Day-level filtering
- Web interface
- Trend analysis
