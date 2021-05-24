from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob

import time
import threading
lock = threading.Lock()


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

def analyze(pairs):
    taMax = 0
    taMaxCoin = 'none'
    signal_coins = {}
    first_analysis = {}
    second_analysis = {}
    third_analysis={}
    first_handler = {}
    second_handler = {}
    third_handler = {}

    lock.acquire()
    if os.path.exists('signals/signalsample.exs'):
        os.remove('signals/signalsample.exs')
    lock.release()

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
        fourth_tacheck = buy_indicator
        index = index +1
        if FULL_LOG:
            print(f'{pair} First {first_tacheck} Second {second_tacheck} Third {third_tacheck}')
        else:
            print(f".{index}.", end = '')
        
        list_coin=[pair,first_tacheck,second_tacheck,third_tacheck,fourth_tacheck]
        dictionary_coin.append (list_coin)

#Begining of choice.............................

    if FULL_LOG: print (dictionary_coin)
    if FULL_LOG: print (f'{txcolors.WARNING} Trié par nom {txcolors.DEFAULT}')
    if FULL_LOG: dictionary_coin.sort()
    if FULL_LOG: print (dictionary_coin)
    print (f'{txcolors.WARNING}First 1 mins check higher{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[1],reverse=True)
    for elem in dictionary_coin:
        if elem[1] >= TA_BUY_THRESHOLD:
            print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}' )    
    if FULL_LOG: print (dictionary_coin[0:4])
    print (f'{txcolors.WARNING}second 5 mins check higher{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[2],reverse=True)
    for elem in dictionary_coin:
        if elem[2] >= TA_BUY_THRESHOLD:
            print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}' )    
    if FULL_LOG: print (dictionary_coin[0:4])
    print (f'{txcolors.WARNING}third 15 mins MACD check{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[3],reverse=True)
    for elem in dictionary_coin:
        if elem[3]>0:
            print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}')    
    if FULL_LOG: print (dictionary_coin[0:4])
    print (f'{txcolors.WARNING}Fourth 15 mins indicator check{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[4],reverse=True)
    for elem in dictionary_coin:
        if elem[4]=="BUY":
            print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}')       
    if FULL_LOG: print (dictionary_coin[0:4])
    #####################################create a virtual indicator
    dictionary_coin.sort()
    for elem in dictionary_coin:
        magique=(elem[2]*1.1)+(elem[1]*1.0)+(elem[3])
        if elem[4] == "STRONG_BUY":
            magique = magique +5
        if elem[4] == "BUY":
            magique = magique +2
        if elem[4] == "NEUTRAL":
            magique = magique +0
        if elem[4] == "SELL":
            magique = magique -2
        if elem[4] == "STRONG_SELL":
            magique = magique -5
        elem.append(magique)
    print (f'{txcolors.WARNING}Liste by magique counter{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[5],reverse=True)
    for elem in dictionary_coin:
        if elem[5]> 31.0:
            print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}')
    if FULL_LOG: print (dictionary_coin[0:4])
    print (f'{txcolors.WARNING}List to buy{txcolors.DEFAULT}')    
    for elem in dictionary_coin:
        if elem[5] >= 31.0:
            print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}' )    
    #print (dictionary_coin[0:4])
    lock.acquire()
    limit_sortie=1
    with open('signals/signalsample.exs','a+') as f:
        for elem in dictionary_coin:
            if ((elem[5] >= 31.0) and (limit_sortie <= 5)):
                limit_sortie=limit_sortie+1
                #f.write(elem[0] + '\n' )
                print (f'signalpopeye: {elem[0]}')
    f.close()
    lock.release()   
    
    
    
    return signal_coins

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    tps1 = time.time()
    signal_coins = {}
    pairs = {}
    decoupe_pairs={}

    pairs=[line.strip() for line in open(TICKERS)]
    for line in open(TICKERS):
        pairs=[line.strip() + PAIR_WITH for line in open(TICKERS)] 
    
    pairs=pairs [0:11]
    print (pairs)
    
    print(f'Analyzing {len(pairs)} coins')
    signal_coins = analyze(pairs)
    if len(signal_coins) == 0:
        print(f'No coins above {TA_BUY_THRESHOLD} threshold')
    else:
        print(f'{len(signal_coins)} coins above {TA_BUY_THRESHOLD} treshold on both timeframes')
    print(f'Waiting {TIME_TO_WAIT} minutes for next analysis')
    tps2 = time.time()
    print(tps2 - tps1)
