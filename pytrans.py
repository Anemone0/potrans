#!/usr/bin/env python
# coding:utf-8
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <terry.yinzhe@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return to Terry Yin.
#
# Now google has stop providing free translation API. So I have to switch to
# http://mymemory.translated.net/, which has a limit for 1000 words/day free
# usage.
#
# The original idea of this is borrowed from <mort.yao@gmail.com>'s brilliant work
#    https://github.com/soimort/google-translate-cli
# ----------------------------------------------------------------------------
'''
This is a simple, yet powerful command line translator with google translate
behind it. You can also use it as a Python module in your code.
'''
import re
import json
from textwrap import wrap
import mymemorytrans
try:
    import urllib2 as request
    from urllib import quote
except BaseException:
    from urllib import request
    from urllib.parse import quote


class Translator:
    def __init__(self, to_lang, from_lang='en', email=None):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.email = email
        print self.email

    def translate(self, source):
        if self.from_lang == self.to_lang:
            return source
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        ret = []
        for s in self.source_list:
            ret.append(self._get_translation_from_google(s))
        return ' '.join(ret)

    def _get_translation_from_google(self, source):
        escaped_source = quote(source, '')
        return mymemorytrans.mymemorytrans(source, self.from_lang, self.to_lang)
        # ret=None
        # while ret==None:
        #     json5 = self._get_json5_from_google(source)
        #     ret=json.loads(json5)['responseData']['translatedText']
        # return ret

    def _get_json5_from_google(self, source):

        escaped_source = quote(source, '')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        if self.email:
            req = request.Request(
                url="http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s&de=%s" %
                (escaped_source, self.from_lang, self.to_lang, self.email), headers=headers)

        else:
            req = request.Request(
                url="http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s" %
                (escaped_source, self.from_lang, self.to_lang), headers=headers)
            # url="http://translate.google.com/translate_a/t?clien#t=p&ie=UTF-8&oe=UTF-8"
            #     +"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
            #     , headers = headers)
        r = request.urlopen(req)
        print r.getcode()
        return r.read().decode('utf-8')


__author__ = "Lingfeng Ai"
"""
使用google翻译自动翻译.po文件到指定语言
"""
import sys
import os
import argparse


def getOriginal(line, key="\"", default=None):
    "获取需要翻译的英文原文"
    line = line.strip("\n")
    subPart = line[line.find(key) + 1:len(line) - 1]
    return subPart


def TargetText(translator, original):
    return "\"" + translator.translate(original) + "\"" + "\n"


def main(defvals=None):
    isnewOne = False
    sentence = ""
    count = 0.0
    parser = argparse.ArgumentParser()

    if defvals is None:
        defvals = {'f': 'Cura.po', 't': 'ita', 'e': None}

    parser.add_argument(
        '-f',
        '--from',
        dest='from_file',
        type=str,
        default=defvals['f'],
        help='From language (e.g. zh, zh-TW, en, ja, ko). Default is ' +
        defvals['f'] +
        '.')
    parser.add_argument(
        '-t',
        '--to',
        dest='to_lang',
        type=str,
        default=defvals['t'],
        help='To language (e.g. zh, zh-TW, en, ja, ko). Default is ' +
        defvals['t'] +
        '.')

    parser.add_argument(
        '-e',
        '--email',
        dest='email',
        type=str,
        default=defvals['e'],
        help='To language (e.g. zh, zh-TW, en, ja, ko). Default is ' +
        "None" +
        '.')

    args = parser.parse_args()

    translator = Translator(to_lang=args.to_lang, email=args.email)

    output_path = os.path.abspath('.') + "/" + args.to_lang  # 创建目标文件的位置

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    output_filename=os.path.split(args.from_file)[1].split('.')[0]
    with open(os.path.join(output_path, output_filename + ".po"), 'w+') as out_file:
        with open(args.from_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                count += 1
                if line.startswith("#"):
                    isnewOne = True
                    out_file.write(line)
                    sentence = ""
                elif line.startswith("msgid"):
                    sentence += getOriginal(line)
                    out_file.write(line)
                elif line.startswith("\""):
                    if isnewOne:
                        sentence += getOriginal(line)
                        out_file.write(line)
                    else:
                        sentence += getOriginal(line)
                        out_file.write(line)
                elif line.startswith("    "):
                    sentence += getOriginal(line)
                    out_file.write(line)
                elif line.startswith("msgstr"):  # 只有在msgstr行才进行翻译
                    targetText = TargetText(
                        translator, sentence.replace(
                            "\\n", " "))
                    if targetText.startswith("MYMEMORY WARNING"):
                        print u"可用翻译词汇限额已经用完（1000/天），请添加email变量为个人邮箱，获取10000/天限额"
                        break
                        print targetText
                    else:
                        out_file.write("msgstr " + targetText.encode('utf-8'))
                    sentence = ""
                    isnewOne = False

                else:
                    out_file.write(line)
                sys.stdout.write(
                    "\r" +
                    u"翻译进度：%3.2f%%" %
                    float(
                        count /
                        len(lines) *
                        100))


if __name__ == '__main__':
    main()
