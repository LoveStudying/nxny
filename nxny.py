import os
import urllib3
import time
from lxml import etree  # 导入html树形结构转换模块
from urllib.parse import urljoin

start_urls = ['http://www.nxny.com/stype_dp/', 'http://www.nxny.com/stype_dp_p2/',
              'http://www.nxny.com/stype_dp_p3/']

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': 'td_cookie=1285411694; okstockusertype=0; okstockuserid=083A19834E2BC073; okstockmail=445680803@qq.com; okstockvipendtime=497F792C6667303CB1AB079BB098B7D190D965B9E63F8675; Hm_lvt_5a7f5b2b7919015119e8a201e15e779f=1571296905,1571310736,1571366079,1571628411; td_cookie=1283208733; Hm_lpvt_5a7f5b2b7919015119e8a201e15e779f=1571638451',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}
# 一个PoolManager实例来生成请求, 由该实例对象处理与线程池的连接以及线程安全的所有细节
http = urllib3.PoolManager()
timeStr = time.strftime("%y%m%d")

def download(url):
    response = http.request('Get', url).data.decode()
    html = etree.HTML(response)
    for detailUrl in html.xpath("//a[contains(@title,'国泰君安')and contains(@title,'" + timeStr + "')]/@href"):
        download_url_deal(detailUrl)
    for detailUrl in html.xpath("//a[contains(@title,'浙商证券')and contains(@title,'" + timeStr + "')]/@href"):
        download_url_deal(detailUrl)
    for detailUrl in html.xpath("//a[contains(@title,'中信证券')and contains(@title,'" + timeStr + "')]/@href"):
        download_url_deal(detailUrl)


def download_url_deal(url):
    time.sleep(2)
    url=urljoin('http://www.nxny.com', url)
    response = http.request('Get', urljoin('http://www.nxny.com', url), headers=headers).data.decode()
    html = etree.HTML(response)
    for downloadUrl in html.xpath('//tr[5]/td/a/@href'):
        fileName = html.xpath('//tr[1]/td[2]/strong/text()')[0]
        filePath = r'C:\Users\miaoke\Desktop\self\晨会'+'\\'+timeStr+'\\'+fileName+'.pdf'
        file_Deal(downloadUrl, filePath)

def file_Deal(url, filePath):
    response = http.request('Get', url, headers=headers)
    if not os.path.exists(os.path.split(filePath)[0]):
        # 目录不存在创建，makedirs可以创建多级目录
        os.makedirs(os.path.split(filePath)[0])
    # 保存数据到文件
    with open(filePath, 'wb') as f:
        f.write(response.data)

if __name__ == '__main__':
    for url in start_urls:
        download(url)
