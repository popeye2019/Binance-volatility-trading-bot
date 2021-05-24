import logging
from threading import Thread, Lock, current_thread
from queue import Queue
import time
from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob

import time
#lock = threading.Lock()

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
FULL_LOG = True # List anylysis result to console


result_T1=['vide',0,0,0]
result_T2=['vide',0,0,0]
result_T3=['vide',0,0,0]
result_T4=['vide',0,0,0]

class MyThread(threading.Thread):
    def __init__(self, number):
        super(MyThread, self).__init__()
        self.number = number
    def run(self):
        print (self.number)

def thread_function(q,lock):
    
    first_analysis = {}
    first_handler = {}    
    while True:
        pair=q.get()
        with lock:
            ttps1 = time.time()
            first_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FIRST_INTERVAL,
            timeout= 10)
            try:
                first_analysis = ('titi')#first_handler[pair].get_analysis()
                for j in range (10000):
                    for k in range (10000):
                        pass
            except Exception as e:
                print("Exeption:")
                print(e)
                print (f'Coin: {pair}')
                print (f'First handler: {first_handler[pair]}')
            first_tacheck = ('toto') #first_analysis.summary['BUY']
            print(f'{pair} First {first_tacheck}')
            list_coin=[pair,first_tacheck]
            #a locker copier modifier copier unlocker
            #dictionary_coin.append (list_coin)


        ttps2 = time.time()   
        print (f"dans {current_thread().name} j'analyse {pair} duree: {ttps2-ttps1}")
 
        q.task_done()
        




if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    tps1 = time.time()

    signal_coins = {}
    pairs = {}
    q= Queue()
    num_threads = 2
    lock=Lock()
    
    pairs=[line.strip() for line in open(TICKERS)]
    for line in open(TICKERS):
        pairs=[line.strip() + PAIR_WITH for line in open(TICKERS)] 
    print(f'Analyzing {len(pairs)} coins')
    #while True:

    for i in range(num_threads):
        t = Thread(name=f"Thread{i+1}", target = thread_function ,args=(q,lock))
        t.daemon=True
        print (i)
        t.start()
    print (f"Les {num_threads} sont lancés")
    for x in range(len(pairs)):
        q.put(pairs[x])
        print (f'x:{x} pairs:{pairs[x]}')
      
    q.join()

tps1 = time.time()
    tps2 = time.time()
    print(tps2 - tps1)
    print ('fini')





