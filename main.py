#!/usr/bin/env python3

import sys
from loader import load_all_streams
from analyzer import StreamAnalyzer
from ui import SpotifyAnalyzerUI


def main():
    """Load data and start interactive analysis."""
    
    # Get data folder from command line or use default
    if len(sys.argv) > 1:
        data_folder = sys.argv[1]
    else:
        data_folder = "./data"
    
    print("="*50)
    print("=== SPOTIFY ANALYZER ===")
    print("="*50)
    print(f"\nLoading Spotify streams from: {data_folder}\n")
    
    try:
        # Load streams
        streams = load_all_streams(data_folder)
        print(f"\n✓ Successfully loaded {len(streams):,} streams\n")
        
        # Create analyzer with indexed data
        analyzer = StreamAnalyzer(streams)
        
        # Start interactive UI
        ui = SpotifyAnalyzerUI(analyzer)
        ui.display_menu()
    
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nUsage:")
        print("  python main.py                      (uses ./data folder)")
        print("  python main.py /path/to/spotify     (uses custom folder)")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
