import datetime
import random
from  asyncio import async
from imp import reload
from multiprocessing.dummy import Pool as ThreadPool

import aiohttp
import time
import json
import asyncio

import redis
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()

def LoadUserAgents(uafile):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgents("user_agents.txt")
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://space.bilibili.com/45388',
    'Origin': 'https://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}
proxies = {
    'http': 'http://61.155.164.108:3128',
    'http': 'http://116.199.115.79:80',
    'http': 'http://42.245.252.35:80',
    'http': 'http://106.14.51.145:8118',
    'http': 'http://116.199.115.78:80',
    'http': 'http://123.147.165.143:8080',
    'http': 'http://58.62.86.216:9999',
    'http': 'http://202.201.3.121:3128',
    'http': 'http://119.29.201.134:808',
    'http': 'http://61.155.164.112:3128',
}
with open("ip_pool.json",'r') as f:
    ip_list = json.load(f)
def get_random_proxies(protocol='http'):
    '''
    Get a random proxies for requests.get.
    '''
    proxy_list = ip_list.get(protocol)
    random_proxies = random.choice(proxy_list)
    return random_proxies

async  def get_user(proxy,mid=11,red=None):
    url = 'https://space.bilibili.com/' +str(mid)
    payload = {
        '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
        'mid': url.replace('https://space.bilibili.com/', ''),
        'csrf':''
    }
    ua = random.choice(uas)
    head = {
        'User-Agent': ua.decode("utf-8"),
        'Referer': 'https://space.bilibili.com/' +str(mid)
    }
    # print("begin")
    # print(get_random_proxies("http"))
    async with aiohttp.ClientSession() as session:
        async  with session.post(url='http://space.bilibili.com/ajax/member/GetInfo',
                                 data=payload,headers=head,proxy=proxy) as response:
            jdata = await response.text()
            jdata = json.loads(jdata)
            print(jdata)
            red.hmset(mid,jdata)

async def printh():
    print("hello",time.time())

if __name__ == '__main__':
    r = redis.Redis(host='172.17.0.2', port=6379,db=2)
    log = redis.Redis(host='172.17.0.2', port=6379,db=3)
    loop = asyncio.get_event_loop()
    random.shuffle(proxies)
    print("start at :",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    try:
        for i in range(1,1999):
            mid = log.hgetall("last_mid_is")['mid'.encode("utf-8")].decode("utf-8")
            mid = int(mid)+1
            loop.run_until_complete(get_user(proxies["http"],mid,r))
            time.sleep(10)
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            log.hmset("last_mid_is",{"mid":str(mid),"time":t,"proxy":proxies["http"],"count":str(i)})
        loop.close()
    except Exception as e:
        print(e)
        print("except at : ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(printh())
    # loop.close()
    # loop.create_future()