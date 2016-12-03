# coding=GBK
import requests
import rsa
import binascii
import re
import json
import base64
import urllib.request
import urllib.parse
import http.cookiejar
myNumAndPwd = {"name": "z567893951220@sina.com", "pwd": "zCx93950825*"}
postData = {
  'entry': 'weibo',
  'gateway': '1',
  'from': '',
  'savestate': '7',
  'userticket': '1',
  'ssosimplelogin': '1',
  'vsnf': '1',
  'vsnval': '',
  'su': '',
  'service': 'miniblog',
  'servertime': '',
  'nonce': '',
  'pwencode': 'rsa2',
  'sp': '',
  'encoding': 'UTF-8',
  'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
  'returntype': 'META'
}

class WeiboLogin():
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    myHeader = {
        # "Host": "login.weibo.cn",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        # "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        # # "Accept-Encoding":"gzip, deflate",
        # "Connection": "keep-alive"
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

    #myHeader = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    cookiefilename = "mycookies.txt"

    cj = []

    def __init__(self):
        # cookie_filename = 'cookie.txt'
        # cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
        # print("cookie",cookie)

        # 保存cookie
        self.cj = http.cookiejar.MozillaCookieJar(self.cookiefilename)
        print("MozillaCookieJar：",self.cj)
        cookie_support = urllib.request.HTTPCookieProcessor(self.cj)
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)


    def _get_servertime(self, username):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % username
        #注意Python2转Python3，如果仍用原先的代码，会输出byte，此时需要在后面解码为GBK，不需要像网上在前面加“rb”
        data = urllib.request.urlopen(url).read().decode('UTF-8')
        print("server data:",data)
        p = re.compile('\((.*)\)')
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = data['servertime']

        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        print("servertime", servertime,"  nonce",nonce,"  pubkey",pubkey,"  rsakv",rsakv)
        return servertime, nonce, pubkey, rsakv

    def _get_pwd(self, pwd, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
        #奇怪，为什么在Python2中这里不需要转成byte？莫非是因为Python2默认为byte？
        pwd = rsa.encrypt(bytes(message,"utf8"), key)
        ##需要加上decode不然会输出位bytes
        return binascii.b2a_hex(pwd).decode()

    def _get_user(self, username):
        name = urllib.request.quote(username)
        #print("name:",name)
        #注意：base64.b64encode() takes bytes as an argument, not a string.
        #需要加上decode不然会输出位bytes
        #注意这里仍然是base64.encodestring，不是base64.b64encode()方法，输入仍然是bytes
        username = base64.encodestring(bytes(name, 'utf-8'))[:-1].decode()
        return username

    def login(self):
        username = myNumAndPwd["name"]
        password = myNumAndPwd["pwd"]
        print("username:", username)
        print("password:",password)
        try:
            servertime, nonce, pubkey, rsakv = self._get_servertime(username)
        except Exception as e:
            print(e)
            print('Get severtime error!')
            return None
        global postData
        postData['servertime'] = servertime
        postData['nonce'] = nonce
        postData['su'] = str(self._get_user(username))
        print("ejU2Nzg5Mzk1MTIyMCU0MHNpbmEuY29t")
        print("postData['su']",postData['su'],"   ",self._get_user(username))
        postData['sp'] = str(self._get_pwd(password, servertime, nonce, pubkey))
        print("b8ed5725e74b42ec9a5bda9069a27d1d7c99d2e4fd00576e303bda518ba66eb283688a13c3a91e55a1c67910deccfb0128826a88d5a518e69831849fa9e79ea037917f91cd17ce8c14b5c52bb94307c333aa8c0da870224f430323b5e78cba6349a65037ec921e92b7cb2f36597bf373acca45eaa65e251b42710c08c07caea6")
        print("postData['sp']",postData['sp'])
        postData['rsakv'] = rsakv
        print("nonce", nonce)
        print("rsakv", rsakv)
        print("postdata",postData)

        # # 处理302重定向
        #TypeError: cannot use a string pattern on a bytes-like object
        post = urllib.parse.urlencode(postData).encode(encoding='UTF8')
        print(post)

        loginUrl = self.loginURL
        print(self.loginURL , post , self.myHeader)


        html = None
        response = None
        try:

            req = urllib.request.Request(
                url=self.loginURL,
                data=post,
                headers=self.myHeader
            )
            response = urllib.request.urlopen(req)
            #由于前面进行了编码，所以这里需要进行解码
            text = response.read().decode("gbk")
            if text:
                p = re.compile('location\.replace\([\'|"](.*?)[\'|"]\)')
                html = p.search(text).group(1)
                print("html:", html)
        except urllib.request.URLError as e:
            if hasattr(e, 'code'):
                error_info = e.code
            elif hasattr(e, 'reason'):
                error_info = e.reason
        finally:
            if response:
                response.close()
        if html:
            # 保存cookie到cookie.txt中
            # self.cj.save(ignore_discard=True, ignore_expires=True)
            # mycookies = " "
            # for c in self.cj:
            #     mycookies += c.name + '=' + c.value + ';'
            print(self.cj)
            #：-）为什么Python2中open模式“wb”仍然可以写字符串，Python3中不行。真是醉了
            with open("mycookies.txt", 'w+') as f:
                for cookie in self.cj:
                    print("cookie",cookie)
                    f.write(str(cookie) + '\n')
            cookiejar = self.cj
            return html
        else:
            return error_info

    def getCookieInfo(self):
        with open("mycookies.txt") as f:
            cookiejar = f.read()
        p = re.compile('\<Cookie (.*?) for .sina.com.cn\/\>')
        p2 = re.compile('\<Cookie (.*?) for .login.sina.com.cn\/\>')
        cookies1 = re.findall(p, cookiejar)
        cookies2 = re.findall(p2, cookiejar)
        mycookie = {}
        for cookie in cookies1:
            total = cookie.split('=')
            mycookie[total[0]] = total[1]
        for cookie in cookies2:
            total = cookie.split('=')
            mycookie[total[0]] = total[1]
        return mycookie


if __name__ == '__main__':
    myweibo = WeiboLogin()
    html = myweibo.login()
    print("hhahahah",html)
    # cookiejar = cookielib.MozillaCookieJar()
    # print cookiejar.load('mycookies.txt')
    with open("mycookies.txt") as f:
        cookiejar = f.read()
    p = re.compile('\<Cookie (.*?) for .sina.com.cn\/\>')
    p2 = re.compile('\<Cookie (.*?) for .login.sina.com.cn\/\>')
    cookies1 = re.findall(p, cookiejar)
    cookies2 = re.findall(p2, cookiejar)
    print(cookies1)
    mycookie = {}
    for cookie in cookies1:
        total = cookie.split('=')
        mycookie[total[0]] = total[1]
    for cookie in cookies2:
        total = cookie.split('=')
        mycookie[total[0]] = total[1]

    print(mycookie)

    print("last:",myweibo.getCookieInfo())





