项目使用Python作为监控程序监控Sync服务器的同步文件夹，一旦出现新的指定格式（如MOBI)的文件，则将会向指定的kindle邮箱发送新增加的电子书，邮箱的设置需要到amazon自己设置，想必用过kindle的应该不陌生。

首先下载项目到本地：
```
$git clone https://github.com/KDF5000/WeeklyBook
```

然后修改`server.py`里面的kindle邮箱，以及授权的邮箱

> EXT_LIST = ['mobi'] #想要发送的邮件格式
> HOST_NAME = 'smtp.cstnet.cn' #授权邮箱的smtp服务器
> HOST_PORT = 25 #smtp服务器端口
> USER_NAME = 'kongdefei@ict.ac.cn' #授权邮箱的用户名
> USER_PASS = '*********************'
> KINDLE_MAILS = ['kdf5000@kindle.cn'] #接收电子书的kindle邮箱，可以在亚马逊查看
> FROM_NAME = 'kongdefei@ict.ac.cn' #发送邮件的from名字，建议使用发送的邮箱地址

##### 后台启动

进入下载的文件夹，执行下面的命令

```shell
$nohup python server.py /home/ubuntu/kongdefei/SyncBook > sync.out 2>&1 &
```

其中`/home/ubuntu/kongdefei/SyncBook`是sync同步的文件夹，sync.out是server.py的输出日志，该程序将会在后台持续运行监控`/home/ubuntu/kongdefei/SyncBook`下面是否有新的电子书的出现。


至此，你就可以享受你心爱的kindle每周定时收到一本优秀的电子书了。
顺便晒一下树莓派[憨笑]
![](http://7sbpmg.com1.z0.glb.clouddn.com/blog/image/raspberry.jpeg)

