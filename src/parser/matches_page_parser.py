import datetime
import requests
from bs4 import BeautifulSoup as Bs

from .single_match_parser import parse as parse_single_match


def get_matches_info():
    offers_container = []
    page = requests.get('https://www.hltv.org/matches')
    html = Bs(page.content, 'html.parser')

    nearest_match_day = html.find('div', class_='match-day')

    current_date = datetime.datetime.today().strftime('%Y-%m-%d - %A')
    nearest_matches_date = nearest_match_day.find('span', class_='standard-headline', recursive=False).text

    if current_date == nearest_matches_date:
        # print('no matches for today!')
        for match in nearest_match_day.find_all('a', class_='a-reset'):
            if match.find('div', class_='team'):
                parse_single_match(match['href'], offers_container)

    return offers_container
