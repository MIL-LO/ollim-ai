import unittest
from unittest.mock import patch, MagicMock
from app.services.spotify_playlist_fetcher import fetch_playlists_by_keyword, fetch_playlist_details

class TestSpotifyPlaylistFetcher(unittest.TestCase):

    @patch("app.services.spotify_playlist_fetcher.sp")
    def test_fetch_playlists_by_keyword(self, mock_sp):
        mock_sp.search.return_value = {
            "playlists": {
                "items": [
                    {"id": "123", "name": "Test Playlist"},
                    {"id": "456", "name": "Another Playlist"}
                ]
            }
        }

        result = fetch_playlists_by_keyword("기쁨")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "123")

    @patch("app.services.spotify_playlist_fetcher.sp")
    def test_fetch_playlist_details(self, mock_sp):
        mock_sp.playlist.return_value = {
            "id": "123",
            "name": "Test Playlist",
            "description": "Test Description",
            "images": [{"url": "http://example.com/image.jpg", "width": 300, "height": 300}],
            "owner": {"id": "owner123", "display_name": "Owner Name"},
            "followers": {"total": 100},
            "tracks": {"items": [{"track": {"name": "Song A"}}, {"track": {"name": "Song B"}}]}
        }

        result = fetch_playlist_details("123")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], "123")
        self.assertEqual(result["name"], "Test Playlist")
        self.assertEqual(result["followers"], 100)

if __name__ == "__main__":
    unittest.main()
