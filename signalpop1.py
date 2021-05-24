from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
# use if needed to pass args to external modules
import sys

import argparse
# used for directory handling
import json

import time
from datetime import date, datetime, timedelta


# for colourful logging to the console
class txcolors:
    BUY = '\033[92m'
    WARNING = '\033[93m'
    SELL_LOSS = '\033[91m'
    SELL_PROFIT = '\033[32m'
    DIM = '\033[2m\033[35m'
    DEFAULT = '\033[39m'
    
from colorama import init
init()

# print with timestamps
old_out = sys.stdout
class St_ampe_dOut:
    """Stamped stdout."""
    nl = True
    def write(self, x):
        """Write function overloaded."""
        if x == '\n':
            old_out.write(x)
            self.nl = True
        elif self.nl:
            old_out.write(f'{txcolors.DIM}[{str(datetime.now().replace(microsecond=0))}]{txcolors.DEFAULT} {x}')
            self.nl = False
        else:
            old_out.write(x)

    def flush(self):
        pass

sys.stdout = St_ampe_dOut()


MY_EXCHANGE = 'BINANCE'
MY_SCREENER = 'CRYPTO'
MY_FIRST_INTERVAL = Interval.INTERVAL_1_MINUTE
MY_SECOND_INTERVAL = Interval.INTERVAL_5_MINUTES
MY_THIRD_INTERVAL = Interval.INTERVAL_5_MINUTES

TA_BUY_THRESHOLD = 10 # How many of the 26 indicators to indicate a buy
PAIR_WITH = 'USDT'
TICKERS = 'signalsample.txt'
TIME_TO_WAIT = 0.1 # Minutes to wait between analysis
FULL_LOG = False # List anylysis result to console

def download(pairs):
    taMax = 0
    taMaxCoin = 'none'
    signal_coins = {}
    first_analysis = {}
    second_analysis = {}
    third_analysis={}
    first_handler = {}
    second_handler = {}
    third_handler = {}

    list_coin=[]
    dictionary_coin= []
        

    for pair in pairs:
        first_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FIRST_INTERVAL,
            timeout= 10
        )
        second_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_SECOND_INTERVAL,
            timeout= 10
        )
        third_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_THIRD_INTERVAL,
            timeout= 10
        )
        
    index=0
       
    for pair in pairs:
        try:
            first_analysis = first_handler[pair].get_analysis()
            second_analysis = second_handler[pair].get_analysis()
            macd_line = third_handler[pair].get_analysis().indicators['MACD.macd']
            macd_signal = third_handler[pair].get_analysis().indicators['MACD.signal']
            buy_indicator = third_handler[pair].get_analysis().summary['RECOMMENDATION']
        except Exception as e:
                    print("Exeption:")
                    print(e)
                    print (f'Coin: {pair}')
                    print (f'First handler: {first_handler[pair]}')
                    print (f'Second handler: {second_handler[pair]}')
                    tacheckS = 0
                
        first_tacheck = first_analysis.summary['BUY']
        second_tacheck = second_analysis.summary['BUY']
        third_tacheck = macd_line - macd_signal
        if third_tacheck>100.0 : third_tacheck=0.0
        fourth_tacheck = buy_indicator
        index = index +1
        if FULL_LOG:
            print(f'{pair} First {first_tacheck} Second {second_tacheck} Third {third_tacheck}')
            print(f".{index}.", end = '')
        
        list_coin=[pair,first_tacheck,second_tacheck,third_tacheck,fourth_tacheck]
        dictionary_coin.append (list_coin)
        try:
            file_name='./json/coins'+str(val_debut)+'-'+str(val_fin)+'.json'
            fichier = open(file_name, 'w+')
        except:
            print (f"oups file pb")
        json.dump(dictionary_coin, fichier)
        
        fichier.close()

    
    
    return

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debut")
    parser.add_argument("-f", "--fin")
    args = parser.parse_args()
    if ((args.debut is None) or (args.fin is None)):
        parser.error(f"Veuillez specifiez depart et fin du fichier à analyser -d inclus  -f exclus.")
        quit()
    val_debut=int(args.debut)
    val_fin= int(args.fin)
    
    tps1 = time.time()
    signal_coins = {}
    pairs = {}
    pairs=[line.strip() for line in open(TICKERS)]
    for line in open(TICKERS):
        pairs=[line.strip() + PAIR_WITH for line in open(TICKERS)] 
    pairs=pairs[val_debut:val_fin]
    #print (pairs)
    #print(f'Downloading {len(pairs)} coins')
    download(pairs)
    tps2 = time.time()
    #print(f'Temps de requete {(tps2 - tps1):.2f}')
    sys.exit()
