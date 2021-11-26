#!/usr/bin/env python3
import os

from flask import Flask

app = Flask(__name__)

@app.route('/healthz')
def health():
    if "FAIL_HEALTH" in os.environ:
        return "Not OK!", 400
    return f"OK"

@app.route('/livez')
def start():
    if "FAIL_LIVE" in os.environ:
        return "Not OK!", 400
    return f"OK"

if __name__ == '__main__':
    app.run()