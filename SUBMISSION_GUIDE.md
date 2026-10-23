# Answers and submission guide: all 16 questions

This assignment requires your own public fork and real execution evidence.
Code answers are supplied below and in answers/. Terminal logs must come from
actual successful runs. No Watson scores or passing live-service logs have been
invented. Do not submit examples, placeholders, or mocked local tests as proof
that the live Watson service ran successfully.


## What has already been checked locally

All eight mocked contract tests passed. Pylint rated the final server 10.00/10.
The actual Pylint output is in answers/8b_static_code_analysis.txt; it is a Windows
local run. You may paste that actual result for Question 16, or capture a fresh
lab run using the instructions below. For Question 14, the supplied
7c_error_handling_interface.png is an actual capture from the running Flask app
with blank input; it is ready to upload. It does not use a mocked prediction.

Questions 1 and 6 still require an actual public fork and pushed files.
Questions 3, 5, 7, and 9 still require live Watson output from your lab.
Question 11 still requires the real successful-prediction screenshot.

## Prepare the repository and lab

1. Sign in as jatinmahire. Fork the ORIGINAL repository using GitHub's Fork
   button: https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai
2. Keep the repository PUBLIC and named exactly oaqjp-final-project-emb-ai.
   A standalone uploaded repository is not a substitute for the requested fork.
3. In the Skills Network lab, clone YOUR fork into /home/project/final_project.
   If that folder already exists, inspect it first and use the existing checkout;
   do not overwrite unrelated work. Copy this package's project files into the
   checkout, retaining the original LICENSE and .git history.
4. Install dependencies in the lab:

```bash
cd /home/project/final_project
python3 -m pip install -r requirements.txt
mkdir -p evidence
```

After collecting the evidence and restoring the final source as directed below,
commit and push your changes to YOUR fork. Confirm the branch is main, the
repository is public, and both file links open while signed out.

## Question 1 - README URL

After pushing your public fork, enter this URL (a template until it exists):
https://github.com/jatinmahire/oaqjp-final-project-emb-ai/blob/main/README.md

The supplied README begins with # Final Project and includes project name details.

## Question 2 - Initial application code

Paste the complete contents of answers/2a_emotion_detection.txt.
This stage returns the original Watson response, before output formatting.

## Question 3 - Initial application execution output

In the lab, temporarily install the stage-2 module at the root:

```bash
cp answers/2a_emotion_detection.txt emotion_detection.py
cp test_emotion_detection.py evidence/final_unit_tests.py
cat > test_emotion_detection.py <<'PY'
import json
import unittest
from emotion_detection import emotion_detector

class TestInitialApplication(unittest.TestCase):
    def test_response(self):
        result = json.loads(emotion_detector('I am really mad about this'))
        self.assertIn('emotionPredictions', result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
PY
```

Record an ACTUAL interactive session using the Linux script utility:

```bash
script -q -e evidence/2b_application_creation.txt
```

Inside the recorded shell, type the following. The lines beginning with >>>
are Python input; do not type the >>> characters themselves. Use the shell
prompt exactly as set below so the required directory appears in the transcript.

```text
cd /home/project/final_project
export PS1='/home/project/final_project $ '
pwd
python3
>>> from emotion_detection import emotion_detector
>>> print(emotion_detector('I am really mad about this'))
>>> exit()
python3 test_emotion_detection.py
exit
```

Paste the entire successful transcript from evidence/2b_application_creation.txt.
Do not paste these instructions instead of the actual output. A network failure
must be fixed in the lab before this question is ready to submit.

## Question 4 - Formatted application code

Paste answers/3a_output_formatting.txt. Then update the root module:

```bash
cp answers/3a_output_formatting.txt emotion_detection.py
```

## Question 5 - Formatted output evidence

Record another session:

```bash
script -q -e evidence/3b_formatted_output_test.txt
```

Inside it run:

```bash
cd /home/project/final_project
export PS1='/home/project/final_project $ '
python3 -c "from emotion_detection import emotion_detector; print(emotion_detector('I am glad this happened'))"
exit
```

Paste the real transcript. It must show a dictionary with anger, disgust, fear,
joy, sadness, and dominant_emotion. Scores are determined by the real model;
do not replace them with guessed numbers.

## Question 6 - Package initializer URL

After pushing your public fork, enter this URL (a template until it exists):
https://github.com/jatinmahire/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py

The supplied initializer imports the module and exposes emotion_detector.

## Question 7 - Packaging execution evidence

Record evidence/4b_packaging_test.txt with script as above. Inside the recording,
run these exact commands, then exit the recording shell:

```bash
cd /home/project/final_project
export PS1='/home/project/final_project $ '
python3 -c "from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector('I am very angry'))"
exit
```

Paste the real transcript including the command and output. Check that it
contains all five emotion scores and 'dominant_emotion': 'anger'.

## Question 8 - Unit-test code

Paste answers/5a_unit_testing.txt. It tests the five required emotion examples.
Restore that test file and the final root import before the next step:

```bash
cp answers/5a_unit_testing.txt test_emotion_detection.py
cat > emotion_detection.py <<'PY'
"""Retain the root-level import used in the early assignment tasks."""
from EmotionDetection.emotion_detection import emotion_detector
__all__ = ["emotion_detector"]
PY
```

## Question 9 - Passing unit-test output

Record evidence/5b_unit_testing_result.txt. Inside the recorded shell, run:

```bash
cd /home/project/final_project
export PS1='/home/project/final_project $ '
python3 test_emotion_detection.py
exit
```

Paste the actual result. All five live-service tests must pass and the report
must end in OK. Local mocked contract tests are separate verification and are
not the answer to this question.

