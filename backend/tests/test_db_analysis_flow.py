import importlib
import os

from fastapi.testclient import TestClient


def _client(tmp_path):
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    import main  # noqa: WPS433

    importlib.reload(main)
    return TestClient(main.app)


def test_create_and_list_victims_persisted(tmp_path):
    client = _client(tmp_path)
    create_resp = client.post("/api/v1/victims", json={"name": "Test User", "case_type": "trauma"})
    assert create_resp.status_code == 200
    victim_id = create_resp.json()["id"]

    detail = client.get(f"/api/v1/victims/{victim_id}")
    assert detail.status_code == 200
    assert detail.json()["name"] == "Test User"

    listing = client.get("/api/v1/victims")
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1


def test_analysis_and_voice_endpoint(tmp_path):
    client = _client(tmp_path)
    victim = client.post("/api/v1/victims", json={"name": "A", "case_type": "threat_case"}).json()
    victim_id = victim["id"]

    interaction = {
        "victim_id": victim_id,
        "message": "I feel scared and unsafe and someone threatened to kill me",
        "channel": "chatbot",
    }
    resp = client.post("/api/v1/interactions/text", json=interaction)
    assert resp.status_code == 200

    analysis = client.post(f"/api/v1/analysis/{victim_id}/analyze")
    assert analysis.status_code == 200
    body = analysis.json()
    assert "distress_score" in body
    assert body["analysis"]["threat_indicators"] > 0
    assert body["distress_score"]["risk_level"] in {"low", "medium", "high", "critical"}

    voice = client.post(
        f"/api/v1/voice-data?victim_id={victim_id}",
        files={"file": ("sample.wav", b"not-a-real-wave", "audio/wav")},
    )
    assert voice.status_code == 200
    assert "voice_stress_score" in voice.json()
