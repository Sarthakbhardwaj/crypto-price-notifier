import sys
import bs4
import requests
from bs4 import BeautifulSoup
from plyer import notification

import time
from datetime import date

import os
os.system('color') 
COLOR = {
    'PINK': '\033[95m',
    'YELLOW': '\033[93m',
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'ENDC': '\033[0m'
}

def Crypto_Price_Scraper(coin,curr,inter):

    url = 'https://coinmarketcap.com/currencies/'+coin
    response = requests.get(url)
    page = response.text
    response.close()
    soup = BeautifulSoup(page,'html.parser')

    data = soup.find('h2',class_='sc-1q9q90x-0 jCInrl h1')
    for x in data:
        if isinstance(x,bs4.element.NavigableString):
            name = x.strip()#use of this?
    acr = data.find('small').text#yeh kya h?
    coinname = name+' ('+acr+')'
    
    currname = ''
    if curr=='inr':
        currname = 'INR(₹) - Indian Rupee'
        currsymb = '₹'
    elif curr=='usd':
        currname = 'USD($) - United States Dollar'
        currsymb = '$'
    elif curr=='eur':
        currname = 'EUR(€) - Euro'
        currsymb = '€'
    elif curr=='gbp':
        currname = 'GBP(£) - Pound sterling'
        currsymb = '£'
    elif curr=='jpy':
        currname = 'JPY(¥) - Japanese Yen'
        currsymb = '¥'

    mm = str(inter%60)
    hh = str((inter//60)%24)
    dd = str((inter//60)//24)
    interval = dd+' days, '+hh+' hours and '+mm+' minutes'

    print('\n\tNotifications set for price of '+COLOR['PINK']+coinname+COLOR['ENDC']+' in the national currency '+COLOR['PINK']+currname+COLOR['ENDC']+' in an interval of '+COLOR['PINK']+interval+COLOR['ENDC']+'.')

    while True:
        
        response = requests.get(url)
        page = response.text
        response.close()
        soup = BeautifulSoup(page,'html.parser')

        #coin price-------------------------------------------------------------
        records = soup.find('div',class_='sc-16r8icm-0 nds9rn-0 dAxhCK').find('div',class_='sc-16r8icm-0 fmPyWa').find('table').find('tbody').find_all('tr')
        coinprice = records[0].find('td').text
        temp = ''
        for i in str(coinprice):
            if i.isnumeric() or i=='.':
                temp += i
        url0 = 'https://www.calculator.net/currency-calculator.html?eamount='+temp+'&efrom=USD&eto='+curr.upper()+'&ccmajorccsettingbox=1&type=1&x=80&y=31'
        response0 = requests.get(url0)
        page0 = response0.text
        response0.close()
        soup0 = BeautifulSoup(page0,'html.parser')
        coinprice = soup0.find('p',class_='verybigtext').find('font').find('b').text
        #-----------------------------------------------------------------------

        #24h change-------------------------------------------------------------
        change24h = records[1].find('td').find('span').text
        change24hpercent = records[1].find('div').find('span').text
        temp = ''
        signcheck = 1
        for i in str(change24h):
            if i=='-':
                signcheck = 0
            if i.isnumeric() or i=='.':
                temp += i
        url0 = 'https://www.calculator.net/currency-calculator.html?eamount='+temp+'&efrom=USD&eto='+curr.upper()+'&ccmajorccsettingbox=1&type=1&x=80&y=31'
        response0 = requests.get(url0)
        page0 = response0.text
        response0.close()
        soup0 = BeautifulSoup(page0,'html.parser')
        change24h = soup0.find('p',class_='verybigtext').find('font').find('b').text
        #-----------------------------------------------------------------------

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('\n\t'+COLOR['PINK']+'-----------------------------------------------------'+COLOR['ENDC'])
        print('\tDate: '+str(date.today())+'   Time: '+current_time+' IST\n')
        print('\t'+COLOR['YELLOW']+coinname+COLOR['ENDC']+'\t'+currsymb+str(coinprice))
        if signcheck==1:
            print('\t24H: '+COLOR['GREEN']+'▲ '+change24hpercent+COLOR['ENDC']+' (+'+currsymb+change24h+')')
        else:
            print('\t24H: '+COLOR['RED']+'▼ '+change24hpercent+COLOR['ENDC']+' (-'+currsymb+change24h+')')
        print('\t'+COLOR['PINK']+'-----------------------------------------------------'+COLOR['ENDC'])

        if signcheck==1:
            mess = coinname+' Price : '+currsymb+str(coinprice)+'\n24H Change: ▲ '+change24hpercent+' (+'+currsymb+change24h+')'
        else:
            mess = coinname+' Price : '+currsymb+str(coinprice)+'\n24H Change: ▼ '+change24hpercent+' (-'+currsymb+change24h+')'
        img = acr.lower()+'.ico'
        notification.notify(
            title = 'Crypto Price Notifier',
            message = mess,
            app_icon = img
        )

        time.sleep(inter*60)

print('\n\n\n\n\t'+COLOR['YELLOW']+'|-- Welcome to Crypto Price Notifier --|'+COLOR['ENDC'])

print('\n\t'+COLOR['PINK']+'Choose the cryptocurrency:'+COLOR['ENDC']+'\n')
print('\t\t1.  Bitcoin   (BTC)')
print('\t\t2.  Ethereum  (ETH)')
print('\t\t3.  XRP       (XRP)')
print('\t\t4.  Solana    (SOL)')
print('\t\t5.  Terra     (LUNA)')
print('\t\t6.  Cardano   (ADA)')
print('\t\t7.  Avalanche (AVAX)')
print('\t\t8.  Dogecoin  (DOGE)')
print('\t\t9.  Stellar   (XLM)')
print('\t\t10. SHIBA INU (SHIB)')
print('\t\t11. Litecoin  (LTC)')
print('\t\t12. TRON      (TRX)')
coin = input('\n\t\tEnter choice: ').lower()
if coin in ['1','bitcoin','btc']:
    coin = 'bitcoin'
elif coin in ['2','ethereum','eth']:
    coin = 'ethereum'
elif coin in ['3','xrp','xrp']:
    coin = 'xrp'
elif coin in ['4','solana','sol']:
    coin = 'solana'
elif coin in ['5','terra','luna']:
    coin = 'terra-luna'
elif coin in ['6','cardano','ada']:
    coin = 'cardano'
elif coin in ['7','avalanche','avax']:
    coin = 'avalanche'
elif coin in ['8','dogecoin','doge']:
    coin = 'dogecoin'
elif coin in ['9','stellar','xlm']:
    coin = 'stellar'
elif coin in ['10','shiba inu','shib']:
    coin = 'shiba-inu'
elif coin in ['11','litecoin','ltc']:
    coin = 'litecoin'
elif coin in ['12','tron','trx']:
    coin = 'tron'
else:
    print('\n\t'+COLOR['RED']+'Invalid Choice\n'+COLOR['ENDC'])
    sys.exit()

print('\n\t'+COLOR['PINK']+'Choose the national currency:'+COLOR['ENDC']+'\n')
print('\t\t1. INR(₹) - Indian Rupee')
print('\t\t2. USD($) - United States Dollar')
print('\t\t3. EUR(€) - Euro')
print('\t\t4. GBP(£) - Pound sterling')
print('\t\t5. JPY(¥) - Japanese Yen')
curr = input('\n\t\tEnter choice: ').lower()
if curr in ['1','inr']:
    curr = 'inr'
elif curr in ['2','usd']:
    curr = 'usd'
elif curr in ['3','eur']:
    curr = 'eur'
elif curr in ['4','gbp']:
    curr = 'gbp'
elif curr in ['5','jpy']:
    curr = 'jpy'
else:
    print('\n\t'+COLOR['RED']+'Invalid Choice\n'+COLOR['ENDC'])
    sys.exit()

inter = int(input('\n\t'+COLOR['PINK']+'Enter time interval between notifications in minutes: '+COLOR['ENDC']))
if inter<1:
    print('\n\t'+COLOR['RED']+'Interval cannot be less than 1 minute'+COLOR['ENDC'])
elif inter>100000:
    print('\n\t'+COLOR['RED']+'Interval cannot be greater than 100000 minutes'+COLOR['ENDC'])
else:
    Crypto_Price_Scraper(coin,curr,inter)
sys.exit()
