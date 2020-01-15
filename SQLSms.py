#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 导入SQLite驱动:
import sqlite3
import json


# 创建数据库
def create_tab():
    # 连接到SQLite数据库
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect("notice.db")
    # 创建一个Cursor
    cursor = conn.cursor()

    # 执行一条SQL语句，创建notice表:
    cursor.execute(
        'create table if not exists users (id integer primary key AUTOINCREMENT, name varchar(255), phone varchar(100) UNIQUE) ')

    cursor.execute(
        'create table if not exists sms_logs (id integer primary key AUTOINCREMENT, bizId varchar(255), smsResponse varchar(255))')

    # 关闭数据库
    cursor.close()
    conn.commit()
    conn.close()


def insert_sms_response(smsResponse):
    create_tab()

    try:
        text = json.loads(smsResponse)
        conn = sqlite3.connect("notice.db")
        # 创建一个Cursor
        cursor = conn.cursor()

        code = text["Code"]
        if code == 'OK':
            bizId = unicode(text["BizId"])
        else:
            bizId = unicode('-1')

        print ("BizId : " + bizId)

        sql = 'insert into sms_logs(bizId, smsResponse) values(?, ?)'
        cursor.execute(sql, [bizId, unicode(smsResponse)])
        # 关闭数据库
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print ("insert_sms_response error" + e)


def insert_user(user, phone):
    create_tab()

    try:
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect("notice.db")
        # 创建一个Cursor
        cursor = conn.cursor()
        sql = 'insert into users(name, phone) values(?, ?)'
        param = [user, phone]

        cursor.execute(sql, param)
        count = cursor.rowcount

        # 关闭数据库
        cursor.close()
        conn.commit()
        conn.close()

        if count > 0:
            print ("添加用户 " + user+" : " + phone)

        return count
    except Exception as e:
        print ("insert_user error:" + e)


def read_users():
    create_tab()
    users = {}

    try:
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect("notice.db")
        # 创建一个Cursor
        cursor = conn.cursor()

        sql = 'select name, phone from users'
        # 执行一条SQL语句，查询日志
        cursor.execute(sql)
        values = cursor.fetchall()

        for item in values:
            users[item[0]] = item[1]

        # 关闭数据库
        cursor.close()
        conn.commit()
        conn.close()
    except Exception:
        print ('read_users error')

    return users


def delete_user(key):
    create_tab()

    try:
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect("notice.db")
        # 创建一个Cursor
        cursor = conn.cursor()

        sql = 'delete from users where name = ? or phone = ?'
        # 执行一条SQL语句，查询日志
        cursor.execute(sql, [key, key])

        # 关闭数据库
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print ('delete_user error : ' + e)

