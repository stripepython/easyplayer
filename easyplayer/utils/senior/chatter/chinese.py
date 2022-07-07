from typing import Optional

from urllib.parse import urlencode
try:
    import simplejson as json
except ImportError:
    import json

import requests
from easyplayer.exceptions import EasyPlayerChatterError

__all__ = ['Chatter']


class Chatter(object):
    def __init__(self, session: Optional[requests.Session] = None):
        self.form = {
            'key': 'free',
            'appid': 0,
            'msg': ''
        }
        self.data = {}
        self.session = requests.Session() if (session is None) else session
        
    def chat(self, message: str, **kwargs):
        message = urlencode(message, **kwargs)
        url = f'http://api.qingyunke.com/api.php?key=free&appid=0&msg={message}'
        response = self.session.get(url)
        response.encoding = 'utf-8'
        self.data = json.loads(response.text)
        try:
            return self.data['content']
        except KeyError:
            err = EasyPlayerChatterError('Request failed')
            raise err from None
        
    @property
    def json(self):
        return self.data
