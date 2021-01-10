import requests
from lxml import etree
import time
import csv


# 获取经纬度
def getlnglat(address):
    parameters = {'address': address, 'key': 'c175dc11d3da1375a10579d2f96cc5e5'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    json = response.json()
    if json['count'] == '0':
        return ' ', ' '
    else:
        location = json['geocodes'][0]['location'].split(',')
        return location[0], location[1]

def getData():
    # 设置爬取开始时间及url与包头
    start_time = time.time()
    url = 'https://gaokao.chsi.com.cn/sch/search.do?searchType=1&start='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
    }

    # 写入csv文件的表头
    with open("data.csv", 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['院校名称', '院校所在地', '院校隶属', '院校类型', '学历层次', '经度', '纬度'])
    start = 0
    count = 0
    while start <= 2720:
        # 爬取，一页20条信息
        response = requests.get(url + str(start), headers=headers)
        start += 20
        html = etree.HTML(response.text)
        university_list = []

        for university in html.xpath('//tr[td]'):
            university_name = university.xpath('./td/a')[0].text.strip()
            university_addr = university.xpath('./td')[1].text.strip()
            university_agency = university.xpath('./td')[2].text.strip()
            university_type = university.xpath('./td')[3].text.strip()
            university_level = university.xpath('./td')[4].text.strip()
            university_lng, university_lat = getlnglat(university_name)
            university_list = [university_name, university_addr, university_agency, university_type,
                               university_level, university_lng, university_lat]
            print(university_list)
            with open("data.csv", 'a', newline='') as f:  # 写入csv文件
                csv_writer = csv.writer(f)
                csv_writer.writerow(university_list)

            count += 1

    end_time = time.time()
    print("共花费 {} S, 爬取 {} 座高校".format(end_time - start_time, count))


def __main__():
    getData()
