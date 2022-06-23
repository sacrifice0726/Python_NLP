import requests
import json
import time
from threading import Thread
import os
import re
from fake_useragent import UserAgent
import random
"""
目的：將google map 評論的重要節點重新拼接後解析其內容，並且將它存成csv檔案
版本：requ-0.0.0.6 正式版
更改內容：刪除代理ip，判斷是否已爬過該檔案。若有不爬，若無則反。
待解決：無
"""

raw_path = os.path.abspath('Data/Raw_data')+'/'
url_path = os.path.abspath('Data/url_data')+'/'

print(os.getcwd())
def replace_all_blank(value):
    """
    去除value中的所有非字母內容，包括標點符號、空格、換行、下劃線等
    :param value: 需要處理的內容
    :return: 返回處理後的內容
    """
    # \W 表示匹配非數字字母下劃線
    result = re.sub('\W+', '/', value)
    result2 = result.replace("/由/Google/提供翻譯/","")
    result3 = result2.replace("原始評論",",")
    result3 = result3.split(',')
    return result3[0]

class url_request():
    
    def __init__(self):
        self.url="https://www.google.com.tw/maps/preview/review/listentitiesreviews?authuser=0&hl=zh-TW&gl=tw&pb=!1m2!{}!{}!2m2!1i{}!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!{}!7e81"
        self.headers=UserAgent().random
        self.headers1={'user-agent': self.headers}
        self.cookie = "anonymid=jk63khrk-y97r4p; _r01_=1; ln_uact=mr_mao_hacker@163.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20180720/1740/main_JAWQ_0aa000000ceb195a.jpg; _ga=GA1.2.273332130.1532825428; depovince=HUN; JSESSIONID=abcE5k0CiAJDc9ESVEcuw; ick_login=026ba348-e4e9-4871-9ce3-5868b95cfdd3; first_login_flag=1; loginfrom=syshome; wp_fold=0; BAIDU_SSP_lcr=https://www.baidu.com/link?url=VRx_HKUd53I5rYWZHvrQ9VVLotqST6-jtaZDlscFYCO&wd=&eqid=e957aec400037928000000065b64fcab; ick=64518f30-9a22-47df-b3c3-4114f185c3c6; t=8fcf47068763c279eea2620b51b7a3311; societyguester=8fcf47068763c279eea2620b51b7a3311; id=967272361; xnsid=fd736c63; jebecookies=3f9a3853-3371-4857-8268-308d663ca146|||||; jebe_key=19041c4e-4d38-4dc1-bfb9-124b81afae61%7C33b1d8f602cf6dd5a9834fe6f2bf97f2%7C1533346094265%7C1%7C1533346099750"
        self.cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in self.cookie.split("; ")}
        self.proxy1 = {
        "https": "http://210.61.124.17:80"
        }
        self._running = True
        
    def terminate(self,n):
        if n==u"None" : self._running = False
        
    def get_complete_url(self,list):
        name_category,parameter = list.split('\t')
        category,name = name_category.split(',')
        parameter1,parameter2,parameter3=parameter.split(',')
    
        for page in range(0,10000,10):
            if self._running==True :
                url_new=self.url.format(parameter1,parameter2,page,parameter3)
                self.get_response(url_new,category,name,page+1)
                time.sleep(random.randint(5,30))
            else:
                print(self._running)
                break
     
    def get_response(self,url_new,category,name,count):
        user_agent=UserAgent(use_cache_server=False)
        html1=requests.get(url=url_new,headers=self.headers1,cookies=self.cookie_dict)
        html=html1.text
        #print(html)
        pretext = ')]}\''
        text = html.replace(pretext,'')
        # 把字串讀取成json
        soup = json.loads(text)
        self.save_csv(soup,category,name,count)
    
    def label(self,category,sorce_new):
        label={("旅館",1):"A",("旅館",5):"B",
               ("餐廳",1):"C",("餐廳",5):"D",
               ("KTV",1):"E",("KTV",5):"F"}
        return label[category,sorce_new]
    
    def save_csv(self,soup,category,name,count):
        # 取出包含留言的List 。
        none_type=0
        if count>1 :count=count-1
        print("進度條:",count)
        conlist = soup[2]
        for i in conlist:
            comment=replace_all_blank(str(i[3]))+'\n' 
            sorce_new=5 if int(i[4])>=4 else 1
            new_label=self.label(category,sorce_new)
            with open("{}{}.csv".format(raw_path,name),"a") as f:
                if str(i[3])!=u"None":
                    f.write(new_label+'\t'+comment)
                else:
                    self.terminate(str(i[3]))
                 
                if count %20 == 0:
                    print("評論:"+comment)
                    print('_______________________________________________________________')
                    count=count+1
                    time.sleep(1)
    
    def run(self,name):
        while self._running :
            self.get_complete_url(name)
            time.sleep(1)

    
if __name__=="__main__":
    list1=[]
    times=0  
    with open ("{}Raw_url.csv".format(url_path),"r") as f:
        for parameter_csv in f.readlines():
            category_name,position=parameter_csv.split('\t')
            category,name=category_name.split(",")
            if "{}.csv".format(name) not in os.listdir(raw_path):
                list1.append(parameter_csv)
                
    print("即將抓取以下數據",list1)
    print("等待時間 3秒 ")
    time.sleep(1)
    print("等待時間 2秒 ")
    time.sleep(1)
    print("等待時間 1秒 ")
    time.sleep(1)
    print("開始抓取 ")
    
    for i in list1:            
        spider=url_request()
        t1 = Thread(target=spider.run,args=(i, ))
        t1.start()
        t1.join()
        print("end")
        

    
