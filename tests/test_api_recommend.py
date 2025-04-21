from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recommend():
    response = client.post("/recommend", json={
        "user_id": "test",
        "diary_id": "test",
        "content": "오늘 하루는 우울했지만 친구 덕분에 괜찮아졌어.",
        "persona": {
            "mbti": "INFP",
            "age_group": "20대",
            "lifestyle": "감성적"
        }
    })
    assert response.status_code == 200
    assert "name" in response.json()