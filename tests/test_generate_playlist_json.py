import unittest
from unittest.mock import patch
from app.services import spotify_playlist_fetcher

class TestGeneratePlaylistJson(unittest.TestCase):

    @patch("app.services.spotify_playlist_fetcher.fetch_playlist_details")
    @patch("app.services.spotify_playlist_fetcher.fetch_playlists_by_genre")
    def test_flattened_playlist_generation(self, mock_search, mock_details):
        # Mock playlist search result
        mock_search.return_value = [{"id": "test_id", "name": "Test Playlist"}]

        # Mock playlist details
        mock_details.return_value = {
            "id": "test_id",
            "name": "Test Playlist",
            "description": "Test Description",
            "image_url": "http://test.image",
            "image_width": 300,
            "image_height": 300,
            "owner_id": "owner123",
            "owner_name": "Test Owner",
            "followers": 100,
            "tracks": [{"track": {"name": "Song 1"}}, {"track": {"name": "Song 2"}}]
        }

        # Simulate generation logic
        keywords = ["테스트"]
        flattened_data = []

        for kw in keywords:
            playlists = spotify_playlist_fetcher.fetch_playlists_by_genre(kw, limit=1)
            for pl in playlists:
                detail = spotify_playlist_fetcher.fetch_playlist_details(pl["id"])
                track_names = [t["track"]["name"] for t in detail.get("tracks", []) if "track" in t]
                flattened_data.append({
                    "id": detail["id"],
                    "name": detail.get("name", ""),
                    "description": detail.get("description", ""),
                    "image_url": detail.get("image_url", ""),
                    "image_width": detail.get("image_width", 0),
                    "image_height": detail.get("image_height", 0),
                    "owner_id": detail.get("owner_id", ""),
                    "owner_name": detail.get("owner_name", ""),
                    "followers": detail.get("followers", 0),
                    "track_summary": ", ".join(track_names)
                })

        # Assert structure
        self.assertEqual(len(flattened_data), 1)
        self.assertEqual(flattened_data[0]["id"], "test_id")
        self.assertIn("Song 1", flattened_data[0]["track_summary"])

if __name__ == '__main__':
    unittest.main()
