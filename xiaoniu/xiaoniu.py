# 导入requests模块
import json
import time

import requests
from urllib.parse import urlencode

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://niutrans.vip',
    'Referer': 'https://niutrans.vip/console/textTrans',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def get_millisecond_timestamp():
    return int(time.time() * 1000)


def load():
    base_url = "https://gcaptcha4.geetest.com/load"
    payload = {
        'callback': f'geetest_{get_millisecond_timestamp()}',
        'captcha_id': '93affd0ff28090db468c7fff1741b1f6',
        'client_type': 'web',
        'pt': '1',
        'lang': 'zho'
    }
    full_url = f"{base_url}?{urlencode(payload)}"
    response = requests.get(full_url, headers=headers)
    json_obj = json.loads(response.text[response.text.find('{'):response.text.rfind('}') + 1])
    return json_obj['data']


def verify():
    data = load()
    base_url = "https://gcaptcha4.geetest.com/verify"
    payload = {
        'callback': f'geetest_{get_millisecond_timestamp()}',
        'captcha_id': '93affd0ff28090db468c7fff1741b1f6',
        'client_type': 'web',
        'lot_number': data['lot_number'],
        'payload': data['payload'],
        'process_token': data['process_token'],
        'payload_protocol': 1,
        'pt': 1,
        'w': "",
    }

    full_url = f"{base_url}?{urlencode(payload)}"
    response = requests.get(full_url, headers=headers)
    json_obj = json.loads(response.text[response.text.find('{'):response.text.rfind('}') + 1])
    return json_obj['data']


# load请求获得lot_number，verify请求获得
def translate(from_lan, to_lan, text):
    data = verify()
    base_url = "https://test.niutrans.com/NiuTransServer/testaligntrans"
    payload = {
        'from': f'{from_lan}',
        'to': f'{to_lan}',
        'src_text': f"{text}",
        'source': 'text',
        'dictNo': '',
        'memoryNo': '',
        'isUseDict': '0',
        'isUseMemory': '0',
        'lot_number': data['seccode']['lot_number'],
        'captcha_output': data['seccode']['captcha_output'],
        'pass_token': data['seccode']['pass_token'],
        'gen_time': data['seccode']['gen_time'],
        'time': get_millisecond_timestamp()
    }
    full_url = f"{base_url}?{urlencode(payload)}"
    response = requests.get(full_url, headers=headers)
    print(response.text)


if __name__ == '__main__':
    text = '你好'
    translate('zh', 'en', text)
