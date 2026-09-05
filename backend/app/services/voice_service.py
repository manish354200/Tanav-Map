"""Voice transcription and stress feature extraction."""

from __future__ import annotations

import os
import tempfile
from typing import Dict

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

try:
    import librosa
except Exception:  # pragma: no cover
    librosa = None


def transcribe_audio(file_path: str) -> str:
    """Transcribe speech with Whisper when available, else fallback."""
    try:
        import whisper  # type: ignore

        model_name = os.getenv("WHISPER_MODEL", "base")
        model = whisper.load_model(model_name)
        output = model.transcribe(file_path)
        return str(output.get("text", "")).strip()
    except Exception:
        return ""


def analyze_voice_stress(file_bytes: bytes, suffix: str = ".wav") -> Dict:
    """Extract stress indicators from pitch/tremor/speaking-rate proxies."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        path = tmp.name

    try:
        if librosa is None or np is None:
            return {"voice_stress_score": 50.0, "features": {"fallback": True}, "transcript": transcribe_audio(path)}
        try:
            y, sr = librosa.load(path, sr=16000, mono=True)
        except Exception:
            return {"voice_stress_score": 50.0, "features": {"invalid_audio": True}, "transcript": transcribe_audio(path)}
        if y.size == 0:
            return {"voice_stress_score": 50.0, "features": {"empty_audio": True}, "transcript": transcribe_audio(path)}

        pitch, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7"))
        valid_pitch = pitch[~np.isnan(pitch)] if pitch is not None else np.array([])
        pitch_std = float(np.std(valid_pitch)) if valid_pitch.size else 0.0
        rmse = librosa.feature.rms(y=y)[0]
        tremor_proxy = float(np.std(rmse))
        zero_cross = float(np.mean(librosa.feature.zero_crossing_rate(y)))

        pitch_score = min(100.0, pitch_std / 3.0)
        tremor_score = min(100.0, tremor_proxy * 1000.0)
        speech_rate_score = min(100.0, zero_cross * 700.0)
        voice_stress_score = round((0.5 * pitch_score) + (0.3 * tremor_score) + (0.2 * speech_rate_score), 2)

        return {
            "voice_stress_score": max(0.0, min(100.0, voice_stress_score)),
            "features": {
                "pitch_variability": round(pitch_std, 4),
                "tremor_proxy": round(tremor_proxy, 6),
                "speech_rate_proxy": round(zero_cross, 6),
            },
            "transcript": transcribe_audio(path),
        }
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
