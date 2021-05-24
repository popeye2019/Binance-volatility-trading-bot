import logging
import threading
import time
result_T1=['vide',0,0,0]
result_T2=['vide',0,0,0]
result_T3=['vide',0,0,0]
result_T4=['vide',0,0,0]



def thread_function1(name):
    global result_T1
    local_result_T1 = result_T1
    logging.info("Thread %s: starting", name)
    for i in range (0,10000):
        for j in range (0,10000):
            k=i*j
    local_result_T1=['toto',12,65,'BUY']
    result_T1=local_result_T1
    logging.info("Thread %s: finishing", name)

def thread_function2(name):
    global result_T2
    local_result_T2 = result_T2
    logging.info("Thread %s: starting", name)
    for i in range (0,10000):
        for j in range (0,10000):
            k=i*j
    local_result_T2=['toto',12,65,'BUY']
    result_T2=local_result_T2
    logging.info("Thread %s: finishing", name)

def thread_function3(name):
    global result_T3
    local_result_T3 = result_T3
    logging.info("Thread %s: starting", name)
    for i in range (0,10000):
        for j in range (0,10000):
            k=i*j
    local_result_T3=['toto',12,65,'BUY']
    result_T3=local_result_T3
    logging.info("Thread %s: finishing", name)

def thread_function4(name):
    global result_T4
    local_result_T4 = result_T4
    logging.info("Thread %s: starting", name)
    for i in range (0,10000):
        for j in range (0,10000):
            k=i*j
    local_result_T4=['toto',12,65,'BUY']
    result_T4=local_result_T4
    logging.info("Thread %s: finishing", name)




if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    w = threading.Thread(target=thread_function1, args=(1,))
    x = threading.Thread(target=thread_function1, args=(2,))
    y = threading.Thread(target=thread_function1, args=(3,))
    z = threading.Thread(target=thread_function1, args=(4,))


    logging.info("Main    : before running thread")
    w.start()
    x.start()
    y.start()
    z.start()
    
    logging.info("Main    : wait for the thread to finish")
    print (result_T1)
    w.join()
    
    logging.info("Main    : all done")
    print (result_T1)
    print (result_T2)
    print (result_T3)
    print (result_T4)

