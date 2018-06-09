#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zjhch123
# @Date:   2018-02-12 21:08:34
# @Last Modified time: 2018-02-12 21:14:48

import re
import urllib2
import json
import sys
from xml.etree import ElementTree as ET
from urllib import urlencode, quote

# Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
reload(sys)
sys.setdefaultencoding('utf-8')

# 百度翻译，支持中文⇌英文
def trans(word):
    word = word.lower()
    request = urllib2.Request('http://fanyi.baidu.com/sug?' + urlencode({'kw': word}))
    request.add_header("Host", "fanyi.baidu.com")
    result = json.load(urllib2.urlopen(request))

    # pull request https://github.com/zjhch123/Alfred-Workflow-baidu-translate/pull/1
    if re.search('[\u4e00-\u9fa5]', word):
        lan = '#en/zh'
    else:
        lan = '#zh/en'
        
    translated = result.get('data')
    items = []
    if translated:
        for item in translated:
            items.append({
                'title': unicode(item.get('k').strip(',')),
                'subtitle': unicode(item.get('v').strip(',')),
                'arg': 'http://fanyi.baidu.com/%s/%s' % (lan, unicode(item.get('k'))),
                'icon': 'icon.jpg'
            })
    else:
        items.append({
            'title': u'百度翻译 ' + unicode(word),
            'arg': 'http://fanyi.baidu.com/%s/%s' % (lan, quote(word)),
            'icon': 'icon.jpg'
        })        

    return generate_xml(items)

def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key in ('arg',):
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)


# print(unicode(trans('china')))
# print(unicode(trans('你好')))
