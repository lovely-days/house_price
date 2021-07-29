import pandas as pd
import pymysql

db = pymysql.connect(host='localhost', user='root', password='ZyW106509', database='webgis_design')
cursor = db.cursor()
sql = "select * from  houses"
cursor.execute(sql)
results = cursor.fetchall()
col_result = cursor.description  # 获取查询结果的字段描述
db.close()

# 获取字段名，以列表形式保存
columns = []
for i in range(0, len(col_result)):
    columns.append(col_result[i][0])
    print(col_result[i][0])

data1 = list(map(list, results))
df = pd.DataFrame(data=data1, columns=columns)  # mysql查询的结果为元组，需要转换为列表
df.to_csv('./house.csv', index=None)



