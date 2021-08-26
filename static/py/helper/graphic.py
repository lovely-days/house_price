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
    radius = float(condition["select_condition"][3])
    coordinate = [float(condition["select_condition"][0]), float(condition["select_condition"][1])]

    house_id_coordinate = get_house_id()
    all_house_data = get_all_house_data()
    return_data = []
    features = []

    for i,item in house_id_coordinate:
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


# 查询矩形范围内房价点数据
# input: 查询条件字典，矩形对角线上两点，默认采用左上及右下坐标方法
# output: 对应房价点 json 数据
def rectangle(condition={}):
    max_longitude = max(float(condition["select_condition"][0][0]), float(condition["select_condition"][1][0]))
    min_longitude = min(float(condition["select_condition"][0][0]), float(condition["select_condition"][1][0]))
    max_latitude = max(float(condition["select_condition"][0][1]), float(condition["select_condition"][1][1]))
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


# 射线法查询多边形内房价点数据
# input:  多边形点坐标集合，以 [-1,-1] 结束
# output: 对应房价点 json 数据
def polygon(condition={}):
    # [[longitude, latitude]...]
    coordinates = []

    # 用于优化剪枝
    polygon_longitudes = []
    polygon_latitudes = []

    # 坐标值转为 float 类型数据
    for item in condition["select_condition"]:
        coordinates.append([float(item[0]), float(item[1])])
        polygon_longitudes.append(float(item[0]))
        polygon_latitudes.append(float(item[1]))

    # 剪枝操作
    max_longitude = max(polygon_longitudes)
    min_longitude = min(polygon_longitudes)
    max_latitude = max(polygon_latitudes)
    min_latitude = min(polygon_latitudes)

    house_id_coordinate = get_house_id()
    all_house_data = get_all_house_data()
    return_data = []
    features = []

    # 遍历所有房价点
    for i, item in house_id_coordinate:
        status = 0
        coordinate_i = item["coordinate"]

        # 当点不在最大最小坐标值构成矩形区域内时不可能在区域内，跳过操作
        if coordinate_i[0] > max_longitude or coordinate_i[0] < min_longitude \
                or coordinate_i[1] > max_latitude or coordinate_i[1] < min_latitude:
            continue

        # 在矩形区域内时执行射线法判断是否在多边形区域内
        for j, in coordinates:
            coordinate1 = coordinates[j+1]
            coordinate0 = coordinates[j]
            # 判断未到点集尾部
            if coordinate1[0] != -1:
                # 判断纵坐标是否在两点之间
                min_lat = min(coordinate0[1], coordinate1[1])
                max_lat = max(coordinate0[1], coordinate1[1])
                # 不在区间内，不可能有交点
                if coordinate_i[1] < min_lat or coordinate_i[1] > max_lat:
                    continue

                # 判断斜率为 0 情况
                if coordinate1[0] == coordinate0[0]:
                    if coordinate0[0] <= coordinate_i[0]:
                        status = status + 1
                    else:
                        continue
                else:
                    # 直线斜率,截距
                    k = (coordinate1[1] - coordinate0[1])/(coordinate1[0] - coordinate0[0])
                    b = (coordinate1[0]*coordinate0[1]-coordinate0[1]*coordinate1[0])/(coordinate1[0]-coordinate0[0])
                    x_i = (coordinate_i[1]-b)/k
                    if x_i < coordinate_i[0]:
                        status = status+1

        # 交点个数为奇数判断点在区域内
        if status/2 != float(status)/2:
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
