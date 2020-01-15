# HzCarRock

杭州阶梯摇号公告的爬虫脚本  

避免错过宝贵的一年2次的摇号机会  

在阿里云服务器上 每天11点去查询，如果有新的公告出来就会发短信给数据库中的用户 

# 使用方式

1. 先进入dysms_python文件夹目录, 更改const.py内的id跟secret

2. 在dysms_python 执行 sudo python setup.py install

3. 切换到HzCarRock目录, 执行CarCrawler.py
