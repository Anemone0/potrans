#!/usr/bin/env python
# coding=utf-8

# @file mymemorytrans.py
# @brief mymemorytrans
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2018-03-13 19:42

import sys
import requests
import json
import execjs

reload(sys)
sys.setdefaultencoding("utf-8")

with open('google_tk.js', "r") as f:
    _JS_CODE = "".join(f.readlines())

JS_LAUNCHER = execjs.compile(_JS_CODE.decode('utf8'))


def trans(source, _from, _to):
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080"}
    tk=JS_LAUNCHER.call('TK', source)
    burp0_url = "https://translate.google.co.jp:443/translate_a/single?client=t&sl={from_lang}&tl={to_lang}&hl={to_lang}&dt=t&ie=UTF-8&oe=UTF-8&source=btn&tk={tk}&q={source}".format(source=source, from_lang=_from, to_lang=_to, tk=tk)

    burp0_headers = {
        "Connection": "close",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "X-Chrome-UMA-Enabled": "1",
        "X-Client-Data": "CLK1yQEIkLbJAQimtskBCMS2yQEIqZ3KAQioo8oB",
        "Accept": "*/*",
        "Referer": "https://translate.google.co.jp/?hl=zh-CN&tab=wT",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8,ja;q=0.7,zh-CN;q=0.6"}

    failed = True
    while failed:
        try:
            r = requests.get(burp0_url, headers=burp0_headers, proxies=proxies)
            failed = False
        except requests.exceptions.SSLError:
            sys.stderr.write('SSLError: Try again...\n')
            failed = True
        print tk
        print r.status_code
        print r.text
    ret = json.loads(r.text.decode('utf8'))
    ret = ret[0][0][0]
    return ret


if __name__ == '__main__':
    #  print trans("Sensitive informations", "en-GB", "zh-CN")
    print trans(sys.argv[1], sys.argv[2], sys.argv[3])
