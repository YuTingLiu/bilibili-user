import requests
from bs4 import BeautifulSoup as bs
import re
import queue as Queue
import threading
import time
import optparse
from collections import defaultdict
import json

url = 'http://www.xicidaili.com/nn/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'}

avili_urls = []
class Proxy_collection(threading.Thread):   #继承Thread实现多线程

    def __init__(self, que):
        threading.Thread.__init__(self)   #重用父类Thread的__init__()
        self._que = que

    def run(self):
        while not self._que.empty():
            url = self._que.get()
            r = requests.get(url, headers=headers, timeout=5)
            soup = bs(r.content, 'lxml', from_encoding='utf-8')
            bqs = soup.find_all(name='tr', attrs={'class':re.compile(r'|[^odd]')})
            for bq in bqs:

                us = bq.find_all(name='td')
                try:
                    print(str(us[5].string), str(us[1].string), str(us[2].string))
                    avili_urls.append(" ".join([str(us[5].string),str(us[1].string), str(us[2].string)]))
                #                     self.proxies_confirm(str(us[5].string), str(us[1].string), str(us[2].string))   #取协议：ip：端口去验证
                except Exception as e:
                    #print e
                    pass

def proxies_confirm(type_self, ip, port):
    proxies = { type_self.lower(): '{}://{}:{}'.format(type_self.lower(), ip, port) }

    r = requests.get('http://1212.ip138.com/ic.asp', headers=headers, proxies=proxies, timeout=5)
    #     print(r.text)
    result = re.findall(r'\d+\.\d+\.\d+\.\d+', r.text)
    result_ip = ''.join(result)   #转为字符串
    print(ip + "find "+result_ip)
    if len(result_ip)>1:
        return True
    else:
        return False

if __name__ == '__main__':
    thread = []

    que = Queue.Queue()
    pagenum = 5
    for i in range(1, pagenum+1):
        que.put('http://www.xicidaili.com/nn/' + str(i))

    for i in range(pagenum):
        thread.append(Proxy_collection(que))
    start = time.clock()
    for i in thread:
        i.start()
    for i in thread:
        i.join()

    end = time.clock()
    print(end - start)

    ip_list = defaultdict(list)
    for l in avili_urls:
        prot,ip,port = l.strip().split(' ')
        try:
            if proxies_confirm(prot,ip,port):
                proxies = { prot: '{}://{}:{}'.format(prot, ip, port) }
                ip_list[prot].append(proxies)
        except:
            pass
    with open("valid_proxies.json",'w') as f:
        json.dump(ip_list,f)
