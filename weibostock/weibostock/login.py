# coding=GBK
import requests
import cookielib
import urllib2
import urllib
import rsa
import binascii
import re
import json
import base64

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
        # 保存cookie
        self.cj = cookielib.MozillaCookieJar(self.cookiefilename)
        cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def _get_servertime(self, username):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % username
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        return servertime, nonce, pubkey, rsakv

    def _get_pwd(self, pwd, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
        pwd = rsa.encrypt(message, key)
        return binascii.b2a_hex(pwd)

    def _get_user(self, username):
        name = urllib.quote(username)
        username = base64.encodestring(name)[:-1]
        return username

    def login(self):
        username = myNumAndPwd["name"]
        password = myNumAndPwd["pwd"]
        print "username:", username
        print "password:",password
        try:
            servertime, nonce, pubkey, rsakv = self._get_servertime(username)
        except:
            print 'Get severtime error!'
            return None
        global postData
        postData['servertime'] = servertime
        postData['nonce'] = nonce
        postData['su'] = self._get_user(username)
        postData['sp'] = self._get_pwd(password, servertime, nonce, pubkey)
        postData['rsakv'] = rsakv
        # # 处理302重定向
        post = urllib.urlencode(postData)

        loginUrl = self.loginURL
        print self.loginURL , post , self.myHeader


        html = None
        response = None
        try:

            req = urllib2.Request(
                url=self.loginURL,
                data=post,
                headers=self.myHeader
            )
            response = urllib2.urlopen(req)
            text = response.read()
            if text:
                p = re.compile('location\.replace\([\'|"](.*?)[\'|"]\)')
                html = p.search(text).group(1)
                #print("html:", html.decode('gbk'))
        except urllib2.URLError as e:
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
            with open("cookies.txt", 'wb+') as f:
                for cookie in self.cj:
                    f.write(str(cookie) + '\n')
            cookiejar = self.cj
            return html
        else:
            return error_info

    def getCookieInfo(self):
        with open("cookies.txt") as f:
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
    print "hhahahah",html
    # cookiejar = cookielib.MozillaCookieJar()
    # print cookiejar.load('mycookies.txt')
    with open("cookies.txt") as f:
        cookiejar = f.read()
    p = re.compile('\<Cookie (.*?) for .sina.com.cn\/\>')
    p2 = re.compile('\<Cookie (.*?) for .login.sina.com.cn\/\>')
    cookies1 = re.findall(p, cookiejar)
    cookies2 = re.findall(p2, cookiejar)
    print cookies1
    mycookie = {}
    for cookie in cookies1:
        total = cookie.split('=')
        mycookie[total[0]] = total[1]
    for cookie in cookies2:
        total = cookie.split('=')
        mycookie[total[0]] = total[1]

    print mycookie

    print "last:",myweibo.getCookieInfo()





