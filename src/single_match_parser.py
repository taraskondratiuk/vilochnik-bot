import datetime

import requests
from bs4 import BeautifulSoup as Bs

from offer import Offer, add_offer_info_to_container


def parse(url, offers_container, hours_offset):
    url = 'https://www.hltv.org' + url
    page = requests.get(url)
    html = Bs(page.content, 'html.parser')

    unix_time = html.find('div', class_='time')['data-unix']
    match_date_time = datetime.datetime.fromtimestamp(int(unix_time) / 1000) + datetime.timedelta(hours=hours_offset)

    tournament = html.find('div', class_='event text-ellipsis').find('a').text

    coef_container = html.find('table', class_='table')

    if coef_container:
        teams = coef_container.find_all('td', class_='team-cell')
        if not teams:
            return
        team1 = teams[0].text
        team2 = teams[2].text

        offers_list = []

        for offer in coef_container.find_all('tr', class_='provider'):
            if not (offer.find('td', class_='noOdds') or offer['class'][0] == 'hidden'):
                offer_container_anchors = offer.find_all('a')
                offers_list.append(Offer(
                    link1=offer_container_anchors[1]['href'],
                    link2=offer_container_anchors[1]['href'],
                    coef1=float(offer_container_anchors[1].text),
                    coef2=float(offer_container_anchors[3].text)
                ))

        add_offer_info_to_container(team1,
                                    team2,
                                    tournament,
                                    match_date_time,
                                    offers_list,
                                    url,
                                    offers_container)
