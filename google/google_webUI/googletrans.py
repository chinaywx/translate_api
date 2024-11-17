import requests
import re
# 此版本由于缺少一个key,导致它的某些翻译会特别差,有时间再逆向
def translate_sync(text, target_language, timeout=60):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    }

    url = "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2609060161424095358&bl=boq_translate-webserver_20201203.07_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=359373&rt=c"
    
    from_data = {
        "f.req": r"""[[["MkEWBc","[[\"{}\",\"auto\",\"{}\",true],[null]]",null,"generic"]]]""".format(text, target_language)
    }

    try:
        response = requests.post(url, headers=headers, data=from_data, timeout=timeout)
        if response.status_code == 200:
            # 正则匹配结果
            match = re.findall(r',\[\[\\"(.*?)\\",\[\\', response.text)
            if match:
                return match[0]
            else:
                match = re.findall(r',\[\[\\"(.*?)\\"]', response.text)
                if match:
                    return match[0]
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    text_to_translate = "你好世界"
    target_language = "en"
    translation = translate_sync(text_to_translate, target_language)
    if translation:
        print(f"Translation: {translation}")
    else:
        print("Failed to get translation.")
