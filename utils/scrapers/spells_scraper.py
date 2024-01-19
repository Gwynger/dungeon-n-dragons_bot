import json
import time
from dataclasses import asdict

import requests  # type: ignore
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

from utils.masterdata import SpellCard


# Function to scroll through the page and retrieve all data
def scroll_through_page(driver):
    len_of_page = driver.execute_script(
        'window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;')
    match = False
    while not match:
        last_count = len_of_page
        time.sleep(3)
        len_of_page = driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;')
        if last_count == len_of_page:
            match = True
    return driver.page_source


# Function to extract data from script tags in html source
def extract_data_from_script(source_data):
    soup_data = BeautifulSoup(source_data, 'html.parser')
    scripts = soup_data.findAll('script')
    for script in scripts:
        if 'window.LIST' in script.text:
            json_str = script.text
            json_str = json_str.split(' = ')[1]
            data = json.loads(json_str[:-1])
            return data


# Function to get detailed information about each spell
def get_spell_details(card, card_url):
    response = requests.get(card_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    params_ul = soup.find('ul', class_='params')
    params_lis = params_ul.find_all('li') if params_ul else []

    for li in params_lis:
        text = li.get_text(' ', strip=True)
        if li.get('class') and 'subsection' in li.get('class'):
            card.description = text
        elif li.get('class') and 'size-type-alignment' in li.get('class'):
            card.level_school = text
        elif ':' in text:
            detail_name, detail_value = (t.strip() for t in text.split(':', 1))
            if detail_name == 'Время накладывания':
                card.casting_time = detail_value
            elif detail_name == 'Дистанция':
                card.c_range = detail_value
            elif detail_name == 'Компоненты':
                card.components = detail_value
            elif detail_name == 'Длительность':
                card.duration = detail_value
            elif detail_name == 'Классы':
                card.classes = detail_value
            elif detail_name == 'Архетипы':
                card.archetypes = detail_value
            elif detail_name == 'Источник':
                card.source = detail_value
    return card


def main():
    url = 'https://dnd.su/spells/'

    # Selenium Creating spell cards and collecting links (plus a bit of information)
    driver = webdriver.Chrome()
    driver.get(url)

    source_data = scroll_through_page(driver)
    driver.quit()

    data = extract_data_from_script(source_data)

    # Extract cards data and create SpellCard objects
    cards = data['cards']
    fields = ['title', 'title_en', 'link', 'level', 'school']  # specify the keys you want
    spell_cards = [SpellCard(**{k: card[k] for k in fields}) for card in cards]

    # Dictionary to store spell card details
    spell_cards_dict = {}

    # Run through the collected links and fill in the details of the cards
    for card in tqdm(spell_cards, desc='Processing spell cards', unit='card'):
        card_url = url[:-8] + card.link
        card = get_spell_details(card, card_url)

        card_title_lower = card.title.lower()
        spell_cards_dict[card_title_lower] = asdict(card)

    with open('../spells.json', 'w', encoding='utf-8') as f:
        json.dump(spell_cards_dict, f, ensure_ascii=False, indent=4)


# To run the script
if __name__ == '__main__':
    main()
