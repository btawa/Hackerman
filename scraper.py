import re
import json
import requests


class Scraper:
    def __init__(self):
        self.jp_listcardtxt_count = self.get_listcardtxt_count()
        self.lastjp = self.get_listcardtxt_count()

        self.us_api_count = self.get_usapi_count()
        self.lastus = self.get_usapi_count()

        self.spoof_count = 0
        self.lastspoof = 0

    def get_listcardtxt_count(self):
        square_jp_api = "http://www.square-enix-shop.com/jp/ff-tcg/card/data/list_card.txt"

        data = requests.get(square_jp_api)
        data.encoding = 'utf-8'
        content = data.text.split('\n')
        cards = []

        for line in content:
            if re.search(r"^(PR|[0-9]+)-", line):
                cards.append(line)

        self.jp_listcardtxt_count = len(cards)
        return len(cards)

    def get_usapi_count(self):
        square_us_api = "https://fftcg.square-enix-games.com/en/get-cards"

        data = requests.get(square_us_api)
        data.encoding = 'utf-8'
        content = json.loads(data.text)

        self.us_api_count = content['count']
        return content['count']

