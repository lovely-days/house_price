# encoding:utf-8

# 网络爬虫爬取贝壳网房价数据并存入数据库中
# 爬取中采用 IP 代理池方法规避网页反爬虫检测
# 采用 url 组合方法遍历各网页
# 选择器结合正则匹配方法提取所需数据

from bs4 import BeautifulSoup
import requests
import re

import src.static.py.helper.sql as db_helper

# data counter
count = 0

# house data structure
house = {'id': count + 1, '名称': 'null', '价格/万元': 'null', '单价/元每平方米': 'null', '户型': 'null', '楼层': 'null',
         '朝向': 'null', '类型': 'null', '面积': 'null', '建筑年份': 'null', '小区': 'null', '区域': 'null',
         '经度': 0.0, '纬度': 0.0}

# information array
# array.append
# array = []

# IP pool
# It may needs to be replaced
IP = ["121.233.227.204:9999", "121.237.24.8:3000", "180.119.94.137:9999", "117.91.248.228:9999", "114.226.223.46:9999"]

# composition of url

# region name
# region = ["yunlongqu/", "gulouqu1/", "quanshanqu/","tongshanqu/", "jinshanqiaokaifaqu/", "xinchengqu3/", "jiawangqu/"]
# page nums 1~100
# options
# region = ["p1/", "p2/", "p3/","p4/", "p5/", "p6/", "p7/"]

# range(1,n) n = page nums
# example: https://xz.ke.com/ershoufang/(#region name#)(#page nums#)(#options#)
# Set it manually
# some region data(data_nums>3000) will divide by p1p2p3(Home price level)
for i in range(1, 23):
    url = "https://xz.ke.com/ershoufang/jiawangqu/" + "pg" + str(i)

    if i == 1:
        url = "https://xz.ke.com/ershoufang/jiawangqu/"

    # url test
    # print(url)

    # IP agent
    try:
        wb_data = requests.get(url, proxies={'http': IP[count % 5]}, timeout=6)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        print('success')
        # IP agent test
        # 第一种方式，返回发送请求的IP地址，使用时要在 get() 添加 stream = True
        # print(response.raw._connection.sock.getpeername()[0])
        # 第二种方式,直接返回测试网站的响应数据的内容
        print(wb_data.text)
    except Exception as e:
        print('error', e)

    # wb_data = requests.get(url)
    # soup = BeautifulSoup(wb_data.text, 'lxml')

    for ul in soup.select('.img.VIEWDATA.CLICKDATA.maidian-detail'):
        v = ul['href']

        if v[0] != "h":
            continue

        # house url test
        print(v)

        # house information

        # IP agent
        try:
            house_data = requests.get(v, proxies={'http': IP[(count+1) % 5]}, timeout=6)
            soup = BeautifulSoup(house_data.text, 'lxml')
            print('success')
            # 检测代理IP是否使用成功
            # 第一种方式，返回发送请求的IP地址，使用时要在 get() 添加 stream = True
            # print(response.raw._connection.sock.getpeername()[0])
            # 第二种方式,直接返回测试网站的响应数据的内容
            print(house_data.text)
        except Exception as e:
            print('error', e)

        # house_data = requests.get(v)
        # soup = BeautifulSoup(house_data.text, 'lxml')

        house['id'] = count + 1

        for name in soup.select('body .detailHeader.VIEWDATA h1 '):
            # name test
            # print(name['title'])

            house['名称'] = name['title']

        for price in soup.select('body .price .total'):
            # price test
            # print(price.get_text())

            house['价格/万元'] = price.get_text()

        for unit_price in soup.select('body .unitPriceValue'):
            # unit_price test
            # print(unit_price.get_text())

            house['单价/元每平方米'] = unit_price.get_text()

        for house_info in soup.select('body .houseInfo'):
            room = house_info.select('.room .mainInfo')[0].get_text()
            house['户型'] = room
            # print(room)

            floor = house_info.select('.room .subInfo')[0].get_text()
            house['楼层'] = floor
            # print(floor)

            direction = house_info.select('.type .mainInfo')[0].get_text()
            house['朝向'] = direction
            # print(direction)

            typename = house_info.select('.type .subInfo')[0].get_text()
            house['类型'] = typename
            # print(typename)

            area = house_info.select('.area .mainInfo')[0].get_text()
            house['面积'] = area
            # print(area)

            years = house_info.select('.area .subInfo.noHidden')[0].get_text().replace('\n', '').replace('\r', '')
            house['建筑年份'] = years
            # replace('\n', '').replace('\r', '') to delete Space and Enter
            # print(years)

        for around_info in soup.select('body .aroundInfo '):
            community = around_info.select('.communityName a')[0].get_text()
            house['小区'] = community
            # print(community)

            areaName = around_info.select('.areaName a')[0].get_text() + " " + around_info.select('.areaName a')[
                1].get_text()
            house['区域'] = areaName
            # print(areaName)
            # print(" ")

        # coordinate
        # regex to find data in script
        script = str(soup.select('script')[14])
        # print(script)

        ret = re.findall(r'resblockPosition.*', script)[0]
        # print(ret)

        ret_locate = re.findall(r'\d*[.]\d*', ret)
        # print(ret_longitude[0])
        # print(ret_longitude[1])
        house["经度"] = ret_locate[0]
        house["纬度"] = ret_locate[1]

        # house test
        for m in house:
            print(house[m])

        # sql statement
        # Synchronized insertion of houses table and records table
        sql_houses = "INSERT INTO webgis_design.houses (HouseID, HouseName, Price, " \
                     "UnitPrice, Roomtype, Floor, Direction, HouseType, Area, Years, Community, " \
                     "Region, Longtitude, Latitude) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}'," \
                     "'{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(
                        house['id'], house['名称'], house['价格/万元'], house['单价/元每平方米'], house['户型'],
                        house['楼层'], house['朝向'], house['类型'], house['面积'], house['建筑年份'], house['小区'],
                        house['区域'], house['经度'], house['纬度'])

        sql_records = "INSERT INTO webgis_design.records (RecordID,TrafficIndex," \
                      "EducationIndex,EnvironmentIndex,DistrictIndex) VALUES ('{0}',{1},{2},{3},{4})".format(
                        house['id'], 0, 0, 0, 0)

        # insert statement
        db_helper.update_database(sql_houses)
        db_helper.update_database(sql_records)

        # count update
        count = count + 1
        # print(count)

        # array not use
        # array.append(house)
        print("第 " + str(house['id']) + " 个数据")
        print("")

# mysql
# db = pymysql.connect(host='localhost', user='root', password='ZyW106509', database='exp')
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print('Database version:{0}'.format(data))
