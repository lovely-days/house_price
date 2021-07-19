import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
import seaborn as sns
import folium
from folium import plugins
import pymysql
import re

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

db = pymysql.connect(host='localhost', user='root', password='ZyW106509', database='webgis_design')
cursor = db.cursor()
# sql = "select * from webgis_design.houses where HouseID< 2000"
sql = "select * from webgis_design.houses"
cursor.execute(sql)
results = cursor.fetchall()
db.close()

# houses = []
data = pd.DataFrame(columns=["HouseName", "type", "district",
                             "area", "region", "space", "price", "priceSquare",
                             "lon", "lat", "orientation", "status", "livingroom", "halls"])

for result in results:
    information = {"HouseName": result[1],
                   "type": result[7], "district": result[11], "area": result[10], "region": "null", "space": 0.0,
                   "price": float(result[2]), "priceSquare": float(result[3]), "lon": float(result[12]),
                   "lat": float(result[13]), "orientation": result[6], "status": result[9],
                   "livingroom": 0, "halls": 0}

    ret_space = re.findall(r"((\d*[.]\d*)|(\d*))", result[8])[0][0]
    information["space"] = float(ret_space)
    # print(ret_space)

    ret_region = re.findall(r"(金山桥开发区|.{2}区)", result[11])[0]
    if len(ret_region) == 0:
        continue
    else:
        information["region"] = ret_region
        # print(ret_region)

    ret_rooms = re.findall(r"\d", result[4])
    if len(ret_rooms) == 0:
        continue
    else:
        information["livingroom"] = int(ret_rooms[0])
        information["halls"] = int(ret_rooms[1])
        data = data.append(information, ignore_index=True)

    # print(ret_rooms[0])
    # print(ret_rooms[1])

    # houses.append(information)

    # for info in information:
    #     print(information[info])

    # data = data.append(information, ignore_index=True)


# print(data)
# data = data.append(information, ignore_index=True)
# data = pd.DataFrame(houses)
# print(data.describe())
# data.groupby('type')['price'].mean()
# ok = data.groupby('region')['price'].mean()

# df_expenditure_mean = pd.DataFrame(ok)
# df_expenditure_mean.rename(columns={'region': '区域', 'means': '均值'}, inplace=True)
# df_expenditure_mean.plot.bar(x='区域', y='均值', rot=0)
# plt.savefig("./2.png")
# print(df_expenditure_mean)

# print(data.groupby('type')['priceSquare'].mean())

# print(data.groupby('livingroom')['price'].mean())

# district_status_group = data.groupby('region').mean()
# district_status_vis = district_status_group.reset_index()[['region', 'priceSquare']]
# district_status_vis.sample(10)
# sns.lmplot('space', 'priceSquare', data)
# plt.savefig("./2.png")

# ok.bar()
# 保存图片
# plt.savefig("./1.png", dpi=300)

price_heatmap = folium.Map(location=[117.200931, 34.219325], zoom_start=11)
price_heatmap.add_child(plugins.HeatMap([[row["lat"], row["lon"]] for name, row in data.iterrows()]))
price_heatmap.save("./heat_locate.html")


def map_points(df, lat_col='lat', lon_col='lon', zoom_start=11, plot_points=False, pt_radius=15, draw_heatmap=False,
               heat_map_weights_col=None, heat_map_weights_normalize=True, heat_map_radius=15):
    middle_lat = df[lat_col].median()
    middle_lon = df[lon_col].median()

    curr_map = folium.Map(location=[middle_lat, middle_lon], zoom_start=zoom_start)

    if plot_points:
        for _, row in data.iterrows():
            folium.CircleMarker([row[lat_col], row[lon_col]], radius=pt_radius, popup=row['name'],
                                fill_color="#3db7e4", ).add_to(curr_map)

    if draw_heatmap:
        if heat_map_weights_col is None:
            cols_to_pull = [lat_col, lon_col]
        else:
            if heat_map_weights_normalize:
                df[heat_map_weights_col] = df[heat_map_weights_col] / df[heat_map_weights_col].sum()
            cols_to_pull = [lat_col, lon_col, heat_map_weights_col]
        lat_lon = df[cols_to_pull].values
        curr_map.add_child((plugins.HeatMap(lat_lon, radius=heat_map_radius)))

    curr_map.save('./heat_price.html')

    return curr_map


data_geo = data.dropna()
map_points(data_geo, plot_points=False, draw_heatmap=True, heat_map_weights_normalize=False,
           heat_map_weights_col='priceSquare', heat_map_radius=9)

'''
data_group = data.groupby('region')['price'].agg([('average', 'mean'), ('median', 'median'), ('variance', 'var')]).reset_index()
print(data_group)
data_group.plot.bar(figsize=(10, 5))
plt.savefig("./111.png", dpi=300)

data_group1 = data.groupby('region')['price'].agg([('price_max', 'max'), ('price_min', 'min')]).reset_index()
print(data_group)
data_group1.plot.box(figsize=(10, 5))
plt.savefig("./222.png", dpi=300)
'''
data_group = data.groupby('region')['price'].agg([('data count', 'count')]).reset_index()
data_group.plot.bar(x='region',y='data count', figsize=(10, 5))
plt.title(" 分区域二手房数目统计 ")
plt.xlabel(" 区域名 ")
plt.ylabel(" 二手房数目 ")
plt.savefig("./count.png", dpi=300)

data_group = data.groupby('region')['price'].agg([('average', 'mean')]).reset_index()
plt.title(" 分区域二手房价格平均数统计 ")
plt.xlabel(" 区域名 ")
plt.ylabel(" 房屋价格 ")
data_group.plot.bar(x='region', figsize=(10, 5))
plt.savefig("./mean.png", dpi=300)

data_group = data.groupby('region')['price'].agg([('variance', 'var')]).reset_index()
plt.title(" 各区域二手房价格方差统计 ")
plt.xlabel(" 区域名 ")
plt.ylabel(" 房价价格 ")
data_group.plot.bar(x='region', figsize=(10, 5))
plt.savefig("./mean.png", dpi=300)

data.boxplot(column='price', by='region', figsize=(10, 5))
plt.title(" 各区域二手房价格箱图 ")
plt.xlabel(" 区域名 ")
plt.ylabel(" 房屋价格 ")
plt.savefig("./boxplot.png", dpi=300)

# data_group = data.groupby('region')['price'].describe().reset_index()
# print(data_group)
# data_group.boxplot(column='region')
# plt.savefig("./111.png", dpi=300)
