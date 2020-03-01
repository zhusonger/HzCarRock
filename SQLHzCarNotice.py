#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 导入SQLite驱动:
import sqlite3


# 创建数据库
def create_tab():
    # 连接到SQLite数据库
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect("notice.db")
    # 创建一个Cursor
    cursor = conn.cursor()

    # 执行一条SQL语句，创建notice表:
    cursor.execute(
        'create table if not exists notice ('
        'id integer primary key AUTOINCREMENT,'
        ' title varchar(255),'
        ' href varchar(255),'
        ' noticeDay varchar(20)) ')

    # 关闭数据库
    cursor.close()
    conn.commit()
    conn.close()


def insert_notice(titles, hrefs, days):
    if len(titles) != len(days) or len(titles) == 0:
        # print "title & day len is not equal or is empyt"
        return

    create_tab()

    try:
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect("notice.db")
        # 创建一个Cursor
        cursor = conn.cursor()
        sql = 'insert into notice(title, href, noticeDay) values(?, ?, ?)'
        param = []
        for index in range(len(titles)):
            title = titles[index]
            href = hrefs[index]
            day = days[index]
            param.append([title, href, day])
        # 执行一条SQL语句，插入日志:
        cursor.executemany(sql, param)

        # 关闭数据库
        cursor.close()
        conn.commit()
        conn.close()
    except Exception:
        print("insertNotice error")


def read_notice():
    create_tab()
    titles = []
    hrefs = []
    days = []

    try:
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect("notice.db")
        # 创建一个Cursor
        cursor = conn.cursor()

        sql = 'select title, href, noticeDay from notice'
        # 执行一条SQL语句，查询日志
        cursor.execute(sql)
        values = cursor.fetchall()

        for item in values:
            titles.append(item[0])
            hrefs.append(item[1])
            days.append(item[2])

        # 关闭数据库
        cursor.close()
        conn.commit()
        conn.close()
    except Exception:
        print('readNotice error')

    return titles, hrefs, days


def delete_notice():

    create_tab()

    try:
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect("notice.db")
        # 创建一个Cursor
        cursor = conn.cursor()

        sql = 'delete from notice'
        # 执行一条SQL语句，查询日志
        cursor.execute(sql)

        # 关闭数据库
        cursor.close()
        conn.commit()
        conn.close()
    except Exception:
        print('deleteNotice error')


