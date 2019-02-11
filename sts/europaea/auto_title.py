import requests
from bs4 import BeautifulSoup

from .global_value import CN_SITE_URL
from .cache import PageCache


def fetch_title_by_item_no(item_no):
    try:
        i_item_no = int(int(item_no) / 1000) + 1
    except ValueError:
        return '[E] invalid item#'
    if i_item_no not in PageCache.page_soup:
        if i_item_no == 1:
            url = f'{CN_SITE_URL}/scp-series'
        else:
            url = f'{CN_SITE_URL}/scp-series-{i_item_no}'
        html = requests.get(url)
        _soup = BeautifulSoup(html.text, 'lxml')
        PageCache.page_soup[i_item_no] = _soup.find_all(
            name='div',
            attrs={'class': 'content-panel standalone series'},
            limit=1)[0]
    main_contant = PageCache.page_soup[i_item_no]
    ele_title = main_contant.find_all(
        name='a',
        text=f'SCP-{item_no}',
        limit=1)[0]
    if not ele_title:
        return '[E] cannot find title'
    return ele_title.parent.text.split(' - ')[1]


def fetch_title_by_url(doc_id):
    html = requests.get(f'{CN_SITE_URL}/{doc_id}')
    _soup = BeautifulSoup(html.text, 'lxml')
    ele_title = _soup.find(id='page-title')
    if not ele_title:
        return '[E] cannot find title'
    return ele_title.text.strip()
