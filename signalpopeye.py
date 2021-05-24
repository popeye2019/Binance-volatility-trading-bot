from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob
import asyncio
import time
from datetime import date, datetime, timedelta

import json

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

#old_out = sys.stdout
#class St_ampe_dOut:
#    """Stamped stdout."""
#    nl = True
#    def write(self, x):
#        """Write function overloaded."""
#        if x == '\n':
#            old_out.write(x)
#            self.nl = True
#        elif self.nl:
#            old_out.write(f'{txcolors.DIM}[{str(datetime.now().replace(microsecond=0))}]{txcolors.DEFAULT} {x}')
#            self.nl = False
#        else:
#            old_out.write(x)
#
#    def flush(self):
#        pass
#sys.stdout = St_ampe_dOut()

NB_THREAD=5

MY_EXCHANGE = 'BINANCE'
MY_SCREENER = 'CRYPTO'
MY_FIRST_INTERVAL = Interval.INTERVAL_1_MINUTE
MY_SECOND_INTERVAL = Interval.INTERVAL_5_MINUTES
MY_THIRD_INTERVAL = Interval.INTERVAL_5_MINUTES

TA_BUY_THRESHOLD = 16 # How many of the 26 indicators to indicate a buy
POP_TRESHOLD = 12 + 17 +5
MAX_COINS_PER_SCAN = 3
PAIR_WITH = 'USDT'
TICKERS = 'signalsample.txt'
TIME_TO_WAIT = 1 # Minutes to wait between analysis
FULL_LOG = False # List anylysis result to console
async def run(shell_command):
    p = await asyncio.create_subprocess_shell(shell_command)
    await p.communicate()


async def main(shell_commands):
    for f in asyncio.as_completed([run(c) for c in shell_commands]):
        await f


def analyze(dictionary_coin):
    signal_coins = {}
    count_sortie=1
    #Begining of choice.............................

    if FULL_LOG: print (dictionary_coin)
    if FULL_LOG: print (f'{txcolors.WARNING} Trié par nom {txcolors.DEFAULT}')
    if FULL_LOG: dictionary_coin.sort()
    if FULL_LOG: print (dictionary_coin)
    
    print (f'{txcolors.WARNING}First 1 mins check higher{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[1],reverse=True)
    if FULL_LOG:
        for elem in dictionary_coin:
            if elem[1] >= TA_BUY_THRESHOLD:
                print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}' )    
    if not FULL_LOG: print (dictionary_coin[0:MAX_COINS_PER_SCAN])
    
    print (f'{txcolors.WARNING}second 5 mins check higher{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[2],reverse=True)
    if FULL_LOG:
        for elem in dictionary_coin:
            if elem[2] >= TA_BUY_THRESHOLD:
                print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}' )    
    if  not FULL_LOG: print (dictionary_coin[0:MAX_COINS_PER_SCAN])
    
    print (f'{txcolors.WARNING}third 15 mins MACD check{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[3],reverse=True)
    if FULL_LOG:
        for elem in dictionary_coin:
            if (elem[3]>0.0):                  
                print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}')    
    if not FULL_LOG: print (dictionary_coin[0:MAX_COINS_PER_SCAN])
    
    print (f'{txcolors.WARNING}Fourth 15 mins indicator check{txcolors.DEFAULT}')
    dictionary_coin.sort(key=lambda a: a[4],reverse=True)
    if FULL_LOG:
        for elem in dictionary_coin:
            if elem[4]=="BUY":
                print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}')       
    if not FULL_LOG: print (dictionary_coin[0:MAX_COINS_PER_SCAN])
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
    if FULL_LOG:
        for elem in dictionary_coin:
            if elem[5]> 31.0:
                print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}')
    if not FULL_LOG: print (dictionary_coin[0:MAX_COINS_PER_SCAN])
    print (f'{txcolors.WARNING}List to buy{txcolors.DEFAULT}')    
    for elem in dictionary_coin:
        if elem[5] >= 31.0:
            print (f'{txcolors.BUY}{elem}{txcolors.DEFAULT}' )    
    #print (dictionary_coin[0:4])

#=======================================================vers le bot
    lock.acquire()
    with open('signals/signalsample.exs','a+') as f:
        for elem in dictionary_coin:
            if ((elem[5] >= 31.0) and (count_sortie <= MAX_COINS_PER_SCAN)):
                count_sortie += 1
                f.write(elem[0] + '\n' )
                if FULL_LOG: print (f'signalpopeye: {elem}')
    f.close()
    lock.release()   
    
    return signal_coins

def do_work():

#clean repertoire Json
#    fichiers = glob.glob('./json/*.json')
#        for f in fichiers:
#            try:
#                os.remove(f)
#            except OSError as e:
#                print("Error: %s : %s" % (f, e.strerror)) 
                

    signal_coins = {}
    pairs = {}
    commands=[]
    pairs=[line.strip() for line in open(TICKERS)]
    for line in open(TICKERS):
        pairs=[line.strip() + PAIR_WITH for line in open(TICKERS)] 

    while True:
    #Launch Download================================================    
        tps1=time.time()
        process=0
        first_index=0

        commands=[]
        for i in range (0+NB_THREAD,len(pairs)+NB_THREAD,NB_THREAD):
            fin = i -1
            if (fin>=len(pairs)) : fin = (len(pairs) -1)
            #print (f'process: {process} debut: {first_index} fin: {fin}')
            command_to_append=('python signalpop1.py -d '+str(first_index)+' -f '+str(fin))
            #print (command_to_append)
            commands.append(command_to_append)
            first_index=i
            process +=1
                
        #commands = ['python signalpop1.py -d 0 -f 5','python signalpop1.py -d 19 -f 24']


        loop = asyncio.ProactorEventLoop()
        loop.run_until_complete(main(commands))
        loop.close()

        tps2 = time.time()
        print(f'Temps de requete : {(tps2 - tps1)}')
#Launch association================================================
        process=0
        first_index=0
        commands=[]
#=======================================generate filename
        for i in range (0+NB_THREAD,len(pairs)+NB_THREAD,NB_THREAD):
            fin = i -1
            if (fin>=len(pairs)) : fin = (len(pairs) -1)
            #print (f'fichier_recup: {process} debut: {first_index} fin: {fin}')
            command_to_append=('./json/coins'+str(first_index)+'-'+str(fin)+'.json')
            #print (command_to_append)
            commands.append(command_to_append)
            first_index=i
            process +=1
#===========================================read and add to dictionary_coin
        dictionary_coin=[]
        for file_name in commands:
            with open(file_name, 'r') as j:
                contents = json.loads(j.read())
                dictionary_coin=dictionary_coin+contents
            j.close()
            #os.remove(file_name)
#===============Remove all .json file
        fichiers = glob.glob('./json/*.json')
        for f in fichiers:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))           
            
        #print("==========================================================")
        #print (dictionary_coin)
        signal_coins = analyze(dictionary_coin)
        print(f'Waiting {TIME_TO_WAIT} minutes for next analysis')
        time.sleep((TIME_TO_WAIT*60))    
        
    #end of recup
    #    while True:
    #        print(f'Analyzing {len(pairs)} coins')
    #        signal_coins = analyze(pairs)
    #        if len(signal_coins) == 0:
    #            print(f'No coins above {TA_BUY_THRESHOLD} threshold')
    #        else:
    #            print(f'{len(signal_coins)} coins above {TA_BUY_THRESHOLD} treshold on both timeframes')
    #        print(f'Waiting {TIME_TO_WAIT} minutes for next analysis')
    #        time.sleep((TIME_TO_WAIT*60))
