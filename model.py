import io
from time import sleep
from threading import Thread, Condition
import numpy as np
import cv2
from utils import read_label_file, get_cap, get_person_fn


def gen():
    get_person = get_person_fn()
    cap = get_cap()
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = get_person(frame)
        output = cv2.imencode('.jpg', frame)[1].tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + output + b'\r\n')
