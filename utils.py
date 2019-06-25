import os
import numpy as np
import cv2
from edgetpu.detection.engine import DetectionEngine
from PIL import Image

# label = '/Downloads/coco_labels.txt'
# labels = read_label_file(label)
# model = '/Downloads/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'


def get_cap():
    video_source = os.environ.get('VIDEO_SOURCE')
    video_source = 'rtsp://192.168.22.28:8554/live.sdp'
    # video_source = 'rtsp://192.168.22.37:8554/unicast'
    return cv2.VideoCapture(video_source)


def read_label_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret


def get_person_fn():
    model = '/Downloads/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite'
    engine = DetectionEngine(model)

    def inference(frame):
        ans = engine.DetectWithImage(
            Image.fromarray(frame),
            threshold=0.1,
            top_k=10
        )
        ans = filter(lambda x: x.label_id == 0, ans)

        height, width = frame.shape[:2]
        one_column = width // 12
        person = np.zeros((height, one_column * 4, 3), dtype=np.uint8)
        for obj in ans:
            box = obj.bounding_box
            box = box * np.array([width, height])
            box = box.astype(np.int32)
            person = frame[box[0][1]:box[1][1], box[0][0]:box[1][0]]
            person = cv2.resize(person, (one_column * 4, height))
        return np.concatenate((frame, person), axis=1)

    return inference
