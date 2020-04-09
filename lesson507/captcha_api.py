#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/29 11:27
# @Author  : tanxw
# @Desc    ：完整的9kw api 处理验证码服务

import sys
import re
import urllib.parse
import urllib.request
import time
import base64
from io import BytesIO
from PIL import Image
from lesson507.form import register


def main(api_key, filename):
    captcha = CaptchaAPI(api_key)
    print(register('lily', 'lem', 'lily@webscraping.com', 'a123456', captcha.solve))


class CaptchaError(Exception):
    pass


class CaptchaAPI:
    def __init__(self, api_key, timeout=60):
        self.api_key = api_key
        self.timeout = timeout
        self.url = 'https://www.9kw.eu/index.cgi'


    def solve(self, img):
        """Submit CAPTCHA and return result when ready
        """
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_data = img_buffer.getvalue()
        captcha_id = self.send(img_data)
        start_time = time.time()
        while time.time() < start_time + self.timeout:
            try:
                text = self.get(captcha_id)
            except CaptchaError:
                pass # CAPTCHA still not ready
            else:
                if text != 'NO DATA':
                    if text == 'ERROR NO USER':
                        raise CaptchaError('Error: no user available to solve CAPTCHA')
                    else:
                        print('CAPTCHA solved!')
                        return text
            print('Waiting for CAPTCHA ...')
        raise CaptchaError('Error: API timeout')


    def send(self, img_data):
        """Send CAPTCHA for solving
        """
        print('Submitting CAPTCHA')
        data = {
            'action': 'usercaptchaupload',
            'apikey': self.api_key,
            'file-upload-01': base64.b64encode(img_data),
            'base64': '1',
            'selfsolve': '1',
            'maxtimeout': str(self.timeout)
        }
        encoded_data = urllib.parse.urlencode(data).encode(encoding='utf8')
        request = urllib.request.Request(self.url, encoded_data)
        response = urllib.request.urlopen(request)
        result = response.read()
        self.check(result.decode('utf8'))
        return result


    def get(self, captcha_id):
        """Get result of solved CAPTCHA
        """
        data = {
            'action': 'usercaptchacorrectdata',
            'id': captcha_id,
            'apikey': self.api_key,
            'info': '1'
        }
        encoded_data = urllib.parse.urlencode(data).encode(encoding='utf8')
        response = urllib.parse.urlopen(self.url + '?' + encoded_data)
        result = response.read()
        self.check(result.decode('utf8'))
        return result


    def check(self, result):
        """Check result of API and raise error if error code detected
        """
        if re.match('00\d\d \w+', result):
            raise CaptchaError('API error: ' + result)



if __name__ == '__main__':
    # try:
    #     api_key = 'HW1JG0M5A5OJY67VCR'
    #     filename = 'samples/sample2.png'
    # except IndexError:
    #     print('Usage: %s <API key> <Image filename>' % sys.argv[0])
    # else:
    #     main(api_key, filename)

    api_key = 'HW1JG0M5A5OJY67VCR'
    captcha = CaptchaAPI(api_key)
    # img = Image.open('samples/sample2.png')
    # text = captcha.solve(img)
    register('lily', 'lem', 'lily@webscraping.com', 'a123456', captcha.solve)