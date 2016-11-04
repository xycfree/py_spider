#/usr/bin/python
#Filename:WeiboLogin.py
#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
    'Accept': '*/*',
    'Origin': 'https://www.zhihu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Xsrftoken': '00bdcdb1f45057399a176c0e3ed64963',

    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',

    'Content-Type': 'application/x-www-form-urlencoded',
    'charset' : 'UTF-8',
    'Referer': 'https://www.zhihu.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'q_c1=2bdfee5a93484e81b580e5144a43a5e7|1475998389000|1475998389000; d_c0="AIDAW7AqqgqPTlPycGPMUg9akKAcxAEdH74=|1475998389"; _za=6b024a97-5737-481c-9128-1fbb88aff5ab; _xsrf=00bdcdb1f45057399a176c0e3ed64963; l_cap_id="ZjJjMjBiN2FmMzYwNDA1NTg2NGNmYzMyMzMyYmE3Y2I=|1476106678|aa88c6d26e779528cbf0c60e9a6625e96e739f27"; cap_id="NWUxNWZjNWRlNTJjNDBlOWI1NGM3ZjYwNzdiNjg3ODI=|1476106678|f06f312579ebd641094b0d030c81cbd37a70b2f5"; _zap=5e37a580-c8fb-4c8c-a431-a7b869957d3d; n_c=1; __utmt=1; __utma=51854390.1662149025.1475998389.1475998389.1476106680.2; __utmb=51854390.2.10.1476106680; __utmc=51854390; __utmz=51854390.1475998389.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|3=entry_date=20161009=1'


}

email1 = "xycfree@163.com"
password1 = "bingpoli123"
remember_me1 = "true"

class zhihu_login():
    """use for signin zhihu
    """
    def __init__(self, email, password, remember_me):
        self.email = email
        self.password = password
        self.remember_me = remember_me

    def get_session(self):
        s = requests.session()
        return s

    def get_request(self):
        s = self.get_session()
        r = s.get("http://www.zhihu.com/#signin", headers=headers)
        print 'r: ', r
        return r

    def get_post_data(self):
        _xsrf = self.get_xsrf()
        post_data = {"email":self.email, "password":self.password, "_xsrf":_xsrf, "remember_me":self.remember_me}
        return post_data

    def get_xsrf(self):
        r = self.get_request()
        soup = BeautifulSoup(r.text,'html.parser')
        _xsrf = soup.find('input', attrs={'name': '_xsrf'})['value']
        print '_xsrf: ', _xsrf
        return _xsrf

    def login_zhihu(self):
        s = self.get_session()
        post_data = self.get_post_data()
        login_url = "https://www.zhihu.com/login/email"
        login = s.post(login_url, post_data,headers=headers,verify=False)
        #print 'result: ', login.text
        resu = json.loads(login.text)
        print resu['r'],resu['msg']
        data = login.json()
        print data['msg']

        r = s.post('https://www.zhihu.com/topic',headers=headers,verify=False)
        print r.text



def main():
#   s = requests.session()
#   r = s.get("http://www.zhihu.com/#signin", headers=headers)

#   _xsrf = get_xsrf(r)

#   post_data = {"email":email, "password":password, "_xsrf":_xsrf, "remember_me":remember_me}
    signin = zhihu_login(email1, password1, remember_me1)
    signin.login_zhihu()

if __name__ == '__main__':
    main()