## Question 10 - Flask deployment code

Paste answers/6a_server.txt. It serves the input page and the /emotionDetector
endpoint, and displays all five scores plus the dominant emotion.

## Question 11 - Successful application screenshot

Run the final application with python3 server.py and open the lab's application
preview on port 5000. Enter "I am glad this happened" and click Analyze emotions.
Once a REAL Watson result appears, capture a screenshot showing the input and
the result with dominant emotion joy. Save it as 6b_deployment_test.png and upload
that screenshot. Do not submit an error page, a generated illustration, or a
page whose success result was mocked.

## Question 12 - HTTP 400 error-handling function

Paste answers/7a_error_handling_function.txt. It explicitly returns None for all
five emotion scores and dominant_emotion when Watson returns HTTP 400. It also
handles blank and whitespace-only text locally.

## Question 13 - Blank-input server handling

Paste answers/7b_error_handling_server.txt. Blank input and an invalid model
response display exactly: Invalid text! Please try again!
Upstream service failures display a distinct service-unavailable message.

## Question 14 - Error-handling screenshot

With python3 server.py running, leave the input blank and click Analyze emotions.
Capture the empty field and the visible "Invalid text! Please try again!" result.
Save as 7c_error_handling_interface.png and upload. Whitespace-only input is
handled as invalid too.

## Question 15 - Server after static-analysis improvements

Paste answers/8a_server_modified.txt. It contains module and function docstrings,
clear names, readable formatting, and the final error-handling implementation.
The static-analysis command is run in the terminal, not placed in server.py.

## Question 16 - Real Pylint output

Record evidence/8b_static_code_analysis.txt. Inside the recorded shell, run:

```bash
cd /home/project/final_project
export PS1='/home/project/final_project $ '
python3 -m pylint server.py
exit
```

Paste the actual output, including the score. Address any remaining messages
and rerun if needed. Do not edit the output to claim a higher score.

## Sources and verification boundaries

Original starter repository:
https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai
IBM Watson emotion documentation:
https://www.ibm.com/docs/en/watson-libraries?topic=catalog-emotion

The implementation was written for these task requirements. The question file
requires an actual fork, actual terminal output, and actual screenshots. The
guide covers all 16 questions, but URL templates and capture instructions are
not substitutes for completing the corresponding actions.


## Question 2 code

```python
"""Call the lab's Watson NLP emotion detection service."""

import requests


def emotion_detector(text_to_analyze):
    """Return the unformatted Watson emotion response as a JSON string."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text
```


## Question 4 code

```python
"""Format the Watson NLP emotion detection result."""

import requests


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the emotion with the highest score."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    response = requests.post(
        url, json={"raw_document": {"text": text_to_analyze}},
        headers=headers, timeout=30,
    )
    response.raise_for_status()
    emotions = response.json()["emotionPredictions"][0]["emotion"]
    names = ("anger", "disgust", "fear", "joy", "sadness")
    scores = {name: emotions[name] for name in names}
    scores["dominant_emotion"] = max(names, key=scores.__getitem__)
    return scores
```


## Question 6 initializer code

```python
"""Expose the emotion detection module and function as a package."""

from . import emotion_detection
from .emotion_detection import emotion_detector

__all__ = ["emotion_detection", "emotion_detector"]
```


## Question 8 code

```python
"""Test the five required example sentences against the live Watson service."""

import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Verify dominant emotions and the required output keys."""

    def check_emotion(self, text, expected):
        """Check the response structure and expected dominant emotion."""
        result = emotion_detector(text)
        self.assertEqual(
            set(result),
            {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"},
        )
        self.assertEqual(result["dominant_emotion"], expected)

    def test_joy(self):
        """Recognize joy."""
        self.check_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Recognize anger."""
        self.check_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Recognize disgust."""
        self.check_emotion("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """Recognize sadness."""
        self.check_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Recognize fear."""
        self.check_emotion("I am really afraid that this will happen", "fear")


if __name__ == "__main__":
    unittest.main(verbosity=2)
```


## Question 10 code

```python
"""Deploy the emotion detection application using Flask."""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Display the application form."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    """Analyze text and display all five scores and the dominant emotion."""
    result = emotion_detector(request.args.get("textToAnalyze", ""))
    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```


## Question 12 code

```python
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
```


## Question 13 code

```python
"""Serve the Watson NLP emotion detection application with Flask."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Display the application input form."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    """Analyze input and return the result or an actionable error message."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    try:
        result = emotion_detector(text_to_analyze)
    except (RequestException, KeyError, IndexError, TypeError, ValueError):
        app.logger.exception("Watson emotion analysis failed")
        return "Emotion service unavailable. Please try again later.", 503

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```


## Question 15 code

```python
"""Serve the Watson NLP emotion detection application with Flask."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Display the application input form."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    """Analyze input and return the result or an actionable error message."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    try:
        result = emotion_detector(text_to_analyze)
    except (RequestException, KeyError, IndexError, TypeError, ValueError):
        app.logger.exception("Watson emotion analysis failed")
        return "Emotion service unavailable. Please try again later.", 503

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```


## Question 16 - Actual local Pylint result

```text
Actual local static-analysis run (Windows; not a Skills Network lab transcript)

Working directory:
D:\DS CP\DS pro\DS pro\output\emotion_assignment\oaqjp-final-project-emb-ai

Command executed:
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pylint server.py

Dependency directory supplied through PYTHONPATH:
D:\DS CP\DS pro\DS pro\tmp\emotion-deps

Actual output:
------------------------------------
Your code has been rated at 10.00/10

Process exit code: 0

```
