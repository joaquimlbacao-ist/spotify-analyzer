from src.analyzer import StreamAnalyzer
import calendar


class SpotifyAnalyzerUI:
    """Terminal interface for Spotify analysis."""
    
    def __init__(self, analyzer: StreamAnalyzer):
        self.analyzer = analyzer
    
    def _print_table(self, headers: list, rows: list):
        """
        Print a formatted table.
        
        Args:
            headers: List of column headers
            rows: List of tuples (one per row)
        """
        # Calculate column widths
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(str(header))
            for row in rows:
                max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width)
        
        # Print header
        header_line = " | ".join(
            str(headers[i]).ljust(col_widths[i]) for i in range(len(headers))
        )
        print(header_line)
        print("-" * len(header_line))
        
        # Print rows
        for row in rows:
            row_line = " | ".join(
                str(row[i]).ljust(col_widths[i]) if i > 0 else str(row[i]).rjust(col_widths[i])
                for i in range(len(row))
            )
            print(row_line)
    
    def display_top_artists(self, limit: int = 10, year: int = None, month: int = None):
        """Display top artists in a table."""
        results = self.analyzer.top_artists(limit=limit, year=year, month=month)
        
        # Print title
        print("\n=== TOP ARTISTS ===")
        if year and month:
            print(f"{calendar.month_name[month]} {year}\n")
        elif year:
            print(f"Year {year}\n")
        else:
            print("All Time\n")
        
        if not results:
            print("No data found.")
            return
        
        # Prepare table
        headers = ["#", "Artist", "Streams"]
        rows = [
            (rank, result.name, f"{result.stream_count:,}")
            for rank, result in enumerate(results, 1)
        ]
        
        self._print_table(headers, rows)
    
    def display_top_tracks(self, limit: int = 10, artist: str = None, album: str = None, 
                          year: int = None, month: int = None):
        """Display top tracks in a table."""
        results = self.analyzer.top_tracks(limit=limit, artist=artist, album=album, year=year, month=month)
        
        # Print title
        print("\n=== TOP TRACKS ===")
        if year and month:
            print(f"{calendar.month_name[month]} {year}", end="")
        elif year:
            print(f"Year {year}", end="")
        
        if artist:
            print(f" | Artist: {artist}", end="")
        if album:
            print(f" | Album: {album}", end="")
        
        print("\n")
        
        if not results:
            print("No data found.")
            return
        
        # Prepare table
        headers = ["#", "Artist", "Track Name", "Streams"]
        rows = [
            (rank, result.artist, result.name, f"{result.stream_count:,}")
            for rank, result in enumerate(results, 1)
        ]
        
        self._print_table(headers, rows)
    
    def display_top_albums(self, limit: int = 10, artist: str = None, 
                          year: int = None, month: int = None):
        """Display top albums in a table."""
        results = self.analyzer.top_albums(limit=limit, artist=artist, year=year, month=month)
        
        # Print title
        print("\n=== TOP ALBUMS ===")
        if year and month:
            print(f"{calendar.month_name[month]} {year}", end="")
        elif year:
            print(f"Year {year}", end="")
        
        if artist:
            print(f" | Artist: {artist}", end="")
        
        print("\n")
        
        if not results:
            print("No data found.")
            return
        
        # Prepare table
        headers = ["#", "Artist", "Album", "Streams"]
        rows = [
            (rank, result.artist, result.name, f"{result.stream_count:,}")
            for rank, result in enumerate(results, 1)
        ]
        
        self._print_table(headers, rows)
    
    def menu_top_artists(self):
        """Sub-menu for top artists with optional filters."""
        year = self._prompt_year()
        month = None
        if year:
            month = self._prompt_month()
        
        limit = self._prompt_limit()
        self.display_top_artists(limit=limit, year=year, month=month)
    
    def menu_top_tracks(self):
        """Sub-menu for top tracks with optional filters."""
        artist = self._prompt_artist()
        album = None
        if artist:
            album = self._prompt_album()
        
        year = self._prompt_year()
        month = None
        if year:
            month = self._prompt_month()
        
        limit = self._prompt_limit()
        self.display_top_tracks(limit=limit, artist=artist, album=album, year=year, month=month)
    
    def menu_top_albums(self):
        """Sub-menu for top albums with optional filters."""
        artist = self._prompt_artist()
        
        year = self._prompt_year()
        month = None
        if year:
            month = self._prompt_month()
        
        limit = self._prompt_limit()
        self.display_top_albums(limit=limit, artist=artist, year=year, month=month)
    
    # ===== Helper prompts =====
    
    def _prompt_year(self) -> int:
        """Prompt user for optional year filter."""
        years = self.analyzer.get_years()
        response = input(f"Filter by year? ({min(years)}-{max(years)}, or leave blank): ").strip()
        
        if not response:
            return None
        
        try:
            year = int(response)
            if year in years:
                return year
            else:
                print(f"Year {year} not found in data.")
                return None
        except ValueError:
            print("Invalid year.")
            return None
    
    def _prompt_month(self) -> int:
        """Prompt user for optional month filter."""
        response = input("Filter by month? (1-12, or leave blank): ").strip()
        
        if not response:
            return None
        
        try:
            month = int(response)
            if 1 <= month <= 12:
                return month
            else:
                print("Month must be 1-12.")
                return None
        except ValueError:
            print("Invalid month.")
            return None
    
    def _prompt_artist(self) -> str:
        """Prompt user for optional artist filter."""
        response = input("Filter by artist? (leave blank for all): ").strip()
        
        if not response:
            return None
        
        # Could add fuzzy matching here in future
        return response
    
    def _prompt_album(self) -> str:
        """Prompt user for optional album filter."""
        response = input("Filter by album? (leave blank for all): ").strip()
        
        if not response:
            return None
        
        return response
    
    def _prompt_limit(self) -> int:
        """Prompt user for number of results."""
        response = input("How many results? (default: 10): ").strip()
        
        if not response:
            return 10
        
        try:
            limit = int(response)
            if limit > 0:
                return limit
            else:
                print("Limit must be > 0.")
                return 10
        except ValueError:
            print("Invalid number.")
            return 10
    
    def display_menu(self):
        """Main menu loop."""
        while True:
            print("\n" + "="*40)
            print("=== SPOTIFY ANALYZER ===")
            print("="*40)
            print("1. Top Artists")
            print("2. Top Tracks")
            print("3. Top Albums")
            print("4. Exit")
            print("="*40)
            
            choice = input("\nSelect (1-4): ").strip()
            
            if choice == "1":
                self.menu_top_artists()
            elif choice == "2":
                self.menu_top_tracks()
            elif choice == "3":
                self.menu_top_albums()
            elif choice == "4":
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice.")
