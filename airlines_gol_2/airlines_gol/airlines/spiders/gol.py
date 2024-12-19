import scrapy
import json
import random

from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzlocal
from ..token_generator import TokenGenerator
from ..items import AirlinesItem

# CASO O PROGRAMA PARE, ENTRE NO SITE: http://voegol.com.br/, ACESSE UM VOO QUALQUER, ENTRE NO DEVTOOLS (F12) EM NETWORK,  E PROCURE
# POR b2c-api.voegol.com.br/api/sabre-default/flights?context=b2c&flow=Issue, E PROCURE EM HEADERS >REQUEST HEADERS> Authorization
# AGORA COPIE E COLE ABAIXO NO self.headers

class GolSpider(scrapy.Spider):
    name = 'gol'
    allowed_domains = ['voegol.com.br']
    start_urls = ['http://voegol.com.br/']
    
    

    def __init__(self):
        self.stations = ['GRU', 'GIG', 'CNF', 'SSA', 'BSB', 'FOR', 'REC', 'POA', 'CWB', 'AJU', 'BEL', 'CGR', 'GYN', 'SLZ',
                         'VIX', 'RBR', 'NAT', 'FLN', 'MAO', 'MCZ', 'THE', 'JPA', 'CGB']
        self.rotas = self.create_routes( self.stations)
        self.ua = random.choice(['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' ])
        self.token = TokenGenerator(self.ua).create_token() #rever a criação desse token
        self.urlstg = "https://b2c-api.voegol.com.br/api/sabre-default/flights?context=b2c&flow=Issue"
        self.dates = self.calc_dates()
        self.counter = 0
        self.dados_bruto = list()
        
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Authorization': self.token,
            'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjkyM0NFMDYyQkI0M0QzRTNFNEEzQUM2MkFENTMwNUMzRDEyNEM3MzIiLCJ4NXQiOiJranpnWXJ0RDAtUGtvNnhpclZNRnc5RWt4ekkiLCJ0eXAiOiJKV1QifQ.eyJkY3QiOiJWREZTVEVGUlMyVlZhakZtZW0xcGEyZERNelJHY1VoSFZXVlNNeTlOWTNNNGFYb3lRbXBXWWtSVVlraHdLekZaY1doQlQyUXdTSFp5UkhBMlpYTjRlRk0xYVVOVloxTlhRVUZFVVdaNWR6TlFWMnRaZFZOWWVscG5SRzl1V2pSRGNUUkJVbUZyZUhCRlRFcE5lV0pEZW5scmMySlhWMGszVG5jeGFWZHdjRmhEYWt0cmFGb3ZaVTFVYWpOdmRTOU1SbXBvYmpkelVrVkNOVkJHVHpCNGNXUjJVa3cyYkN0blFuTTRTM1ZqYkRWQmMyOTFlV0V3V1Roc2JsTTBabGRzUmk5VmVrZFhPWEEyZDFka2NWUlFUaTh4TldOMGNYUjFiVmxDYmtkVFJ6aEhNazFUVGpZdlowMU9OR3N5ZDNwTFUzZG1UVUZzUkd4Vk4zaERaMmMxZDNaTGRubFNkR3h0U0VGc1NUSmxNWGRZUW5KdE5UTlRZVkZrTkhFMGNsbFFWazk1T1ZkNmRHTjVOMHRwVmxwaVJFdDVaelZoY21Vd1NUaGxTM2swTldGVU5tdGFNV1pyU2pWVGIwOWFZM1Z1TDNaeFNUZ3paMjV1UnpSMVkwaHVOamRCS2lvPSIsInN0ZiI6IkczREMiLCJuYmYiOjE3MzQzNTYxMjUsImV4cCI6MTczNDc4ODEyNiwiaWF0IjoxNzM0MzU2MTI2LCJpc3MiOiJodHRwczovL2F1dGgtYXBpLnZvZWdvbC5jbG91ZCIsImF1ZCI6ImIyYy52b2Vnb2wuY29tLmJyL1BST0QifQ.pp4nLpk0EFPjfJCcYw3i-BJhim-KtifLT_v1kjwksRuz0sn2pSV5SACdN1F8_EjWr44z8xnnvpLXhVxQ2I_3oNvLiaUPNQowaVt__gJC6UCuixVzsmhrvJ7mwNcLB47zOKz71vp9J7Mtdg0hgyzSgqhl1EuC0rwCiloguHSac4kfXGNrSRjfEK6ZikoIHvziAvJfXLq53VjPxYvLogj7dAhB8KZ6yJDjWknq91iBxKb2j27b2UH0LIjK3vMp9Jqn2l_qif5a19vjZPODSckzLwNA4Ers4cEqtFslbgLddRyAf3RDuJPrU9gUL7KPd26mt9ykpKjah0-OXQYbGJzQ6Q",
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'b2c-api.voegol.com.br',
            'Origin': 'https://b2c.voegol.com.br',
            'Referer': 'https://b2c.voegol.com.br/',
            'Cookie': '_gcl_au=1.1.1863648732.1629930187; _4c_=%7B%22_4c_mc_%22%3A%226d55bf36-b2f2-4ab2-920c-eef0cb5d0611%22%7D; OptanonConsent=isIABGlobal=false&datestamp=Sun+Oct+03+2021+16%3A37%3A17+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=6.15.0&hosts=&consentId=e4cdaea7-67cb-4c0b-8712-2602888774be&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=BR%3BSP&AwaitingReconsent=false; _dyn_id.64b3=24c68d9c-41d1-523d-9512-66212283b5f2.1629930188.4.1633289839.1631639518.7726e95b-153c-4830-ba94-da3ef86edd5d; _ga=GA1.3.685429798.1629930189; _fbp=fb.2.1629930189351.1384699519; _gaexp=GAX1.3.4lP59E9wQDSdfd7DsdxqRQ.18971.1!oLIZnmk-SZ69MN2CGhRghA.18978.0; OptanonAlertBoxClosed=2021-10-03T19:37:17.209Z; visid_incap_2631856=CwPagUcOQXubkx2yla4bKPXCJmEAAAAAQUIPAAAAAAD1OgFursl/UnE9vsuiSglD; cto_bundle=cARSF18wZUhLMUh2TlF5Vnc1N2tSU3lvSGNUekpvWGU0b2F3U0VBdFpvcEdqYzhtJTJCZk5td2VLREdwWjZqMUd4QkREaEM4RzRoS2xkZjZKNHREZnlwV290MDYyWXVHR0NpeVR4b1ZVZFFnTU0ybzllb0FoY2tja2YwS3lxcGtDQ0pMU05MN1F6SEpnVDJBZkp1SWJNZWlzUGtGZyUzRCUzRA; _hjid=ec06553f-fbde-4d97-a2ed-7249218a5151; kppid_managed=kppidff_OXKAtub5; _uetvid=05eca60005f311ec8d8837f38fd8c708; visid_incap_2652338=JWLSpMWBRLm7naDAlBp9xmkGWmEAAAAAQUIPAAAAAAAadObdoO9eTs5BYfa0H73B; incap_ses_1454_2652338=cesCbytjrlPMP0D8UqUtFGkGWmEAAAAA8BoUeBRZ3oCMRGH/81+vzQ==; _gid=GA1.3.1617142352.1633289838; _dc_gtm_UA-75870109-1=1; dtCookie==3=srv=14=sn=STH1O9HJ0B9M21NVA67HHV437JSV0FEQ=app:24a72bec43719dda=0=ol=0=perc=100000=mul=1; rxVisitor=1633289838860HT2LC155RR0HNDRLN12TMBMPT23QFQMM; dtPC=14$89865863_428h3p14$89868013_39h10p14$89871673_815h3vEKAEWQWPHJUDCKCTCBUGDIHWPVMACSVQ-0e3; rxvt=1633291672039|1633289838862; dtSa=-; dtLatC=148; _dyn_ses.64b3=*; incap_ses_1354_2631856=ryqkeMh1VSoWboPRFGDKEokGWmEAAAAArXGok2ndfXfuXiR2iFQ3LA==',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': self.ua,
            'x-jsessionid': '', 
            'x-sabre-cookie-encoded': '',
            }

    def create_routes(self,lst):
        combinations = []
        for i in range(len(lst)):
            for j in range(len(lst)):
                if i != j:
                    combinations.append((lst[i], lst[j]))
        return combinations

        
    
    def calc_dates(self):
        d = datetime.now(tzlocal()) + timedelta(60)
        t = timedelta((12 - d.weekday()) % 7)
        ddate = d + t
        adate = ddate + timedelta(8)
        ddate = ddate.strftime('%Y-%m-%d')
        adate = adate.strftime('%Y-%m-%d')
        when_dep = ddate + "T03:00:00.000Z"
        when_arr = adate + "T03:00:00.000Z"

        return (when_dep, when_arr)
    
    def build_payload(self, rota):
        payload = {"promocodebanner":False,"destinationCountryToUSA":False,"lastSearchCourtesyTicket":False,"passengerCourtesyType":None,
        "airSearch":{"cabinClass":None,"currency":None,"pointOfSale":"BR","awardBooking":False,"searchType":"BRANDED","promoCodes":[""],
        "itineraryParts":[{"from":{"code":rota[0],"useNearbyLocations":False}, "to":{"code":rota[1],"useNearbyLocations":False},
        "when":{"date":self.dates[0]},"selectedOfferRef":None,"plusMinusDays":None},
        {"from":{"code":rota[1],"useNearbyLocations":False},"to":{"code":rota[0],"useNearbyLocations":False},
        "when":{"date":self.dates[1]},"selectedOfferRef":None,"plusMinusDays":None}],
        "passengers":{"ADT":1,"CHD":0,"INF":0},"trendIndicator":None,"preferredOperatingCarrier":None}}

        return payload
    
    def start_requests(self):
        payload = self.build_payload(self.rotas[0])
        yield scrapy.Request(self.urlstg, method='POST', body=json.dumps(payload), headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        # raw_data = json.loads(response.text)
        data_hoje = str(datetime.now(tzlocal()).date().strftime("%d-%m-%Y"))

        try:
            ida = data['response']['airSearchResults']['unbundledOffers'][0]
            volta = data['response']['airSearchResults']['unbundledOffers'][1]

            for voo in ida:
                item = AirlinesItem()
                
                item['crawler'] = 'gol'
                item['scandate'] = datetime.now(tzlocal()).strftime('%d-%m-%Y')
                item['departuredate'] = voo['itineraryPart'][0]['segments'][0]['departure']
                item['arrivaldate'] = voo['itineraryPart'][0]['segments'][0]['arrival']
                item['trajeto'] = 'ida'
                item['departurestation'] = voo['itineraryPart'][0]['segments'][0]['origin']
                item['arrivalstation'] = voo['itineraryPart'][0]['segments'][0]['destination']
                item['fullfare'] = voo['total']['alternatives'][0][0]['amount']
                item['productclass'] = voo['brandId']

                #COLETA DOS DADOS BRUTOS
                # nome_json = f"raw_data_{data_hoje}_{item['departurestation']}_para_{item['arrivalstation']}"
                # out_file = open(nome_json, "wt")
                # json_data = json.dump(data, out_file, indent=4)
                # self.dados_bruto.append({nome_json: json_data})
                # print(self.dados_bruto)

                yield item
    
            for voo in volta:
                item = AirlinesItem()

                item['crawler'] = 'gol'
                item['scandate'] = datetime.now(tzlocal()).strftime('%d-%m-%Y')
                item['departuredate'] = voo['itineraryPart'][0]['segments'][0]['departure']
                item['arrivaldate'] = voo['itineraryPart'][0]['segments'][0]['arrival']
                item['trajeto'] = 'volta'
                item['departurestation'] = voo['itineraryPart'][0]['segments'][0]['origin']
                item['arrivalstation'] = voo['itineraryPart'][0]['segments'][0]['destination']
                item['fullfare'] = voo['total']['alternatives'][0][0]['amount']
                item['productclass'] = voo['brandId']

                #COLETA DOS DADOS BRUTOS
                # nome_json = f"raw_data_{data_hoje}_{item['departurestation']}_para_{item['arrivalstation']}"
                # out_file = open(nome_json, "wt")
                # json_data = json.dump(data, out_file, indent=4)
                # self.dados_bruto.append({nome_json: json_data})
                # print(self.dados_bruto)

                yield item

            self.counter += 1
        except:
            self.counter += 1
            print('Nenhum voo encontrado!')

        if self.counter < len(self.rotas):
            payload = self.build_payload(self.rotas[self.counter])
            yield scrapy.Request(self.urlstg, method='POST', body=json.dumps(payload), headers=self.headers, callback=self.parse)
            #time.sleep(10*(1+random.uniform(0,1)))
            
        else:
            print("Coleta finalizada.")

            
    
