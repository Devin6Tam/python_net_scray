#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/29 0:23
# @Author  : tanxw

import csv
import string
from PIL import Image
import pytesseract
from lesson507.form import register

# pip install pytesseract
# 还需要安装tesseract,安装包：https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200223.exe
# 环境变量修改 Path 加入C:\Program Files\Tesseract-OCR

# 安装pytesseract目录下，修改pytesseract.py
# tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
REGISTER_URL = 'http://example.webscraping.com/places/default/user/register'


def main():
    print(register('jacky', 'chen', 'jacky@webscraping.com', 'a123456', ocr))


def ocr(img):
    # threshold the image to ignore background and keep text
    gray = img.convert('L')
    gray.save('captcha_greyscale.png')
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    bw.save('captcha_threshold.png')
    word = pytesseract.image_to_string(bw)
    ascii_word = ''.join(c for c in word if c in string.ascii_lowercase).lower()
    return ascii_word


def test_samples():
    """Test accuracy of OCR on samples images
    """
    correct = total = 0
    for filename, text in csv.reader(open('samples/samples.csv')):
        img = Image.open('samples/' + filename)
        if ocr(img) == text:
            correct += 1
        total += 1
    print('Accuracy: %d/%d' % (correct, total))


if __name__ == '__main__':
    main()
