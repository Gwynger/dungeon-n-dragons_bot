import json
from dataclasses import asdict

import requests  # type: ignore
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils.masterdata import FeatCard


# This function extracts the necessary data from the feat's page
def scrape_feat_card_details(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    card_wrapper = soup.find('div', class_='card-wrapper')

    title_span = card_wrapper.find('span', {'data-copy': True})
    title, title_en = title_span.text.split(' [')
    title_en = title_en.strip(']')

    description_div = card_wrapper.find('div', itemprop='description')
    description = description_div.text.strip()

    requirements_li = card_wrapper.find('li', class_='size-type-alignment')
    requirements = requirements_li.text.strip().replace('Требование: ', '') if requirements_li else None

    source_span = card_wrapper.find('span', class_='source-plaque')
    source = source_span['title'] if source_span else None

    # Only save the postfix part of the URL, not the whole URL
    url_postfix = url.replace('https://dnd.su', '')

    return FeatCard(title, url_postfix, title_en, requirements, description, source)


def main():
    url = 'https://dnd.su/feats/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    feats_html = soup.find_all('div', class_='col list-item__spell for_filter')

    feat_cards_dict = {}
    for feat_html in tqdm(feats_html):
        url = 'https://dnd.su' + feat_html.a['href']
        feat_card = scrape_feat_card_details(url)
        feat_cards_dict[feat_card.title.lower()] = asdict(feat_card)

    with open('../feats.json', 'w', encoding='utf-8') as f:
        json.dump(feat_cards_dict, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
