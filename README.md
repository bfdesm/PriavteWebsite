# MyASP wheel
## 文件介绍
### index下面放前端资源,可以自己创建文件夹
### css存放css文件
## ASP.py 服务器对象
### 建立,关闭套接字,等待连接
## RequestHandler.py 请求处理器对象
### 获得请求,解析请求,发送响应,关闭套接字
## RouteHandler.py 路由处理器
### 目前支持请求: GET
### 文件放到index目录下,默认都是寻找html文件,还不支持css,JavaScript
#### eg1: http://127.0.0.1:81/login.html <==> http://127.0.0.1:81/login
#### eg2: http://127.0.0.1:81/1.txt
#### eg3: 没有找到文件返回 "404 Not Found"
## HttpFactory.py http响应生成工厂
### 目前支持响应类型: text/html text/css
## ASPlocalTest.py 简单的例子
### 运行该文件后,电脑打开该网站 http://127.0.0.1:81/
