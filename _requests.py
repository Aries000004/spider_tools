#!-*- coding:utf-8 -*-
import requests

"""
封装常用requests的一些方法

1、cookie相关
    requests接收cookie信息,解析response header中的Set-Cookie参数，使用正则";\s*"去做split，第一个";"前的k=v组合会被视为cookie的key和value
    其余会被视为应属于"version","expires", "max-age","domain", "path", "port","comment", "commenturl"等参数信息，如果不被识别，则会视为nonstandard_attr
    放到_rest参数中，也就是说，若响应为
    "Set-Cookie: ticketID=A; JSESSIONID=779f7c72-0ddb-40b3-b92e-5549973f0a17; UID=e526db86fc844bbab344da199ca06c84; Comment=SessionServer-unity; Path=/; Secure"
    则response.cookies.get_dict()是{"ticketID":"A"}
    而真正有效的JSESSIONID，UID为被视为nonstandard_attr而放到rest中，故该session对象在之后的请求会出现异常
2、timeout设置问题
    默认connect timeout=15
"""

session_obj = requests.Session()
url = 'http://www.baidu.com'

class CookiesOpt(object):
    def cookie_opt(self):
        """cookie的相关操作，cookie相关操作在cookielib.py文件中"""
        session_obj.cookies.set('key', None)  # 清楚cookie中为key的值
        session_obj.cookies.set('k', 'v')  # 重置cookie值
        session_obj.cookies.get_dict()  # 取当前session的所有cookie值
        session_obj.cookies.get('k')  # 获取指定k的cookie值

    def specify_cookies(self):
        """指定cookie值的请求"""
        cookies = {
            'key1': 'val1',
            'key2': 'val2'
        }
        session_obj.get(url, cookies=cookies)


class ProxiesOpt(object):

    @property
    def proxies(self):
        """
        http参数设置及使用方式
        """
        proxies = { # http/https设置同样代理
            'all': '60.187.108.9:47586',
        }
        http_proxy = {
            'http': '60.187.108.9:47586',  # http://60.187.108.9:47586
        }
        https_proxy = {
            'https': '60.187.108.9:47586',  # http://60.187.108.9:47586
        }
        return proxies

    def use_proxy(self):
        """作为proxies参数传入"""
        requests.get(url, proxies=self.proxies)

    # def use_proxy_1(self):


class RequestsOpt(object):
    def _get(self):
        """
        get请求, 请求默认参数字段名称:params，
        网络请求时，params中的参数将会以query string 形式传输
        服务端的http server可以打印出以该方式传输的参数
        """
        params = {
            'k': 'v'
        }
        requests.get(url, params=params)

    def _post(self):
        """
        post请求，请求默认参数字段名称:data
        网络请求时，data中的参数将会被放在 body 中传输
        服务端http server不做特殊截获无法打印该部分参数
        """
        data = {
            'k': 'v'
        }
        requests.post(url, data=data)

class GetRequestsPrams(object):
    """
    获取表单数据: request.form.get("key", type=str, default=None)
    获取get请求参数: request.args.get("key")
    获取所有参数: request.values.get("key")
    """


def forbidden_secure_warning():
    """
    禁用安全请求警告
    在session.verify=False即关闭SSL校验时，会有安全warning信息提醒
    """
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def ResponseOpt():
    """
    response具体实现:https://github.com/requests/requests/blob/master/requests/models.py
    requests.models.Response()为False的情况，此时resp对象的所有属性仍旧可用，只是bool值被置为了False
    发送http请求时，如果
        1.200 <= status_code < 400, 则resp的bool值为True
        2.400 <= status_code < 600, 则resp的bool值为False   (此时resp对象中的content/json/raw等属性全部可用)
    例:
        resp = requests.get('http://www.baidu.com')
        if resp.status_code > 200 and resp_status < 400:
            assert(resp, True)
        elif resp.status_code >= 400 and resp_status < 600:
            assert(resp, False)

    一般情况下，实现层使用resp时倾向于使用True/False来判断该对象是否可用
    如果这里需要对各种status_code同等对待，则只需要把status_code置为True区间即可
    即:
        resp = requests.get('http://www.baidu.com')
        if resp.status_code== 400:  # status_code为400
            assert(resp, False)     # 此时resp为False
            resp.status_code = 201       # 重置 status_code为201，即True区间
            assert(resp, True)  # 此时resp就变为False了
    """