"""Detect five emotions using the Watson NLP service provided by the lab."""

import requests

SERVICE_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion; invalid input yields None."""
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty_result

    response = requests.post(
        SERVICE_URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers=HEADERS,
        timeout=30,
    )
    if response.status_code == 400:
        return empty_result
    response.raise_for_status()

    prediction = response.json()["emotionPredictions"][0]["emotion"]
    scores = {emotion: prediction[emotion] for emotion in EMOTIONS}
    scores["dominant_emotion"] = max(EMOTIONS, key=scores.__getitem__)
    return scores
