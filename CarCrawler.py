#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 网络请求
import urllib2
# 正则表达式
import re
# 时间
import time
# JSON
import json
# 修改默认编码
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 日志数据库
import SQLHzCarNotice
# 发送短信用户数据库
import SQLSms

import dysms_python.demo_sms_send


keyword = u"阶梯"
url = "http://xkctk.hangzhou.gov.cn/tzgg/"
User_Agent = " Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
headers = {'User-Agent': User_Agent}

# 发送短信
def sendSms(users):
    titles, days = SQLHzCarNotice.read_notice()

    # 有新公告 加入到数据库中
    if len(titles) > 0:
        title = titles[0]
        day = days[0]
        dayLen = len(day)
        titleLen = len(title)
        t = time.strptime(day, "%Y-%m-%d")
        if dayLen + titleLen >= 20:
            keyIndex = title.find(keyword)
            keyLen = len(keyword)
            start = keyIndex - 2
            end = keyIndex + keyLen + 2
            remark = title[0:2] + u".." + title[start:end] + u".." + title[titleLen - 2:titleLen] \
                     + " " + unicode(t.tm_mon) + "月" + unicode(t.tm_mday) + "号"
        else:
            remark = title

        for user in users:
            phone = users[user]
            print "发送短信给 " + user + " : " + phone
            # 发送短信

            # smsResponse = dysms_python.demo_sms_send.sendSms(user, phone, remark)
            # print smsResponse
            # SQLSms.insert_sms_response(smsResponse)

def crawlerNotice():
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read()
        content = content.decode('utf-8')
        pattern = re.compile('<a class="text" href=\".*?\" target="_blank">(.*?)</a>\s*<span class="date">(.*?)</span>',
                             re.S)
        items = re.findall(pattern, content)

        dbNotice = SQLHzCarNotice.read_notice()
        dbTitles = set(dbNotice[0])
        titles = []
        days = []
        for item in items:
            title = item[0]
            day = item[1]

            # 已经在数据库中的 说明已经检测到过了，不再添加
            if keyword in title and not title in dbTitles:
                titles.append(title)
                days.append(day)

        SQLHzCarNotice.insert_notice(titles, days)

        users = SQLSms.read_users()

        sendSms(users)

        # SQLHzCarNotice.delete_notice();
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print "code" + e.code
        if hasattr(e, "reason"):
            print "reason" + e.reason


# 姓名跟电话号码
if len(sys.argv) > 1:
    arg1 = sys.argv[1]
    # 删除用户
    if arg1 == '-d':
        key = sys.argv[2]
        SQLSms.delete_user(unicode(key))
    # 添加用户
    elif arg1 == '-a':
        user = sys.argv[2]
        phone = sys.argv[3]
        SQLSms.insert_user(unicode(user), unicode(phone))
        sendSms({user:phone})
    elif arg1 == '-l':
        users = SQLSms.read_users()
        print "用户列表:"
        for user in users:
            print user+" " + users[user]
    elif arg1 == '-c':
        print "开始爬了..."
        crawlerNotice()
    else:
        print '脚本参数:\n' \
              + 'CarCrawler.py.py -c 启动爬虫脚本\n' \
              + 'CarCrawler.py.py -d name/phone 删除用户\n' \
              + 'CarCrawler.py.py -a name phone 新增用户\n' \
              + 'CarCrawler.py.py -l 显示所有用户\n';
else:
    print '脚本参数:\n' \
          + 'CarCrawler.py.py -c 启动爬虫脚本\n' \
          + 'CarCrawler.py.py -d name/phone 删除用户\n' \
          + 'CarCrawler.py.py -a name phone 新增用户\n' \
          + 'CarCrawler.py.py -l 显示所有用户\n';