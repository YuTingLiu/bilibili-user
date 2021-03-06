# -*-coding:utf8-*-

import requests
import json
import random
import sys
import datetime
import time
from imp import reload
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd

def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()


reload(sys)


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
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}
# proxies = {
#     'http': 'http://61.155.164.108:3128',
#     'http': 'http://116.199.115.79:80',
#     'http': 'http://42.245.252.35:80',
#     'http': 'http://106.14.51.145:8118',
#     'http': 'http://116.199.115.78:80',
#     'http': 'http://123.147.165.143:8080',
#     'http': 'http://58.62.86.216:9999',
#     'http': 'http://202.201.3.121:3128',
#     'http': 'http://119.29.201.134:808',
#     'http': 'http://61.155.164.112:3128',
# }
with open("ip_pool.json",'r') as f:
    ip_list = json.load(f)
def get_random_proxies(protocol='http'):
    '''
    Get a random proxies for requests.get.
    '''
    proxy_list = ip_list.get(protocol)
    random_proxies = random.choice(proxy_list)
    return random_proxies

time1 = time.time()
datas = []
for m in range(0, 1999999):  # 26 ,1000   199999999
    urls = []
    for i in range(m * 100, (m + 1) * 100):
        url = 'https://space.bilibili.com/' + str(i)
        urls.append(url)

    print('urls len',len(urls))
    def getsource(url):
        try:
            payload = {
                '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
                'mid': url.replace('https://space.bilibili.com/', '')
            }
            ua = random.choice(uas)
            head = {
                'User-Agent': ua,
                'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))
            }
            jscontent = requests \
                .session() \
                .post('http://space.bilibili.com/ajax/member/GetInfo',
                      headers=head,
                      data=payload,
                      proxies=get_random_proxies()) \
                .text
            time2 = time.time()
            jsDict = json.loads(jscontent)
            print("返回数据")
            print(jsDict)
            statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
            if statusJson == True:
                if 'data' in jsDict.keys():
                    jsData = jsDict['data']
                    mid = jsData['mid']
                    name = jsData['name']
                    sex = jsData['sex']
                    face = jsData['face']
                    coins = jsData['coins']
                    spacesta = jsData['spacesta']
                    birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                    place = jsData['place'] if 'place' in jsData.keys() else 'noplace'
                    description = jsData['description']
                    article = jsData['article']
                    playnum = jsData['playNum']
                    sign = jsData['sign']
                    level = jsData['level_info']['current_level']
                    exp = jsData['level_info']['current_exp']
                    print("Succeed: " + mid + "\t" + str(time2 - time1) + " " + str(len(datas)))
                    try:
                        res = requests.get(
                            'https://api.bilibili.com/x/space/navnum?mid=' + str(mid) + '&jsonp=jsonp').text
                        js_fans_data = json.loads(res)
                        following = js_fans_data['data']['following']
                        fans = js_fans_data['data']['follower']
                    except:
                        following = 0
                        fans = 0
                else:
                    print('no data now')
                try:
                    datas.append([
                                    mid, name, sex, face, coins, spacesta,
                                    birthday, place, description, article,
                                    following, fans, playnum, sign, level, exp])
                except:
                    print('datas append error')
        except:
            print("error ",url)
            pass


    pool = ThreadPool(4)
    try:
        results = pool.map(getsource, urls)
    except Exception:
        print('ConnectionError')
        pool.close()
        pool.join()
        time.sleep(11)
        pool = ThreadPool(4)
        results = pool.map(getsource, urls)
    time.sleep(30)

pool.close()
pool.join()

print(len(datas))
df = pd.DataFrame(datas)
print(df.head())
df.to_csv("billibili.data.csv")