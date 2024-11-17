import requests
import re
import random
import time


class BingTranslator:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    BING_TRANSLATOR_URL = 'https://www.bing.com/translator'
    TRANSLATE_URL_TEMPLATE = 'https://www.bing.com/ttranslatev3?isVertical=1&&IG={}&IID=translator.{}.{}'
    RETRY_COUNT = 3

    def __init__(self):
        self.session = self._get_session()

    def _get_session(self):
        session = requests.Session()
        headers = {
            'User-Agent': self.USER_AGENT,
            'Referer': self.BING_TRANSLATOR_URL
        }
        session.headers.update(headers)
        response = session.get(self.BING_TRANSLATOR_URL)
        content = response.text
        self._update_session_headers(session, content)
        return session

    def _update_session_headers(self, session, content):
        params_pattern = re.compile(r'params_AbusePreventionHelper\s*=\s*(\[.*?\]);', re.DOTALL)
        match = params_pattern.search(content)
        if match:
            params = match.group(1)
            key, token, time = [p.strip('"').replace('[', '').replace(']', '') for p in params.split(',')]
            session.headers.update({'key': key, 'token': token})
        ig_match = re.search(r'IG:"(\w+)"', content)
        if ig_match:
            ig_value = ig_match.group(1)
            session.headers.update({'IG': ig_value})

    def translate(self, text, from_lang, to_lang):
        for attempt in range(self.RETRY_COUNT):
            try:
                url = self.TRANSLATE_URL_TEMPLATE.format(
                    self.session.headers.get("IG"),
                    random.randint(5019, 5026),
                    random.randint(1, 3)
                )
                data = {
                    'fromLang': from_lang,
                    'text': text,
                    'to': to_lang,
                    'token': self.session.headers.get('token'),
                    'key': self.session.headers.get('key')
                }
                response = self.session.post(url, data=data).json()
                return self._handle_response(response, text, from_lang, to_lang)
            except requests.RequestException as e:
                if attempt < self.RETRY_COUNT - 1:
                    time.sleep(2)  # Retry after a brief pause
                    self.session = self._get_session()
                else:
                    raise e

    def _handle_response(self, response, text, from_lang, to_lang):
        if isinstance(response, dict):
            if 'ShowCaptcha' in response:
                self.session = self._get_session()
                return self.translate(text, from_lang, to_lang)
            elif 'statusCode' in response and response['statusCode'] == 400:
                raise ValueError(f'1000 characters limit! You sent {len(text)} characters.')
        elif isinstance(response, list):
            return response[0].get('translations', [{}])[0].get('text', None)
        return response


class RateLimitException(Exception):
    pass


if __name__ == '__main__':
    text = '本实用新型涉及一种生产用具，尤其涉及一种用于生产的防滑犁头柄。'
    from_lang = 'zh-Hans'
    to_lang = 'en'

    # Bing Translator
    bing_translator = BingTranslator()
    for i in range(50):
        try:
            bing_translation = bing_translator.translate(text, from_lang, to_lang)
            print(bing_translation)
        except Exception as e:
            print(f"Translation failed: {e}")
