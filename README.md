# image-search-raspberry-pi

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/) [![Flask](https://img.shields.io/badge/flask-v1.1.1-blue)](https://pypi.org/project/Flask/) [![License](https://img.shields.io/github/license/Evilran/image-search-raspberry-pi)](https://github.com/Evilran/image-search-raspberry-pi/blob/master/LICENSE)

This is an online image search platform running on the Raspberry Pi via Object detection through Tensorflow lite.

- [x] Search image via URL link
- [x] Search image via upload an image
- [ ] Search similar images

Requirements
------------------------------------------------------------------

- numpy==1.16.2
- Flask>=1.0.0
- requests==2.22.0
- Pillow>=6.2.0
- Google Edge TPU or Tensorflow Lite ([Follow the instructions here](https://www.tensorflow.org/lite/guide/build_rpi))

Usage
---

It uses the **flask** in python, just one command to run the web server simply:

```
$ python3 server.py
```

Then visit the website: **127.0.0.1:5000** (port 5000 on the Raspberry Pi).



Here‘s screenshots of running on the Raspberry Pi 3B+ with Coral USB Accelerator:

![image](https://github.com/Evilran/image-search-raspberry-pi/blob/master/images/url.png)

![image](https://github.com/Evilran/image-search-raspberry-pi/blob/master/images/image.png)

![image](https://github.com/Evilran/image-search-raspberry-pi/blob/master/images/demo.gif)



## How does image search work on the Raspberry Pi?

- [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) 

- [Coral USB Accelerator](https://coral.withgoogle.com/products/accelerator) (Optional)

***Important Things***：This program does not have to use the Coral USB Accelerator, but I used it for accelerating the inference process in Tensorflow lite.

Thanks for [object detection](https://github.com/google-coral/tflite/tree/master/python/examples/detection) source code in the coral example, this image search platform is based on this. I used the *MobileNet SSD v2 (COCO)* model by default, you can modify it in the file `detect_image.py` .

If you don't have a usb accelerator, you can compile the entire Tensorflow lite on the Raspberry Pi and learn about its object detection [here](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi).

