#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name: server.py
Author: Evi1ran
Date Created: November 06, 2019
Description: None
'''

# built-in imports
import os
import re
import requests

# third-party imports
from flask import Flask
from flask import request
from flask import render_template
from detect_image import detect_image

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg'])
UPLOAD_FOLDER=r'./cache/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/url', methods=['GET', 'POST'])
def url():
    if request.method == 'POST':
        url = request.form['url']
        if re.match(r'^https?:/{2}\w.+$', url): 
            if allowed_file(url):
                filename = url.split('/')[-1]
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
                r = requests.get(url)
                if r.status_code == 200:
                    c = r.content
                    if not c.startswith(b'<!DOCTYPE html>'):
                        with open(path, 'wb') as f:
                            f.write(c) 
                        result, output = detect_image(path, filename)
                        return render_template('index.html', result = result, output = output)
                    else:
                        return render_template('index.html', alert = 'URL does not seem to be an image!')
                else:
                    return render_template('index.html', alert = 'URL is not accessible!')
            else:
                return render_template('index.html', alert = 'URL is not an image!')
        else:
            return render_template('index.html', alert = 'Wrong URL format!')

    else:
        return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            result, output = detect_image(path, file.filename)
            return render_template('index.html', result = result,  output = output)
        else:
            return render_template('index.html', alert = 'File is not an image!')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()