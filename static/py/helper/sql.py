import pymysql


# 修改数据库操作
# input: sql 修改数据库语句
# output: 运行成功则返回影响行数, 否则返回异常

def update_database(sql_str=''):
    conn = pymysql.connect(host='localhost', user='root', password='ZyW106509', database='webgis_design')
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


# 查一条数据
# input: sql 查询语句
# output: 返回查询得到单一数据

def select_one(sql_str=''):
    conn = pymysql.connect(host='localhost', user='root', password='ZyW106509', database='webgis_design')
    cursor = conn.cursor()

    cursor.execute(sql_str)
    data = cursor.fetchone()
    conn.close()

    return data


# 查所有数据
# input: sql 查询语句
# output: 返回查得所有数据

def select_all(sql_str):
    conn = pymysql.connect(host='localhost', user='root', password='ZyW106509', database='webgis_design')
    cursor = conn.cursor()

    cursor.execute(sql_str)
    data = cursor.fetchall()
    conn.close()

    return data
