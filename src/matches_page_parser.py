import os

import requests
from bs4 import BeautifulSoup as Bs

from single_match_parser import parse as parse_single_match


def get_matches_info(hours_offset):
    offers_container = []
    page = requests.get('https://www.hltv.org/matches')
    html = Bs(page.content, 'html.parser')

    nearest_match_day = html.find('div', class_='match-day')
    second_nearest_match_day = nearest_match_day.find_next('div', class_='match-day')

    _get_matches_for_particular_day(nearest_match_day, offers_container, hours_offset)
    _get_matches_for_particular_day(second_nearest_match_day, offers_container, hours_offset)

    return offers_container


def _get_matches_for_particular_day(day_container, offers_container, hours_offset):
    for match in day_container.find_all('a', class_='a-reset'):
        if match.find('div', class_='team'):
            parse_single_match(match['href'], offers_container, hours_offset)
