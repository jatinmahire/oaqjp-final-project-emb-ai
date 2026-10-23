"""Capture four assignment screenshots from real Watson predictions and tests.

Run from the project root in a lab where the Watson endpoint is reachable.
Dependencies: requests, Flask, pylint, playwright, and Playwright Chromium.
No prediction or test result is mocked by this script.
"""

import argparse
import html
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request


def execute(arguments, project):
    """Run a Python command and retain the actual output and return code."""
    completed = subprocess.run(
        [sys.executable, *arguments], cwd=project, capture_output=True,
        text=True, timeout=240, check=False,
    )
    command = f'{Path(sys.executable).name} ' + subprocess.list2cmdline(arguments)
    record = f'Working directory: {project}\n\nCommand:\n{command}\n\n'
    record += completed.stdout + completed.stderr
    record += f'\nProcess exit code: {completed.returncode}\n'
    if completed.returncode:
        raise RuntimeError(record)
    return record


def save_record(page, path, title, record):
    """Render an actual command transcript into a readable PNG."""
    document = '''<!doctype html><html><head><meta charset="utf-8">
    <style>
    body{padding:35px;margin:0;background:#edf2f7;color:#183149;font-family:Arial}
    main{background:white;border:1px solid #cad6e3;border-radius:12px;padding:30px}
    h1{font-size:25px;margin:0 0 20px}pre{white-space:pre-wrap;overflow-wrap:anywhere;
    background:#f5f8fc;padding:22px;border-radius:8px;font:18px/1.6 monospace}
    p{color:#526574;font-size:15px}</style></head><body><main>'''
    document += '<h1>' + html.escape(title) + '</h1><pre>'
    document += html.escape(record) + '</pre>'
    document += '<p>Actual executed command and captured output. No mocked predictions.</p></main></body></html>'
    page.set_content(document)
    page.screenshot(path=str(path), full_page=True)
    print('Saved:', path, flush=True)


def available_port():
    """Choose an unused local TCP port for the preview server."""
    with socket.socket() as connection:
        connection.bind(('127.0.0.1', 0))
        return connection.getsockname()[1]


def main():
    """Verify live results before producing the requested evidence files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='.', help='Project root containing server.py')
    parser.add_argument('--output', default='remaining_uploads', help='Destination directory')
    args = parser.parse_args()
    project = Path(args.project).resolve()
    output = Path(args.output).resolve()
    for name in ('server.py', 'test_emotion_detection.py', 'EmotionDetection/emotion_detection.py'):
        if not (project / name).is_file():
            raise RuntimeError(f'Missing {name}. Run from the emotion-detection project root.')

    from playwright.sync_api import sync_playwright

    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
        try:
            page = browser.new_page(viewport={'width':1440, 'height':1000})
            formatted = execute([
                '-c',
                'from emotion_detection import emotion_detector; '
                'result = emotion_detector("I am glad this happened"); '
                'print(result); '
                'assert set(result) == {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"}; '
                'assert all(isinstance(result[key], (int, float)) for key in ("anger", "disgust", "fear", "joy", "sadness")); '
                'assert result["dominant_emotion"] == "joy"',
            ], project)
            save_record(page, output / '3b_formatted_output_test.png',
                        'Formatted output: real Watson prediction', formatted)

            packaged = execute([
                '-c',
                'from EmotionDetection.emotion_detection import emotion_detector; '
                'result = emotion_detector("I am very angry"); '
                'print(result); '
                'assert set(result) == {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"}; '
                'assert all(isinstance(result[key], (int, float)) for key in ("anger", "disgust", "fear", "joy", "sadness")); '
                'assert result["dominant_emotion"] == "anger"',
            ], project)
            save_record(page, output / '4b_packaging_test.png',
                        'Package validation: real Watson prediction', packaged)

            tests = execute(['test_emotion_detection.py'], project)
            if 'Ran 5 tests' not in tests or '\nOK' not in tests:
                raise RuntimeError('The required five-test success summary was not found:\n' + tests)
            save_record(page, output / '5b_unit_testing_result.png',
                        'Five required live-service tests passed', tests)

            port = available_port()
            address = f'http://127.0.0.1:{port}'
            with tempfile.TemporaryFile() as log:
                server = subprocess.Popen(
                    [sys.executable, '-c',
                     f'from server import app; app.run(host="127.0.0.1", port={port})'],
                    cwd=project, stdout=log, stderr=log, env=os.environ.copy(),
                )
                try:
                    ready = False
                    for _ in range(50):
                        if server.poll() is not None:
                            break
                        try:
                            with urllib.request.urlopen(address, timeout=1):
                                ready = True
                                break
                        except OSError:
                            time.sleep(0.2)
                    if not ready:
                        log.seek(0)
                        raise RuntimeError('Preview server did not start:\n' + log.read().decode(errors='replace'))
                    page.goto(address)
                    page.locator('#textToAnalyze').fill('I am glad this happened')
                    page.get_by_role('button', name='Analyze emotions').click()
                    page.wait_for_function(
                        'document.querySelector("#system_response").textContent.includes("The dominant emotion is joy")',
                        timeout=65000,
                    )
                    result = page.locator('#system_response').inner_text()
                    if not all(emotion in result for emotion in ('anger', 'disgust', 'fear', 'joy', 'sadness')):
                        raise RuntimeError('The application did not display every required emotion score.')
                    page.screenshot(path=str(output / '6b_deployment_test.png'), full_page=True)
                    print('Saved:', output / '6b_deployment_test.png', flush=True)
                finally:
                    server.terminate()
                    server.wait(timeout=15)
        finally:
            browser.close()
    print('All four evidence images were captured from successful live-service runs.')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired, ImportError) as error:
        print('Capture stopped. Resolve the following problem and run again:\n' + str(error), file=sys.stderr)
        raise SystemExit(1) from error
