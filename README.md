# auth_login_tools
封装授权登陆时的一些通用方法
* [授权抓取时，多张图片验证码合并问题](https://github.com/wanghuafeng/spider_tools/blob/master/image_merge.py)
* [session对象持久化到本地，进行断点调试](https://github.com/wanghuafeng/spider_tools/blob/master/session_obj_pickle.py)
* [rsa(含no padding), des, md5加密、解密封装](https://github.com/wanghuafeng/spider_tools/blob/master/__encrypt.py)
* [日志封装器](https://github.com/wanghuafeng/spider_tools/blob/master/__logger.py)
* [网络请求的装饰器](https://github.com/wanghuafeng/spider_tools/blob/master/decorator.py)
* [文件加载](https://github.com/wanghuafeng/spider_tools/blob/master/load_config.py)
* [使用gevent压力测试](https://github.com/wanghuafeng/spider_tools/blob/master/_gevent.py)
* [获取机器参数, socket相关TCP server](https://github.com/wanghuafeng/spider_tools/blob/master/_socket.py)
* [封装requests相关的一些方法](https://github.com/wanghuafeng/spider_tools/blob/master/_requests.py)
* [封装subprocess的一些方法及使用是的注意点](https://github.com/wanghuafeng/spider_tools/blob/master/_subprocess.py)
* [ssh tunnel建立及服务端端口映射转发](https://github.com/wanghuafeng/spider_tools/blob/master/ssh_tunnel.py)
* [一些统计sql高级用法](https://github.com/wanghuafeng/spider_tools/blob/master/some_sql.sql)
* [代理存活检测封装工具](https://github.com/wanghuafeng/spider_tools/blob/master/proxy_alive_check_utils.py)
* [linux一些配置相关查询](https://github.com/wanghuafeng/spider_tools/blob/master/linux_relative.py)
* [一些常用算法实现](https://github.com/wanghuafeng/spider_tools/blob/master/arith.py)
<pre>
web抓包工具:Firebug+Httpfox相互补充
	1、Firebug适用普通跳转抓包，全局搜索，js断点跟踪，当前页面跳转抓包
	但window.open(url,"_blank");另起开启新的窗口完成跳转时，Firebug的Presist设置会无效，导致跳转页可能会有丢包的情况
	2、Httpfox功能可视化展示及断点捕捉较Firebug稍微弱一些，但是却可以弥补Firebug在新窗口跳转时捕获所有网络交互包
fiddler手机抓包:
    PC局域网地址:192.168.1.82
    1、pc 安装fiddler
    2、fiddler配置(重启生效)
    3、手机设置代理(必须同一局域网内)，服务器地址:192.168.1.82, 端口:8888
    4、安装证书，打开Safari，输入http://192.168.1.82:8888，点击"FiddlerRoot certificate"进行证书安装
        (1)不同的fiddler版本证书可能不同，升级fiddler后需要把(”设置“->“通用”->"描述文件")证书删除后重新安装
        (2)ios系统10.3以后，新安装的证书都是不受信任的，需要进行手工设置, 设置方式：设置->通用->关于本机->证书信任设置->  找到 fiddler证书，打开信任开关

针对cookie特殊反爬虫case:
    1、在cookie之中使用随机数作为key，val则为固定值，服务端对变量key进行校验 (hun)

代理模块使用注意点：
     1、判断网站是否在翻页过程中允许切换IP
     2、授权网站的特殊端口限制
     3、网站对单个IP的封禁策略预估
     4、目标网站的特殊代理类型的限制
     5、授权登陆与登陆成功后的代理使用策略的不同
登陆实现方式：
     1、服务端模拟登陆
     2、APP客户端登陆(webview)
     3、APP客户端模拟登陆
     4、web端模拟登陆(可行性待调研)
抓取方式实现:(解析部门均由服务端实现)
     1、服务端登陆、服务端抓取
     2、客户端登陆、服务端抓取
     3、客户端登陆、客户端抓取
     4、客户端模拟登陆、服务端抓取
     5、web端模拟登陆、服务端抓取(待调研)
存储模块：
     所有抓取模块统一调度，作为独立模块拆出
     1、已清洗数据入库前校验及二次处理(加密等)
     2、接口调用前的逻辑整合
     注意点：
          (1)各抓取方向存储模块设计时必须技术评审
          (2)分表、分库以及数据库自动扩展的可行性、合理性
          (3)model层单独对应一个表结构的相关读写逻辑，尽量避免多表操作混到一个model中
          (4)涉及业务逻辑较为复杂时，可以抽离出service层
          (5)controller层尽量不做太复杂的逻辑处理，一个模块尽量合并到一个controller中
          (6)代码层减少硬编码，抽离出统一的校验及处理方法，减少重复工作
数据监控(邮件报警+短信报警)：
     0、服务存活监控
     1、登陆比监控(不同抓取通道,自动切换)
     2、抓取完整率监控
     3、解析准确率监控，新模板自动发现(代码层+人工review)
     4、各抓取模块更细颗粒度监控(尝试抓取登陆号码数,成功登陆号码数;提交验证码数,验证成功号码数;开始抓取号码数,抓取成功号码数;号码登陆成功率，号码抓取成功率，开始抓取成功率，整体转化率)
</pre>
