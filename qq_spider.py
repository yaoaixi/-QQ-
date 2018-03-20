#coding:utf-8
from  selenium import webdriver
import requests
import time
import os
from urllib import parse
import configparser

class Spider(object):
    def __init__(self):
        self.web=webdriver.Chrome()
        self.web.get('https://user.qzone.qq.com')
        config = configparser.ConfigParser(allow_no_value=False)
        config.read('userinfo.ini')
        self.__username =config.get('qq_info','qq_number')
        self.__password=config.get('qq_info','qq_password')
        self.headers={
                'host': 'h5.qzone.qq.com',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.8',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'connection': 'keep-alive'
        }
        self.req=requests.Session()
        self.cookies={}

    

    def login(self):
        self.web.switch_to_frame('login_frame')
        log=self.web.find_element_by_id("switcher_plogin")
        log.click()
        time.sleep(1)
        username=self.web.find_element_by_id('u')
        username.send_keys(self.__username)
        ps=self.web.find_element_by_id('p')
        ps.send_keys(self.__password)
        btn=self.web.find_element_by_id('login_button')
        time.sleep(1)
        btn.click()
        print("获取g_tk中,请稍后...")
        time.sleep(2)
        self.web.get('https://user.qzone.qq.com/{}'.format(self.__username))
        cookie=''
        for elem in self.web.get_cookies():
            cookie+=elem["name"]+"="+ elem["value"]+";"
        self.cookies=cookie
        self.get_g_tk()
        self.headers['Cookie']=self.cookies
        self.web.quit()
        
    
    def get_frends_url(self):
        url='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?'
        params = {"uin": self.__username,
              "follow_flag": 0,
              "groupface_flag": 0,
              "fupdate": 1,
              "g_tk": self.g_tk}
        url = url + parse.urlencode(params)
        return url

    def get_frends_num(self):
        url=self.get_frends_url()
        page=self.req.get(url=url,headers=self.headers)
        if not os.path.exists("./frends/"):
            os.mkdir("frends/")
        with open('./frends/'+'0.json','w',encoding='utf-8') as w:
            w.write(page.text)

    def get_mood_url(self):
        url='https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        params = {
              "sort":0,
                  "start":0,
              "num":20,
            "cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
              "replynum":100,
              "callback":"_preloadCallback",
              "code_version":1,
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
              "format":"jsonp",
              "need_private_comment":1,
              "g_tk": self.g_tk
              }
        url = url + parse.urlencode(params)
        return url


    def get_mood_detail(self):
        from getFrends import frends_list
        url = self.get_mood_url()
        for u in frends_list[0:]:
            t = True
            QQ_number=str(u['uin'])
            url_ = url + '&uin=' + QQ_number
            pos = 0
            name=u['remark']
            if u['remark']=="":
                if u['name']=="":
                    name=QQ_number
                else:
                    name=u['name']
            print("开始抓取", QQ_number+"-"+ name,"的数据...")
            while (t):
                url__ = url_ + '&pos=' + str(pos)
                mood_detail = self.req.get(url=url__, headers=self.headers)
                if "\"msglist\":null" in mood_detail.text:
                    if pos==0:
                        print("该空间没有说说数据...\n")
                    else:
                        print("完成...\n")
                    t = False
                elif "\"message\":\"对不起,主人设置了保密,您没有权限查看\"" in mood_detail.text:
                    print("对不起,主人设置了保密,您没有权限查看,(扎心了老铁！）\n")
                    t = False
                else:
                    print("说说", QQ_number, name, (pos + 1), "-", (pos + 20))
                    print ("ykk",mood_detail.text)
                    if not os.path.exists("./mood_detail/"):
                        os.mkdir("mood_detail/")
                    if not os.path.exists("./mood_detail/" + name):
                        os.mkdir("mood_detail/"+name)
                    with open('./mood_detail/'+name+"/" +QQ_number+"_"+ str(pos) + '.json', 'w',encoding='utf-8') as w:
                        w.write(mood_detail.text)
                    pos += 20
            time.sleep(2)


    def get_g_tk(self):
        p_skey = self.cookies[self.cookies.find('p_skey=')+7: self.cookies.find(';', self.cookies.find('p_skey='))]
        h=5381
        for i in p_skey:
            h+=(h<<5)+ord(i)
        print('g_tk=',h&2147483647)
        self.g_tk=h&2147483647


        

if __name__=='__main__':
    print("欢迎使用本系统，祝您爬取数据愉快！！！")
    print("正在读取配置文件信息...")
    print("调用浏览器...")
    sp=Spider()
    print("模拟登入...")
    sp.login()
    print("获取好友QQ号码...")
    sp.get_frends_num()
    sp.get_mood_detail()

    from data_analys import dataToExcel
