import re
import json
import requests
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


class Scraper:
    def __init__(self):
        self.jp_listcardtxt_count = self.get_listcardtxt_count()
        self.lastjp = self.jp_listcardtxt_count

        self.us_api_count = self.get_usapi_count()
        self.lastus = self.us_api_count

        self.spoof_count = 0
        self.lastspoof = 0

    def get_listcardtxt_count(self):
        logging.info(f"Starting JP Request")
        square_jp_api = "http://www.square-enix-shop.com/jp/ff-tcg/card/data/list_card.txt"

        try:
            data = requests.get(square_jp_api)
            data.encoding = 'utf-8'
            content = data.text.split('\n')
            cards = []

            for line in content:
                if re.search(r"^(PR|[0-9]+)-", line):
                    cards.append(line)

            self.jp_listcardtxt_count = len(cards)

            logging.info(f"Finished JP Request - Count {self.jp_listcardtxt_count} - Requested Elapsed Time: {data.elapsed}")

        except Exception as e:
            logging.error(e)


        return self.jp_listcardtxt_count

    def get_usapi_count(self):
        logging.info(f"Starting US Request")
        square_us_api = "https://fftcg.square-enix-games.com/en/get-cards"

        try:
            data = requests.get(square_us_api)
            data.encoding = 'utf-8'
            content = json.loads(data.text)

            self.us_api_count = content['count']

            logging.info(f"Finished US Request - Count: {self.us_api_count} - Request Elapsed Time: {data.elapsed}")

        except Exception as e:
            logging.error(e)

        return self.us_api_count
