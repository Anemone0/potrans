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

reload(sys)
sys.setdefaultencoding("utf-8")


def mymemorytrans(source, _from, _to):
    burp0_url = "https://mymemory.translated.net:443/api/ajaxfetch?q={source}&langpair={from_lang}|{to_lang}&mtonly=1".format(
        source=source, from_lang=_from, to_lang=_to)
    burp0_headers = {
        "Connection": "close",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8,ja;q=0.7,zh-CN;q=0.6"}
    failed = True
    while failed:
        try:
            r = requests.get(burp0_url, headers=burp0_headers)
            failed = False
        except requests.exceptions.SSLError:
            sys.stderr.write('SSLError: Try again...\n')
            failed = True
        try:
            ret = json.loads(r.text)["responseData"]["translatedText"]
        except Exception as e:
            print e
            failed = True
    return ret


if __name__ == '__main__':
    #  print mymemorytrans("Hello, world!", "en-GB", "zh-CN")
    print mymemorytrans(sys.argv[1], sys.argv[2], sys.argv[3])
