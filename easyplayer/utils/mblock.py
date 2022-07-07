import os
import glob

import click

try:
    import requests
except ImportError:
    from easyplayer.exceptions import EasyPlayerModuleError
    
    class _raise_error(object):
        @staticmethod
        def get(*args, **kwargs):
            raise EasyPlayerModuleError('Please install requests')
    
    requests = _raise_error


try:
    import simplejson as json
except ImportError:
    import json
    
__all__ = ['install', 'clear']


def _download_image(name, file_name):
    url = f'https://res-cn.makeblock.com/mblock/static/assets/scratch/{name}'
    response = requests.get(url)
    image_format = name.split('.')[-1]
    file_name = file_name + '.' + image_format
    with open(f'downloads/{file_name}', 'wb') as fp:
        fp.write(response.content)
    click.echo(f'INFO: downloaded {file_name}')


def _load_json():
    url = 'https://res-cn.makeblock.com/mblock/static/sprites/makeblock/sprites.json'
    response = requests.get(url)
    response.encoding = 'utf-8'
    result = json.loads(response.text)
    click.echo('INFO: loaded sprites json-file')
    return result


def install():
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
        click.echo('INFO: created downloads folder')
    sprites = _load_json()
    for sprite_info in sprites:
        name = sprite_info.get('name', 'nullify')
        md5 = sprite_info.get('md5', None)
        if md5:
            _download_image(md5, name)


def clear():
    if os.path.exists('downloads'):
        for fp in glob.glob('downloads/*.*'):
            os.remove(fp)
            click.echo(f'INFO: deleted {fp}')
    else:
        click.echo('ERROR: not installed mblock-images')
