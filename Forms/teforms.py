import requests as rq
import time
from spt.speech import speech_to_text
from spt.tts import say

class google_forms():
    
    def __init__(self) :
        self.payload = {}
        self.day = time.ctime()
        self.month ={'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','July':'7','Aug':'8','Sept':'9','Ouc':'10','Nov':'11','Dec':'12'}
        self.payload['fvv'] = '0'
        self.payload['draftResponse']= '[]'
        self.payload['fbzx'] ='-3215123678769399173'
        self.url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSdvgFFLw3L7KFGUMLJL70YfChwOl4Q9zp1eSHkP9bW1TdkpxQ/formResponse'
        
    #   簡意問卷調查
    def page_0(self,category,commit) :
    
        if category in ['好','很好','非常好']:
            self.payload['entry.152147693']= '好'
        elif category in ['不好','不太好','很爛','爛透了','非常爛']:
            self.payload['entry.152147693']= '很爛'
        else:
            self.payload['entry.152147693']= '普通'
            
        date = self.day.split(' ')
        self.payload['entry.1944228548_year']= date[4]
        self.payload['entry.1944228548_month']= self.month[date[1]]
        self.payload['entry.1944228548_day']= date[2]
        self.payload['entry.122087055']= commit
    
    #   發送請求
    def send_requests(self,category,commit):
        #   處理日期、姓名及作業項目
        self.page_0(category,commit)
        try :
            res = rq.post(self.url, data=self.payload)
            res.raise_for_status()
            if res.status_code == 200 :
                print('Work progress has been sent')
        except rq.HTTPError:
            print(self.payload)
            print('HTTP Error!')
            
    def run(self):
        say('what is the service status')
        service_status = speech_to_text()
        say("Other commit")
        commit = speech_to_text()
        
        commit = "xxxxx可以改善得更好 , {}".format (time.ctime())
        print(commit)
        self.send_requests(service_status,commit)
        
if __name__=='__main__':
    c = google_forms()
    c.run()