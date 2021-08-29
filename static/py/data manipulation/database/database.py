# encoding:utf-8
import pymysql
import re


# 修改 update_database 函数中数据库连接信息

# 修改数据库操作
# input: sql 修改数据库语句
# output: 运行成功则返回影响行数, 否则返回异常

def update_database(sql_str=''):
    conn = pymysql.connect(host='localhost', user='sys_user', password='user_password', database='house_price')
    cursor = conn.cursor()

    try:
        cursor.execute(sql_str)
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return 0


house_id = 1

# 数据表 house 创建
file = open("house.txt", encoding='utf-8')
line = file.readline()
while line:
    # print(line)
    ret_data = re.findall(r"([^'##'\n]+)", line)

    # sql statement
    # Synchronized insertion of houses table and records table
    sql_houses = "INSERT INTO houses (HouseID, HouseName, Price, " \
                 "UnitPrice, Roomtype, Floor, Direction, HouseType, Area, Years, Community, " \
                 "Region, Longitude, Latitude) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}'," \
                 "'{7}','{8}','{9}','{10}','{11}','{12}','{13}')" \
        .format(house_id, ret_data[1], ret_data[2], ret_data[3], ret_data[4], ret_data[5], ret_data[6],
                ret_data[7], ret_data[8], ret_data[9], ret_data[10], ret_data[11], ret_data[12], ret_data[13])

    sql_records = "INSERT INTO records (RecordID,TrafficIndex," \
                  "EducationIndex,EnvironmentIndex,DistrictIndex) VALUES ('{0}',{1},{2},{3},{4})". \
        format(house_id, 0, 0, 0, 0)

    # insert statement
    update_database(sql_houses)
    update_database(sql_records)

    # for item in range(len(ret_data)):
    #     print(item)
    #     print(ret_data[item])

    house_id = house_id + 1
    print("house_id: " + str(house_id))
    line = file.readline()

file.close()

infrastructure_id = 1

# 数据表 infrastructure 创建
file = open("infrastructure.txt", encoding='utf-8')
line = file.readline()
while line:
    # print(line)
    ret_data = re.findall(r"([^,\n]+)", line)
    sql = "insert into infrastructures (`PointID`,`PointName`, `PointType`,`Longitude`,`Latitude`) values ('{0}','{1}','{2}','{3}','{4}')". \
        format(infrastructure_id, ret_data[0], ret_data[1], ret_data[2], ret_data[3])
    # print(sql)
    update_database(sql)

    infrastructure_id = infrastructure_id + 1
    line = file.readline()

    print("infrastructure_id: " + str(infrastructure_id))

file.close()
