import io
import numpy as np
import os
import cv2
from PIL import Image
from PIL import ImageDraw
from utils import read_label_file, get_cap

from edgetpu.basic.basic_engine import BasicEngine


home = os.environ.get('HOME')
model = '{}/Downloads/open_pose_edgetpu.tflite'.format(
    home)
label = '{}/Downloads/coco_labels.txt'.format(home)


def gen():
    engine = BasicEngine(model)
    labels = read_label_file(label)
    cap = get_cap()

    # a = engine.get_num_of_output_tensors()
    # b = engine.total_output_array_size()
    # c = engine.get_output_tensor_size(0)
    # d = engine.required_input_array_size()

    # print(a, b, c, d)

    while True:
        _, frame = cap.read()
        input_val = cv2.resize(frame, (432, 368))
        input_val = input_val.flatten()
        ans = engine.RunInference(input_val)
        heat_map = ans[1].reshape([54, 46, 57])
        prop = heat_map[1, :, :]
        prop = np.multiply(prop, 255)
        # prop = cv2.resize(prop, (460, 640))
        _, buffer = cv2.imencode(".jpg", prop)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               io.BytesIO(buffer).read() + b'\r\n')


if __name__ == "__main__":
    gen()
