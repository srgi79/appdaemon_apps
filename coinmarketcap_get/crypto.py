import appdaemon.plugins.hass.hassapi as hass
import requests as re
import json

URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
#HEADERS = { 'Accepts': 'application/json',
#                        'X-CMC_PRO_API_KEY': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}
PARAMS = {"symbol":"USDT"}

class Crypto(hass.Hass):

    def initialize(self):
        self.log("Crypto app started")
        self.entity = "sensor.app_usdt"
        self.headers = { 'Accepts': 'application/json',
                        'X-CMC_PRO_API_KEY': self.args['token']}
        self.run_in(self.update, 0)
        self.run_every(self.update, "now", 60) #Seconds

    def update(self, kwargs):
        try:
            page = re.get(URL, headers=self.headers, params=PARAMS)
            response_dict = json.loads(page.text)
            data = response_dict['data']['USDT'][0]['total_supply']
            self.log(data)
            self.set_state(self.entity, state = data, attributes={"symbol": "USDT"})
        except:
            self.log("Crypto app failed to request")
            self.set_state(self.entity, state = 0)