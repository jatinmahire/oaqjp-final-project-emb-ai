# Final Project

## Project name
Emotion Detection with Watson NLP

This Flask application uses the Watson NLP emotion endpoint provided by the
Skills Network lab to detect anger, disgust, fear, joy, and sadness and identify
the dominant emotion. It handles blank input and upstream HTTP 400 responses.

## Run in the course lab

```bash
cd /home/project/final_project
python3 -m pip install -r requirements.txt
python3 test_emotion_detection.py
python3 -m pylint server.py
python3 server.py
```

Open the lab's application preview on port 5000. The Watson endpoint must be
reachable from the environment. Remote-service failures are not treated as
successful emotion predictions. Unit tests in test_emotion_detection.py use
the actual service; verification/test_contract.py uses mocks for local checks.

The repository should be a public fork of
https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai
and keep the exact repository name oaqjp-final-project-emb-ai.

## Assignment file links

- Question 1: [README.md](https://github.com/jatinmahire/oaqjp-final-project-emb-ai/blob/main/README.md)
- Question 6: [EmotionDetection/__init__.py](https://github.com/jatinmahire/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py)
- [Question-by-question submission guide](SUBMISSION_GUIDE.md)
- [Actual blank-input screenshot for Question 14](evidence/7c_error_handling_interface.png)

## Verification status

Eight local contract tests passed using mocked Watson responses. The final
server received a local Pylint score of 10.00/10. The five live-service tests
and successful-prediction screenshot still require a reachable Watson lab
endpoint. A successful prediction or deployment screenshot is not claimed.

The source history originates from the IBM starter repository. GitHub's fork
relationship must be verified separately to satisfy the assignment requirement.
