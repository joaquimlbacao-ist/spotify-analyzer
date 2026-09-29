import requests

MUSICBRAINZ_BASE = "https://musicbrainz.org/ws/2"
COVERART_BASE = "https://coverartarchive.org"

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

def get_album_cover(artist, album):
    """Get album cover URL (no download, just return URL)"""
    mbid = search_album(artist, album)
    if not mbid:
        return None
    return get_cover_url(mbid)