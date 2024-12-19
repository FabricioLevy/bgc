from requests import NullHandler, Session
import json

class TokenGenerator:

    def __init__(self, ua):
        self.ua = ua
        self.session = Session()

    def create_token(self):
        url = 'https://gol-auth-api.voegol.com.br/api/authentication/create-token'

        headers = {
            'Host': 'gol-auth-api.voegol.com.br',
            'User-Agent': self.ua,
            'Accept': 'text/plain',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://b2c.voegol.com.br/',
            'X-AAT': 'NEUgdaCsLXoDdbB0/Jfb+d6O72lprMfUJxaW/eTW7ncXFZgMqTtFpi5mQdzidn0c0EnON6hHWtrBAshheNOhtQ==',
            'Origin': 'https://b2c.voegol.com.br',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Connection': 'keep-alive'
        }

        r = self.session.get(url=url, headers=headers, verify=False)
        print(r.text)
        data = json.loads(r.text)
        token = 'Bearer ' + data['response']['token']
        print(token)

        return token