import re
import html
import urllib.parse
import requests
# 此程序对于某些特定句子无法返回翻译结果

# 定义用于解析翻译结果的正则表达式模式
pattern = r'(?s)class="(?:t0|result-container)">(.*?)<'

def translate(text, target_language, source_language, timeout=50):
    # 检查输入文本的长度是否超过5000个字符
    if len(text) > 5000:
        print('\nError: It can only detect 5000 characters at once. (%d characters found.)' % (len(text)))
        exit(0)

    # 对输入文本进行URL编码
    escaped_text = urllib.parse.quote(text.encode('utf8'))
    url = f'https://translate.google.com/m?tl={target_language}&sl={source_language}&q={escaped_text}'

    try:
        # 发送HTTP GET请求
        response = requests.get(url, timeout=timeout)
        # 使用正则表达式提取翻译结果
        result = re.findall(pattern, response.text)
        # 返回解析后的结果
        return html.unescape(result[0]) if result else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # 假设 txt_contents 是一个列表，每个元素是一个元组 (content, filename)
    txt_contents = [
        # 示例数据：(文本内容, 文件名)
        ("Hello, world!", "example1.txt"),
        ("Goodbye, world!", "example2.txt"),
    ]

    # 假设 tar_argument 和 sour_argument 是目标语言和源语言的参数
    tar_argument = "zh-CN"  # 目标语言为中文
    sour_argument = "en"    # 源语言为英文

    for content, filename in txt_contents:
        # 调用 translate 函数进行翻译
        result = translate(text=content, target_language=tar_argument, source_language=sour_argument, timeout=10)
        print(f"Translation for {filename}: {result}")

if __name__ == '__main__':
    main()
