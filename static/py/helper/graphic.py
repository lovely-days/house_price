# encoding:utf-8

from geopy.distance import geodesic

import src.static.py.helper.sql as db_helper
import src.static.py.helper.co_system as coordinate_helper


# 获取房价点序号及坐标数据
# input: null
# output: 房价点序号及坐标数据数组
def get_house_id():
    sql_house = "select * from houses"
    db_house = db_helper.select_all(sql_house)

    # 0 19304 1 文化名园 3室3厅南 2 48.8 3 3461 4 3室3厅 5 高楼层 / 共5层 6 南 7 暂无数据 / 精装 8 141平米 9 2008年建 / 板塔结合
    # 10 文化名园 11 贾汪区贾汪 12 117.464858 13 34.444896

    house_data = []

    for item in db_house:
        coordinate = coordinate_helper.bd09_to_wgs84(float(item[12]), float(item[13]))
        house_data.append({"HouseID":item[0], "coordinate": coordinate})

    return house_data


# 获取全部房价点数据
# input: null
# output: 房价数据数组
def get_all_house_data():
    sql_house = "select * from houses"
    db_house = db_helper.select_all(sql_house)

    # 0 19304 1 文化名园 3室3厅南 2 48.8 3 3461 4 3室3厅 5 高楼层 / 共5层 6 南 7 暂无数据 / 精装 8 141平米 9 2008年建 / 板塔结合
    # 10 文化名园 11 贾汪区贾汪 12 117.464858 13 34.444896

    all_house_data = []

    for item in db_house:
        coordinate = coordinate_helper.bd09_to_wgs84(float(item[12]), float(item[13]))
        house_data = {"House ID": item[0], "House Name": item[1], "Price": item[2], "Unit Price": item[3],
                      "Room Type": item[4], "Floor": item[5], "Direction": item[6], "House Type": item[7],
                      "Area": item[8], "Years": str(item[9]).strip(), "Community": item[10], "Region": item[11],
                      "Coordinate":coordinate}
        all_house_data.append(house_data)


    return all_house_data


# 查询圆范围内房价点数据
# input: 查询条件字典，圆心坐标及半径
# output: 对应房价点 json 数据
def circle(condition={}):
    radius = condition["select_condition"][3]
    coordinate = [condition["select_condition"][0], condition["select_condition"][1]]

    house_id_coordinate = get_house_id()
    all_house_data = get_all_house_data()
    return_data = []
    features = []

    for i,item in house_id_coordinate:
        distance = geodesic((item["coordinate"][1], item["coordinate"][0]),(coordinate[1],coordinate[0])).km
        if distance <= radius:
            return_data.append(all_house_data[i])

    for item in return_data:
        feature = {"type": "Feature",
                   "geometry": {
                       "type": "Point",
                       "coordinates": [item["Coordinate"]]
                   },
                   "properties": item
                   }

        features.append(feature)

    json_return = {"type": "FeatureCollection", "features": features}
    # print(features)

    return json_return


# 查询矩形范围内房价点数据
# input: 查询条件字典，矩形对角线上两点，默认采用左上及右下坐标方法
# output: 对应房价点 json 数据
def rectangle(condition={}):
    max_longitude = max(float(condition["select_condition"][0][0]), float(condition["select_condition"][1][0]))
    min_longitude = min(float(condition["select_condition"][0][0]), float(condition["select_condition"][1][0]))
    max_latitude = min(float(condition["select_condition"][0][1]), float(condition["select_condition"][1][1]))
    min_latitude = min(float(condition["select_condition"][0][1]), float(condition["select_condition"][1][1]))

    house_id_coordinate = get_house_id()
    all_house_data = get_all_house_data()
    return_data = []
    features = []

    for i, item in house_id_coordinate:
        if min_longitude < item["Coordinate"][0] < max_longitude \
                and min_latitude < item["Coordinate"][1] < max_latitude:
            return_data.append(all_house_data[i])

    for item in return_data:
        feature = {"type": "Feature",
                   "geometry": {
                       "type": "Point",
                       "coordinates": [item["Coordinate"]]
                   },
                   "properties": item
                   }

        features.append(feature)

    json_return = {"type": "FeatureCollection", "features": features}
    # print(features)

    return json_return


# 查询多边形内房价点数据
# input:  多边形点坐标集合，以 [-1,-1] 结束
# output: 对应房价点 json 数据
def polygon(condition={}):
    coordinate = condition["select_condition"]

    house_id_coordinate = get_house_id()
    all_house_data = get_all_house_data()
    return_data = []
    features = []

    for i, item in house_id_coordinate:
        distance = geodesic((item["coordinate"][1], item["coordinate"][0]), (coordinate[1], coordinate[0])).km
        if distance <= radius:
            return_data.append(all_house_data[i])

    for item in return_data:
        feature = {"type": "Feature",
                   "geometry": {
                       "type": "Point",
                       "coordinates": [item["Coordinate"]]
                   },
                   "properties": item
                   }

        features.append(feature)

    json_return = {"type": "FeatureCollection", "features": features}
    # print(features)

    return json_return
