from spotipy.exceptions import SpotifyException

from app.api.spotify_client import sp


# 키워드 기반 (장르를 자연어로 검색)
def fetch_playlists_by_genre(genre_keyword: str, limit=50, offset=0):
    """
    장르 키워드로 플레이리스트 검색 (예: 'K-pop', 'Pop', '한국 발라드', 'Hip-hop')
    """
    result = sp.search(q=genre_keyword, type='playlist', limit=limit, offset=offset)
    playlists = result.get('playlists', {}).get('items', [])
    return playlists

# 카테고리 기반 (Spotify가 제공하는 공식 카테고리 ID 사용) + fallback

def fetch_playlists_by_category(category_id: str, country="KR", limit=20):
    """
    Spotify 카테고리 ID 기반 플레이리스트 조회 (예: 'pop', 'k-pop', 'mood')
    """
    try:
        result = sp.category_playlists(category_id=category_id, country=country, limit=limit)
        return result.get('playlists', {}).get('items', [])
    except SpotifyException as e:
        print(f"[WARN] category '{category_id}' not found in country='{country}', fallback to 'US' → {e}")
        try:
            result = sp.category_playlists(category_id=category_id, country="US", limit=limit)
            return result.get('playlists', {}).get('items', [])
        except Exception as e2:
            print(f"[ERROR] fallback to US also failed: {e2}")
            return []

# 플레이리스트 상세 정보 조회
def fetch_playlist_details(playlist_id: str) -> dict:
    """
    playlist_id를 기준으로 상세 정보를 조회합니다.
    """
    playlist = sp.playlist(playlist_id)

    image = playlist.get("images", [{}])[0]
    owner = playlist.get("owner", {})
    followers = playlist.get("followers", {}).get("total", 0)
    tracks = playlist.get("tracks", {}).get("items", [])

    return {
        "id": playlist.get("id"),
        "name": playlist.get("name"),
        "description": playlist.get("description"),
        "image_url": image.get("url"),
        "image_width": image.get("width"),
        "image_height": image.get("height"),
        "owner_id": owner.get("id"),
        "owner_name": owner.get("display_name"),
        "followers": followers,
        "tracks": tracks,
    }

# Spotify 카테고리 이름 → ID 매핑 딕셔너리
CATEGORY_NAME_TO_ID = {
    "korean": "0JQ5DAqbMKFQtzIMjOW2bE",
    "k-pop": "0JQ5DAqbMKFGvOw3O4nLAf",
    "케이팝": "0JQ5DAqbMKFGvOw3O4nLAf",
    "한국노래": "0JQ5DAqbMKFQtzIMjOW2bE",
    "pop": "0JQ5DAqbMKFEC4WFtoNRpw",
    "팝": "0JQ5DAqbMKFEC4WFtoNRpw",
    "hiphop": "0JQ5DAqbMKFQ00XGBls6ym",
    "힙합": "0JQ5DAqbMKFQ00XGBls6ym",
    "mood": "0JQ5DAqbMKFzHmL4tf05da",
    "분위기": "0JQ5DAqbMKFzHmL4tf05da",
    "rock": "0JQ5DAqbMKFDXXwE9BDJAr",
    "락": "0JQ5DAqbMKFDXXwE9BDJAr",
    "indie": "0JQ5DAqbMKFCWjUTdzaG0e",
    "인디": "0JQ5DAqbMKFCWjUTdzaG0e"
}

def get_category_id_from_keyword(keyword: str) -> str | None:
    """
    사용자 키워드를 Spotify 카테고리 ID로 매핑 (한글/영문 대응)
    """
    keyword = keyword.lower()
    for key, cid in CATEGORY_NAME_TO_ID.items():
        if key in keyword:
            return cid
    return None

# 🔁 사용 예시:
if __name__ == "__main__":
    keyword = "케이팝"
    category_id = get_category_id_from_keyword(keyword)

    if category_id:
        playlists = fetch_playlists_by_category(category_id)
        if not playlists:
            print("[INFO] Fallback to keyword search")
            playlists = fetch_playlists_by_genre(keyword)
    else:
        playlists = fetch_playlists_by_genre(keyword)

    from pprint import pprint
    pprint(playlists[:3])  # 결과 일부 출력