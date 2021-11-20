#!/usr/bin/env python3

import logging
import traceback
import threading
import random
import string
import time
import os

from flask import Flask

log_file = os.getenv('LOG_DEST', '/dev/stdout')
format = '[%(levelname)s][%(asctime)s]: %(message)s'

app = Flask(__name__)
logging.basicConfig(format=format, filename=log_file, filemode='w', level=logging.DEBUG)

gstop = False

def random_logs():
    global gstop
    logging.info(f"Log from thread:{''.join(random.choice(string.ascii_lowercase) for _ in range(16))}")
    while not gstop:
        logging.info(f"Log from thread:{''.join(random.choice(string.ascii_lowercase) for _ in range(16))}")
        time.sleep(1)
    return

thread = threading.Thread(target=random_logs)

@app.route('/log/msg/<arg>')
def msg(arg):
    logging.info(f"Msg:{arg}")
    return f"Done"

@app.route('/log/start')
def start():
    global gstop
    gstop = False
    thread.start()
    return f"Started"

@app.route('/log/stop')
def stop():
    global gstop
    gstop = True
    thread.join()
    return f"Stopping"

@app.route('/log/excpetion')
def log_exception():
    try:
        raise ValueError('Let\'s log some excpetions')
    except ValueError as e:
        logging.info(f"Exception:\n {traceback.format_exc()}")
    return f"Logged exception to file"

if __name__ == '__main__':
    app.run()