import requests
import json
from html.parser import HTMLParser
from bs4 import BeautifulSoup

r = requests


def get_korona(currency='usd'):
    currency_id = {
        'usd':'840',
        'eur':'978',
        'gel':'981'
    }
    url = 'https://koronapay.com/transfers/online/api/transfers/tariffs?sendingCountryId=RUS&sendingCurrencyId=810&receivingCountryId=GEO&receivingCurrencyId='+currency_id[currency]+'&paymentMethod=debitCard&receivingAmount=10000&receivingMethod=cash&paidNotificationEnabled=true'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    req = r.get(url,headers=headers)
    
    if req.status_code == 200:
        txt = req.text
        rate = float(json.loads(txt)[0]['exchangeRate'])
        #print('Korona rate for '+currency+' is '+str(rate))
        return rate
    else:
        raise ValueError('Korona returned ' + str(req.status_code))

    
#get_korona('GEL')

def get_libery(operation = 'usd_buy'):
    url = 'https://www.libertybank.ge/en/'
    req = r.get(url)

    if req.status_code == 200:
        html = req.text
        
        operations = {
            'usd_buy': 3,
            'usd_sell': 4,
            'eur_buy': 10,
            'eur_sell': 11
        }

        soup = BeautifulSoup(html,"html.parser")
        rates = soup.find_all('span', class_='currency-rates__currency caps bold')
        
        if operation == 'eurusd':
            eur = float(rates[operations['eur_sell']].text)
            usd = float(rates[operations['usd_sell']].text)
            rate = eur/usd
            rate = round(rate,4)
            return rate
        
        rate = float(rates[operations[operation]].text)
        #print('Liberty rate for '+operation+' is '+str(rate))
        
        return rate

    else:
        raise ValueError('Libery returned ' + str(req.status_code))    
        
def get_unistream(currency='usd'):
    url = 'https://online.unistream.ru/card2cash/calculate?destination=GEO&amount=100&currency='+currency+'&accepted_currency=RUB&profile=unistream'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    req = r.get(url,headers=headers)
    
    if req.status_code == 200:
        txt = req.text
        rate = pow(json.loads(txt)['fees'][0]['rate'],-1)
        #print('Unistream rate for '+currency+' is '+str(rate))
        
        return rate
    else:
        raise ValueError('Unistream returned ' + str(req.status_code))



def find_best_exchange():
    exchanges = {
        'Korona EUR direct':get_korona('eur'),
        'Korona USD -> EUR':get_korona('usd')*get_libery('eurusd'),
        'Korona GEL -> EUR':get_korona('gel')*get_libery('eur_buy'),
        'Unistr EUR direct':get_unistream('eur'),
        'Unistr USD -> EUR':get_unistream('usd')*get_libery('eurusd'),
        'Unistr GEL -> EUR':get_unistream('gel')*get_libery('eur_buy')
    }

    list_exchanges = list(exchanges.keys())
    
    for i in range(0,len(exchanges)):
        operation = list_exchanges[i]
        rate = exchanges[operation]
        rate = round(rate,4)
        print(operation + ' | ' + str(rate))

find_best_exchange()