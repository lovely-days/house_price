# encoding:utf-8

import src.static.py.helper.sql as db_helper
import src.static.py.helper.co_system as coordinate_helper

sql_dic = {'region': ['', '\'.*云龙区.*\'', '\'.*鼓楼区.*\'', '\'.*铜山区.*\'', '\'.*泉山区.*\'', '\'.*金山桥开发区.*\'', '\'.*新城区.*\'', '\'.*贾汪区.*\''],
           'roomtype': ['', '\'.*[1]室.*\'', '\'.*[1-2]室.*\'', '\'.*[1-3]室.*\'', '\'.*[1-4]室.*\'', '\'.*[1-5]室.*\''],
           'area': ['', '<50', 'between 50 and 80', 'between 80 and 120', 'between 120 and 150', '>150'],
           'all_price': ['', '<50', 'between 50 and 100', 'between 100 and 150', '>150'],
           'unit_price': ['', '<5000',  'between 5000 and 10000', 'between 10000 and 15000', 'between 15000 and 20000', '>20000'],
           'direction': ['', '\'.*南.*\'', '\'.*东.*\'', '\'.*北.*\'', '\'.*西.*\''],
           'floor': ['', '\'.*低楼层.*\'', '\'.*中楼层.*\'', '\'.*高楼层.*\''],
           'house_type': ['', '\'.*精装.*\'', '\'.*简装.*\'', '\'.*毛坯.*\'', '\'.*其他.*\'']}


# 拼接形成查询所用 sql 语句
def get_sql(dic={}):
    sql = "select * from houses "

    # 当区域全选时存在 bug, 懒得改了，直接删了全选选项

    # 区域
    if int(dic['region']) != 0:
        sql = sql + "where Region regexp " + sql_dic['region'][int(dic['region'])] + " "

    # 室数目
    if int(dic['roomtype']) != 0:
        sql = sql + "and RoomType regexp " + sql_dic['roomtype'][int(dic['roomtype'])] + " "

    # 面积
    if int(dic['area']) != 0:
        sql = sql + "and Price*10000/UnitPrice " + sql_dic['area'][int(dic['area'])] + " "

    # 总价
    if int(dic['all_price']) != 0:
        sql = sql + "and Price " + sql_dic['all_price'][int(dic['all_price'])] + " "

    # 单价
    if int(dic['unit_price']) != 0:
        sql = sql + "and UnitPrice " + sql_dic['unit_price'][int(dic['unit_price'])] + " "

    # 朝向
    if int(dic['direction']) != 0:
        sql = sql + "and Direction regexp " + sql_dic['direction'][int(dic['direction'])] + " "

    # 楼层
    if int(dic['floor']) != 0:
        sql = sql + "and Floor regexp " + sql_dic['floor'][int(dic['floor'])] + " "

    # 装修情况
    if int(dic['house_type']) != 0:
        sql = sql + "and HouseType regexp " + sql_dic['house_type'][int(dic['house_type'])] + " "

    print(sql)
    return sql


# 查询房屋点坐标数据并返回对应 json 格式
# input: 标志数组
# output: 对应 Geojson 格式数据

def select_coordinate_geo(dic={}):
    sql_house = get_sql(dic)
    db_house = db_helper.select_all(sql_house)

    # 0 19304 1 文化名园 3室3厅南 2 48.8 3 3461 4 3室3厅 5 高楼层 / 共5层 6 南 7 暂无数据 / 精装 8 141平米 9 2008年建 / 板塔结合
    # 10 文化名园 11 贾汪区贾汪 12 117.464858 13 34.444896

    # 0 4467 1 三胞广场 2 Shopping 3 117.194196 4 34.223977

    features = []

    for item in db_house:
        coordinates = coordinate_helper.bd09_to_wgs84(float(item[12]), float(item[13]))
        properties = {"House ID": item[0], "House Name": item[1], "Price": item[2], "Unit Price": item[3],
                      "Room Type": item[4], "Floor": item[5], "Direction": item[6], "House Type": item[7],
                      "Area": item[8], "Years": str(item[9]).strip(), "Community": item[10], "Region": item[11]}
        feature = {"type": "Feature",
                   "geometry": {
                       "type": "Point",
                       "coordinates": coordinates
                   },
                   "properties": properties
                   }

        features.append(feature)

    json_return = {"type": "FeatureCollection", "features": features}
    # print(features)

    return json_return


'''
test_dic = {'region': '1', 'roomtype': '0', 'area': '3', 'all_price': '3', 'unit_price': '3', 'direction': '1', 'floor': '1',
            'house_type': '1'}

select_coordinate_geo(test_dic)
'''



