"""Local contract tests with mocked Watson responses, not live-service evidence."""

import unittest
from unittest.mock import Mock, patch
from requests.exceptions import HTTPError

from EmotionDetection.emotion_detection import emotion_detector, EMOTIONS
from server import app


class ContractTests(unittest.TestCase):
    """Exercise extraction, errors, routes, and HTML rendering."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_extracts_scores_and_dominant_emotion(self, post):
        values = dict(zip(EMOTIONS, (0.8, 0.1, 0.02, 0.01, 0.07)))
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {"emotionPredictions": [{"emotion": values}]}
        result = emotion_detector("Example input")
        self.assertEqual(result, {**values, "dominant_emotion": "anger"})
        self.assertEqual(post.call_args.kwargs["json"], {"raw_document": {"text": "Example input"}})
        self.assertEqual(post.call_args.kwargs["timeout"], 30)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_produces_all_none(self, post):
        post.return_value.status_code = 400
        self.assertEqual(emotion_detector("invalid"), dict.fromkeys((*EMOTIONS, "dominant_emotion")))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_skips_network(self, post):
        for text in ("", "   ", None):
            with self.subTest(text=text):
                self.assertIsNone(emotion_detector(text)["dominant_emotion"])
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_non_400_failure_is_not_a_prediction(self, post):
        post.return_value = Mock(status_code=503)
        post.return_value.raise_for_status.side_effect = HTTPError("unavailable")
        with self.assertRaises(HTTPError):
            emotion_detector("Valid input")

    def test_input_form_is_served(self):
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="textToAnalyze"', response.data)

    @patch("server.emotion_detector")
    def test_blank_interface_message(self, detector):
        response = app.test_client().get("/emotionDetector?textToAnalyze=%20%20")
        self.assertEqual(response.data.decode(), "Invalid text! Please try again!")
        detector.assert_not_called()

    @patch("server.emotion_detector")
    def test_success_interface_contains_all_scores(self, detector):
        detector.return_value = {**dict.fromkeys(EMOTIONS, 0.1), "dominant_emotion": "joy"}
        response = app.test_client().get("/emotionDetector?textToAnalyze=Hello")
        for emotion in EMOTIONS:
            self.assertIn(emotion.encode(), response.data)
        self.assertIn(b"The dominant emotion is joy", response.data)

    @patch("server.emotion_detector")
    def test_upstream_http_400_interface(self, detector):
        detector.return_value = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
        response = app.test_client().get("/emotionDetector?textToAnalyze=Invalid")
        self.assertEqual(response.data.decode(), "Invalid text! Please try again!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
