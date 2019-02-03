import requests
from bs4 import BeautifulSoup

from .common import SCP_CN_SITE


class Cache:
    PAGE_CONTANT_SOUP = dict()


def fetch_title_by_item_no(item_no_):
    try:
        i_item_no_ = int(int(item_no_)/1000)+1
    except ValueError:
        return '[E] invalid item#'
    if i_item_no_ not in Cache.PAGE_CONTANT_SOUP:
        if i_item_no_ == 1:
            url = f'{SCP_CN_SITE}/scp-series'
        else:
            url = f'{SCP_CN_SITE}/scp-series-{i_item_no_}'
        html = requests.get(url)
        _soup = BeautifulSoup(html.text, 'lxml')
        Cache.PAGE_CONTANT_SOUP[i_item_no_] = _soup.find_all(
            name='div',
            attrs={'class': 'content-panel standalone series'},
            limit=1)[0]
    main_contant = Cache.PAGE_CONTANT_SOUP[i_item_no_]
    ele_title = main_contant.find_all(
        name='a',
        text=f'SCP-{item_no_}',
        limit=1)[0]
    if not ele_title:
        return '[E] cannot find title'
    return ele_title.parent.text.split(' - ')[1]

def fetch_title_by_url(doc_id):
    html = requests.get(f'{SCP_CN_SITE}/{doc_id}')
    _soup = BeautifulSoup(html.text, 'lxml')
    ele_title = _soup.find(id='page-title')
    if not ele_title:
        return '[E] cannot find title'
    return ele_title.text.strip()
