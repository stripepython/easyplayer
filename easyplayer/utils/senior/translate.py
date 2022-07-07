"""
Original module: pybaidu.translate
Original author: stripe-python

"""

import os
import re
from typing import Optional, Dict, Union

import requests
import execjs  # JS reverse requires

try:
    import simplejson as json
except (ModuleNotFoundError, ImportError):
    import json

from easyplayer.exceptions import EasyPlayerTranslateError

__all__ = ['languages', 'JSEngines', 'Translator']

class _Languages(object):
    auto = automatic_detection ='auto'
    chinese = simplified_chinese = 'zh'
    japanese = 'jp'
    japanese_kana = 'jpka'
    thai = 'th'
    france = 'fra'
    english = 'en'
    spanish = 'spa'
    korean = 'kor'
    turkish = 'tr'
    vietnamese = 'vie'
    malay = 'ms'
    german = 'de'
    russian = 'ru'
    iranian = 'ir'
    arabic = 'ara'
    estonian = 'est'
    belarusian = 'be'
    bulgarian = 'bul'
    hindi = 'hi'
    icelandic = 'is'
    polish = 'pl'
    farsi = 'fa'
    danish = 'dan'
    filipino = 'tl'
    finnish = 'fin'
    dutch = 'nl'
    catalan = 'ca'
    czech = 'cs'
    croatian = 'hr'
    latvian = 'lv'
    lithuanian = 'lt'
    romanian = 'rom'
    south_african = 'af'
    norwegian = 'no'
    brazilian = 'pt_BR'
    portuguese = 'pt'
    swedish = 'swe'
    serbian = 'sr'
    esperanto = 'eo'
    slovak = 'sk'
    slovenian = 'slo'
    swahili = 'sw'
    ukrainian = 'uk'
    hebrew = 'iw'
    greek = 'el'
    hungarian = 'hu'
    armenian = 'hy'
    italian = 'it'
    indonesian = 'id'
    albanian = 'sq'
    amharic = 'am'
    assamese = 'as'
    azerbaijani = 'az'
    basque = 'eu'
    bengali = 'bn'
    bosnian = 'bs'
    galician = 'gl'
    georgian = 'ka'
    gujarati = 'gu'
    hausa = 'ha'
    igbo = 'ig'
    inuit = 'iu'
    irish = 'ga'
    zulu = 'zu'
    kannada = 'kn'
    kazakh = 'kk'
    kyrgyz = 'ky'
    luxembourgish = 'lb'
    macedonian = 'mk'
    maltese = 'mt'
    maori = 'mi'
    marathi = 'mr'
    nepali = 'ne'
    oriya = 'or'
    punjabi = 'pa'
    kachua = 'qu'
    seswana = 'tn'
    sinhala = 'si'
    tamil = 'ta'
    tatar = 'tt'
    telugu = 'te'
    urdu = 'ur'
    uzbek = 'uz'
    welsh = 'cy'
    yoruba = 'yo'
    cantonese = 'yue'
    classical_chinese = 'wyw'
    chinese_traditional = 'cht'
    
    
class JSEngines(object):
    node = node_js = 'Node'
    pyv8 = 'PyV8'
    java_script_core = 'JavaScriptCore'
    spidermonkey = spider_monkey = 'SpiderMonkey'
    jscript = 'JScript'
    phantomjs = 'PhantomJS'
    slimerjs = 'SlimerJS'
    nashorn = 'Nashorn'


languages = _Languages

_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/68.0.3440.106 Safari/537.36'
)


def _get_gtk():
    """
    Get window GTK value, a constant.

    :return: Window GTK value
    """
    return '320305.131321201'


def _get_sign(word: str):
    """
    JS reversely obtains the sign value.
    JS comes from the JavaScript code translated by Baidu Fanyi.

    :param word: Text to be translated.
    :type word: str
    :return: Sign value
    """
    gtk = _get_gtk()  # GTK value
    # JS code
    js = r'''
var t = "{{word}}"
var i = "{{gtk}}"
function a(r) {
    if (Array.isArray(r)) {
        for (var o = 0, t = Array(r.length); o < r.length; o++) t[o] = r[o];
        return t
    }
    return Array.from(r)
}
function n(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a), a = "+" === o.charAt(t + 1) ? r >>> a : r << a, r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}
function e(r) {
    var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
    if (null === o) {
        var t = r.length;
        t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
    } else {
        for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++) "" !== e[C] && f.push.apply(f, a(e[C].split(""))), C !== h - 1 && f.push(o[C]);
        var g = f.length;
        g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
    }
    var u = void 0;
    var l = "gtk";
    var u = null !== i ? i : (i = {{gtk}} || "") || "";
    for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
        var A = r.charCodeAt(v);
        128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
    }
    for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b], p = n(p, F);
    return p = n(p, D), p ^= s, 0 > p && (p = (2147483647 & p) + 2147483648), p %= 1e6, p.toString() + "." + (p ^ m)
}
    '''
    
    js = js.replace('{{word}}', word)  # Replace variables
    js = js.replace('{{gtk}}', gtk)
    
    python = execjs.compile(js)
    sign = python.call('e', word)
    return sign


def _get_token(session: requests.Session, headers: Dict[str, str], cookies: Optional[Dict[str, str]] = None):
    """
    Get the window token value from Baidu translation website.

    :param headers: Request header.
    :return: Window token value
    """
    url = 'https://fanyi.baidu.com/?aldtype=16047'
    response = session.get(url, headers=headers, cookies=cookies)
    
    html = response.text
    token = re.findall("token: '(.*)'", html)
    if not token:
        raise EasyPlayerTranslateError('not found token')
    token = token[0]
    return token


class Translator(object):
    def __init__(self, input_language: str = languages.auto, output_language: str = languages.english,
                 session: Optional[requests.Session] = None, js_engine: str = JSEngines.node,
                 cookies: Optional[Union[Dict[str, str], str]] = None, user_agent: str = _USER_AGENT,
                 **other_headers: Dict[str, str]):
        os.environ['EXECJS_RUNTIME'] = js_engine  # Set the PyExecJS running environment
        self.url = 'https://fanyi.baidu.com/v2transapi'
        
        self.headers = {'User-Agent': user_agent, **other_headers}
        if isinstance(cookies, str):
            self.headers['Cookie'] = cookies
            cookies = None
        self.cookies = cookies
        
        if not session:
            session = requests.session()
        self.session = session
        
        self._form = {
            'from': input_language,
            'to': output_language,
            'query': '',
            'transtype': 'translang',
            'simple_means_flag': '3',
            'domain': 'common',
            'sign': '',
            'token': ''
        }
        self._data = {}
        self._loaded = False
        
    def load(self, text: str):
        self._form['query'] = text
        self._form['sign'] = _get_sign(text)
        self._form['token'] = _get_token(self.session, self.headers, self.cookies)
        self._loaded = True
        
    def get(self, **kwargs):
        if not self._loaded:
            raise EasyPlayerTranslateError('please load the text first')
        response = self.session.post(self.url, data=self._form, headers=self.headers,
                                     cookies=self.cookies, **kwargs)
        response.encoding = 'utf-8'
        data = json.loads(response.text)
        if 'errno' in data:
            code = data['errno']
            msg = data['errmsg']
            raise EasyPlayerTranslateError(f'[Error No {code}] {msg}')
        self._data = data
        return data['trans_result']['data'][0]['dst']

    @property
    def data(self):
        return self._data
