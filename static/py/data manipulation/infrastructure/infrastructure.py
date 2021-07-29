import re
import src.static.py.helper.sql as db_helper

file = open("infrastructure.txt", encoding='utf-8')
line = file.readline()
while line:
    print(line)
    ret_data = re.findall(r"([^,\n]+)", line)
    sql = "insert into infrastructures (`PointName`, `PointType`,`Longitude`,`Latitude`) values ('{0}','{1}','{2}','{3}')". \
        format(ret_data[0], ret_data[1], ret_data[2], ret_data[3])
    print(sql)
    db_helper.update_database(sql)
    line = file.readline()

file.close()

