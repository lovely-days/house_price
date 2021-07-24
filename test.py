# encoding:utf-8
import  folium

'''创建Map对象'''
m = folium.Map(
    location=[29.488869,106.571034],
    tiles='Stamen Terrain',
    zoom_start=13
)

'''为地图对象添加点击显示经纬度的子功能'''
m.add_child(folium.LatLngPopup())

m.save("./ok.html")