import re
import requests

def extract_translation(response_text):
    """
    Extracts the translated text from the Google Translate HTML response.

    Args:
        response_text (str): The HTML response from the Google Translate service.

    Returns:
        str: The extracted translated text if found, otherwise None.
    """
    pattern = r'<span id="tw-answ-target-text">(.*?)</span>'
    # 使用正则表达式搜索匹配的翻译文本
    match = re.search(pattern, response_text)
    if match:
        return match.group(1)
    return None


def google_translate(text, source_lang, target_lang):
    """
    Sends a request to the Google Translate service to translate text from a source language to a target language.

    Args:
        text (str): The original text to be translated.
        source_lang (str): The language code of the source text.
        target_lang (str): The language code to which the text will be translated.

    Returns:
        str: The translated text.
    """
    url = "https://www.google.com.hk/async/translate"

    # 构建请求的有效载荷
    payload = f"async=translate,sl:{source_lang},tl:{target_lang},st:{text},id:1672056488960,qc:true,ac:true,_id:tw-async-translate,_pms:s,_fmt:pc"
    
    # 定义请求的头部信息
    headers = {
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version': '"108.0.5359.125"',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-full-version-list': '"Not?A_Brand";v="8.0.0.0", "Chromium";v="108.0.5359.125", "Google Chrome";v="108.0.5359.125"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-model': '',
        'sec-ch-ua-wow64': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'X-Client-Data': 'CKW1yQEIhbbJAQiktskBCMS2yQEIqZ3KAQjb08oBCLD+ygEIlaHLAQjv8swBCN75zAEI5PrMAQjxgM0BCLKCzQEI7ILNAQjIhM0BCO+EzQEIt4XNAQ==',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Host': 'www.google.com.hk',
        'Cookie': '1P_JAR=2022-12-26-12; NID=511=eVLI1bG9nhyOZtqU14JBHm5Be00epdxfR4XmfQeehYyIkzgpXi6dbpNY75ZMVyS7aOjoM2oZ5WdoR8eNq6wi1-e_J0NeoyI0dtsHW-_8Ik4PGrqvuGHdcvVC03zTOEK2TY1FZL85Wimo_ZPIE3hGIrmGPSiel6-rRRW9lD30UPs'
    }

    # 发送POST请求到Google Translate服务
    response = requests.post(url, headers=headers, data=payload, proxies={"http": "http://127.0.0.1:10809"})
    
    # 提取并返回翻译结果
    return extract_translation(response.text)

text="""本实用新型公开了一种节能电动锄头的多功能装置，包括支撑底座，所述的支撑底座的内腔的底部的两侧转动连接有第一转轴，所述的第一转轴的两端转动连接有第一支撑杆，所述的第一支撑杆远离第一转轴的一端转动连接有滑轮，所述的第一转轴的表面，且位于支撑底座与第一支撑杆之间的位置套设有移动齿轮，本实用新型涉及生态农业设备技术领域。"""
# 调用Google Translate函数并打印结果
result = google_translate(text, target_lang='en', source_lang='zh-CN')
print(result)
