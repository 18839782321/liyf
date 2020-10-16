# coding=utf-8
"""
该文件封装了mysql的一些常用方法：增、改、查
"""
# 导入模块
import pymysql.cursors

# 数据库设置，有其他需求可自行修改
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='deal_data', charset='utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)  # 返回字典结构


def insert(table, item, swhere):
    """
    封装添加函数
    :param table: 表名
    :param item: 需要插入的数据，传进来的类型是字典，可以根据键值取数据
    :param swhere: where条件
    :return: 插入成功或者失败
    """
    insert_sql_key = insert_sql_value = update_sql = ''
    for key in item:
        if key:
            value = str(item[key]).replace("'", "\\\'")
            # 将单引号转成\单引号
            value = value.replace('"', '\\\"')
            # 将双引号转成\双引号
            insert_sql_key = insert_sql_key + str(key) + ","
            insert_sql_value = insert_sql_value + "'" + value + "',"
            update_sql = update_sql + str(key) + "='" + value + "',"
    # 拼接一条完整的sql语句并执行
    insert_sql = "insert into " + table + "(" + insert_sql_key.strip(',') + ") values (" + insert_sql_value.strip(
        ',') + ")"
    update_sql = " update " + table + " set " + update_sql.strip(",")
    select_sql = " select id from " + table + " where " + swhere
    # 如果存在就更新
    # select_sql = cursor.escape_string(select_sql)
    db.ping(reconnect=True)
    cursor.execute(select_sql)
    result = cursor.fetchone()
    if (result):
        sql = update_sql + " where id in(" + str(result['id']) + ")"
    else:
        sql = insert_sql
    try:
        db.ping(reconnect=True)
        print(sql)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # db.close()
        print('success')
    except Exception as e:
        print('mysql错误')
        db.commit()
        print(sql)
        print(e)


def _select(table, item, swhere):
    """
    封装查询函数
    :param table: 表名
    :param item: 需要查询的数据
    :param swhere: 查询的条件
    :return: 根据拼接的SQL语句查询出来的结果
    """
    if swhere == '':
        swhere = "1"
    # 拼接SQL语句
    select_sql = " select " + item + " from " + table + " where " + swhere
    # 在每次运行sql之前，ping一次，如果连接断开就重连。
    db.ping(reconnect=True)
    cursor.execute(select_sql)

    result = cursor.fetchall()
    if (result):
        # 有数据，返回result，属于字典结构
        return result
    else:
        # 无数据，返回空字符串
        return ''
