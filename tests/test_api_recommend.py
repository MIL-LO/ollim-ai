from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_recommend():
    response = client.post("/recommend", json={
      "user_id": "11111111-aaaa-bbbb-cccc-222222222222",
      "diary_id": "99999999-xxxx-yyyy-zzzz-888888888888",
      "content": "오늘은 친구들과 하루 종일 웃고 떠들면서 행복한 시간을 보냈어. 너무 기뻤어!",
      "persona": {
        "mbti": "ENFP",
        "age_group": "20대",
        "lifestyle": "사교적"
      }
    })
    assert response.status_code == 200
    assert "name" in response.json()