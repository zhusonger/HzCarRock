# HzCarRock

杭州阶梯摇号公告的爬虫脚本  

避免错过宝贵的一年2次的摇号机会  

在阿里云服务器上 每天11点去查询，如果有新的公告出来就会发短信给数据库中的用户 

#前置条件
1. python3环境
2. 同级目录添加config.ini文件
3. 阿里云邮箱（这个可以自己换, 修改下hostname即可）

## config.ini格式
```
[User]
Name=XXX
UserName=xxx@xxx.com.cn
Password=xxxx
[Email]
From='xxxx@xxxx.com.cn'
```

# 使用方式
运行 CarCrawler.py 即可

目前我是结合Jenkins做定时构建
也可以使用linux的定时任务crontab
