# encoding:utf-8

import src.static.py.helper.sql as db_helper
import src.static.py.helper.co_system as coordinate_helper


# 查坐标点数据
# input: 标志数组
# output: 对应 Geojson 格式数据

def select_coordinate_geo():
    sql_house = "select * from houses"
    sql_infrastructure = "select * from infrastructures"
    db_house = db_helper.select_all(sql_house)
    db_infrastructure = db_helper.select_all(sql_infrastructure)

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

    # print(json_return)

    return json_return


select_coordinate_geo()
