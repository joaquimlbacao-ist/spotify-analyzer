import requests
import os

MUSICBRAINZ_BASE = "https://musicbrainz.org/ws/2"
COVERART_BASE = "https://coverartarchive.org"
COVERS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "album_covers"
)

os.makedirs(COVERS_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "SpotifyAnalyzer/1.0 (https://github.com/joaquimlbacao-ist/spotify-analyzer)"
}

def search_album(artist, album):
    """Search MusicBrainz release group for album"""
    query = f'artist:"{artist}" AND releasegroup:"{album}"'
    params = {"query": query, "fmt": "json", "limit": 1}
    
    try:
        response = requests.get(f"{MUSICBRAINZ_BASE}/release-group", params=params, headers=HEADERS, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("release-groups"):
            return data["release-groups"][0]["id"]
        return None
    except requests.RequestException as e:
        print(f"MusicBrainz error: {e}")
        return None

def get_cover_url(release_group_mbid):
    """Get front cover URL from Cover Art Archive"""
    try:
        response = requests.get(f"{COVERART_BASE}/release-group/{release_group_mbid}", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        for image in data.get("images", []):
            if image.get("front"):
                return image.get("image")
        return None
    except requests.RequestException as e:
        print(f"Cover Art error: {e}")
        return None

def download_cover(cover_url, artist, album):
    """Download and save cover image locally"""
    try:
        response = requests.get(cover_url, timeout=10)
        response.raise_for_status()
        
        safe_artist = artist.replace("/", "_").replace("\\", "_").replace(":", "_")[:50]
        safe_album = album.replace("/", "_").replace("\\", "_").replace(":", "_")[:50]
        filename = f"{safe_artist}_{safe_album}.jpg"
        filepath = os.path.join(COVERS_DIR, filename)
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        return filepath
    except requests.RequestException as e:
        print(f"Download error: {e}")
        return None

def get_album_cover(artist, album):
    """Get album cover: search release group → get URL → download"""
    mbid = search_album(artist, album)
    if not mbid:
        return None
    
    cover_url = get_cover_url(mbid)
    if not cover_url:
        return None
    
    return download_cover(cover_url, artist, album)