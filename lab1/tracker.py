import requests
import json
import copy

class Tracker:
    def __init__(self, coins):
        url = ''
        for c in coins:
            url += c + '%2C'
        url = url[:-3]

        self.base_url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={url}&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        self.data = {}

        r = json.loads(requests.get(self.base_url).text)

        for i in r:
            self.data.update({i['symbol']:[i['current_price'], i['total_volume']]})
    
    def get_data(self):
        save = copy.deepcopy(self.data)

        try:
            r = json.loads(requests.get(self.base_url).text)
            for i in r:
                self.data.update({i['symbol']:[i['current_price'], i['total_volume']]})
            return self.data
        except:
            return save