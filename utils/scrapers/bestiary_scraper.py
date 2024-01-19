import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from utils.masterdata import BeastCard


def scroll_to_end_of_page(driver):
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == driver.execute_script('return document.body.scrollHeight'):
            break


def get_page_source(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    scroll_to_end_of_page(driver)
    page_source = driver.page_source
    driver.quit()
    return page_source


def parse_page(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    beasts = soup.select('div.col.list-item__beast')
    beasts_dict = {}
    for beast in beasts:
        id = beast['data-id']
        name = beast.select_one('div.list-item-title').text
        url = beast.select_one('a')['href']
        danger = beast.select_one('span.list-mark__danger span').text
        type = beast.select_one('span.list-icon__classic')['title'] if beast.select_one(
            'span.list-icon__classic') else None
        beasts_dict[name.lower()] = BeastCard(id, name, url, danger, type).__dict__
    return beasts_dict


def write_to_file(beasts_dict, filename='../beasts.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(beasts_dict, f, ensure_ascii=False, indent=4)


def main():
    url = 'https://dnd.su/bestiary/'
    page_source = get_page_source(url)
    beasts_dict = parse_page(page_source)
    write_to_file(beasts_dict)


if __name__ == '__main__':
    main()
