#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 网络请求
import urllib.request
# 正则表达式
import re
# 时间
import time
# JSON
# import json
# 日志数据库
import SQLHzCarNotice
# 发送短信用户数据库
import SQLSms
# 发送邮件
import AliEmail

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import sys

keyword = "阶梯"
url = "https://hzxkctk.cn/tzgg/"
User_Agent = " Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
headers = {'User-Agent': User_Agent}

# 发送短信
def send_sms(users):
    titles, hrefs, days = SQLHzCarNotice.read_notice()

    # 有新公告 加入到数据库中
    if len(titles) > 0:
        title = titles[0]
        href = hrefs[0]
        day = days[0]
        # dayLen = len(day)
        # titleLen = len(title)
        # t = time.strptime(day, "%Y-%m-%d")
        # if dayLen + titleLen >= 20:
        #     remark = title + str(t.tm_mon) + "月" + str(t.tm_mday) + "号"
        # else:
        #     remark = title

        print("摘要:" + title+", "+href+", "+day)
        text = "<h3>标题</h3>"+title+"\n\n <h3>链接</h3>"+href+"\n\n <h3>日期</h3>"+day
        for item in users:
            user_email = users[item]
            print("发送短信给 " + item + " : " + user_email)
            # 发送邮件
            AliEmail.send_email("阶梯摇号公告更新", text, user_email)



def crawler_notice():
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read()
        content = content.decode('utf-8')
        pattern = re.compile('<a class="text" href=\"(.*?)\" target="_blank">(.*?)</a>\s*<span class="date">(.*?)</span>',
                             re.S)
        items = re.findall(pattern, content)

        dbNotice = SQLHzCarNotice.read_notice()
        dbTitles = set(dbNotice[0])
        titles = []
        hrefs = []
        days = []
        for item in items:
            href = item[0]
            title = item[1]
            day = item[2]

            # 已经在数据库中的 说明已经检测到过了，不再添加
            if keyword in title and title not in dbTitles:
                titles.append(title)
                hrefs.append(href)
                days.append(day)
                print("\nNEWS:"+title+","+href+"\n")
            else:
                print(title+","+href)
        SQLHzCarNotice.insert_notice(titles, hrefs, days)

        if len(titles) > 0:
            # send_sms()
            email_users = SQLSms.read_users()
            href = hrefs[0]
            title = titles[0]
            day = days[0]

            text = "<h3>标题</h3>" + title + "\n\n <h3>链接</h3>" + href + "\n\n <h3>日期</h3>" + day
            for item in email_users:
                user_email = email_users[item]
                print("发送短信给 " + item + " : " + user_email)
                # 发送邮件
                AliEmail.send_email("阶梯摇号公告更新", text, user_email)

    except urllib.request.URLError as e:
        if hasattr(e, "code"):
            print("code" + e.code)
        if hasattr(e, "reason"):
            print("reason" + e.reason)


# 姓名跟电话号码
if len(sys.argv) > 1:
    arg1 = sys.argv[1]
    # 删除用户
    if arg1 == '-d':
        key = sys.argv[2]
        SQLSms.delete_user(str(key))
    # 添加用户
    elif arg1 == '-a':
        user = sys.argv[2]
        phone = sys.argv[3]
        # 插入用户成功才发送短信
        if SQLSms.insert_user(str(user), str(phone)) > 0:
            send_sms({user: phone})
    elif arg1 == '-l':
        users = SQLSms.read_users()
        print("用户列表:")
        for user in users:
            print(user + " " + users[user])
    elif arg1 == '-c':
        print("开始爬了...")
        crawler_notice()
        print("爬完了...")
    else:
        print('脚本参数:\n' \
              + 'CarCrawler.py.py -c 启动爬虫脚本\n' \
              + 'CarCrawler.py.py -d name/phone 删除用户\n' \
              + 'CarCrawler.py.py -a name phone 新增用户\n' \
              + 'CarCrawler.py.py -l 显示所有用户\n')
else:
    print('脚本参数:\n' \
          + 'CarCrawler.py.py -c 启动爬虫脚本\n' \
          + 'CarCrawler.py.py -d name/phone 删除用户\n' \
          + 'CarCrawler.py.py -a name email 新增用户\n' \
          + 'CarCrawler.py.py -l 显示所有用户\n')
