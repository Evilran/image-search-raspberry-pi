#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name: detect_image.py
Author: Evi1ran
Date Created: November 06, 2019
Description: None
'''

# built-in imports
import time

# third-party imports
from PIL import Image
from PIL import ImageDraw

import detect
import tflite_runtime.interpreter as tflite


EDGETPU_SHARED_LIB = 'libedgetpu.so.1'


def load_labels(path, encoding='utf-8'):
  """Loads labels from file (with or without index numbers).

  Args:
    path: path to label file.
    encoding: label file encoding.
  Returns:
    Dictionary mapping indices to labels.
  """
  with open(path, 'r', encoding=encoding) as f:
    lines = f.readlines()
    if not lines:
      return {}

    if lines[0].split(' ', maxsplit=1)[0].isdigit():
      pairs = [line.split(' ', maxsplit=1) for line in lines]
      return {int(index): label.strip() for index, label in pairs}
    else:
      return {index: line.strip() for index, line in enumerate(lines)}


def make_interpreter(model_file):
  model_file, *device = model_file.split('@')
  return tflite.Interpreter(
      model_path=model_file,
      experimental_delegates=[
          tflite.load_delegate(EDGETPU_SHARED_LIB,
                               {'device': device[0]} if device else {})
      ])


def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red')
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill='red')


def detect_image(path, filename):
  model = "models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
  labels = "models/coco_labels.txt"
  threshold = 0.4
  count = 5
  labels = load_labels(labels)
  interpreter = make_interpreter(model)
  interpreter.allocate_tensors()

  image = Image.open(path).convert('RGB')
  scale = detect.set_input(interpreter, image.size,
                           lambda size: image.resize(size, Image.ANTIALIAS))

  print('----INFERENCE TIME----')
  print('Note: The first inference is slow because it includes',
        'loading the model into Edge TPU memory.')
  for _ in range(count):
    start = time.monotonic()
    interpreter.invoke()
    inference_time = time.monotonic() - start
    objs = detect.get_output(interpreter, threshold, scale)
    print('%.2f ms' % (inference_time * 1000))

  result = []
  print('-------RESULTS--------')
  if not objs:
    print('No objects detected')

  for obj in objs:
    print(labels.get(obj.id, obj.id))
    print('  id:    ', obj.id)
    print('  score: ', obj.score)
    print('  bbox:  ', obj.bbox)
    img_processed = "static/output/" + filename
    result.append(labels.get(obj.id, obj.id))
    draw_objects(ImageDraw.Draw(image), objs, labels)
    image.save(img_processed)
    output = img_processed
  return result, output

