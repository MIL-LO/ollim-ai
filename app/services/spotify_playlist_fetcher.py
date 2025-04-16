from app.api.spotify_client import sp

def fetch_playlists_by_keyword(keyword: str, limit=50, offset=0):
    """
    특정 키워드(감정/분위기)로 플레이리스트 검색
    """
    result = sp.search(q=keyword, type='playlist', limit=limit, offset=offset)
    playlists = result.get('playlists', {}).get('items', [])
    return playlists

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


if __name__ == "__main__":
    playlist_id = "1Q2HVqrVB4t5YbV1WHCdgy"  # 예시 ID
    details = fetch_playlist_details(playlist_id)
    from pprint import pprint
    pprint(details)