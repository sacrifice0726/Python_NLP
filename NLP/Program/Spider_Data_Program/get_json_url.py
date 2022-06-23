import time
from selenium import webdriver
import pyautogui
import clipboard as c
import os
"""
selenium 爬蟲正式檔案 
編號      0-0.0.6
"""
def mouse_postion():
    while True:
        try:
            print(pyautogui.position())
            time.sleep(1)
        except KeyboardInterrupt:
            print("end")
            break

class selenium_pyautogui_geturl():
    
    def __init__(self) :
        self.raw_path = os.path.abspath('Data/Raw_data')+'/'
        self.url_path = os.path.abspath('Data/url_data')+'/'
        self.bug_path = os.path.abspath('Data/Bug_data')+'/'
        self.category = input( " 請輸入要查詢種類： " )

    def selen_pyau(self,key_word):
        #   指定webdriver.exe路徑
        webdriver_chrome_path= os.path.abspath('chromedriver')
        #   自動打開開發者工具
        options=webdriver.ChromeOptions()
        options.add_argument("--auto-open-devtools-for-tabs")
        driver = webdriver.Chrome(webdriver_chrome_path,chrome_options=options)

        #   預計打開網頁網址
        driver.get("https://www.google.com.tw/maps")

        #   在搜尋欄輸入查詢資訊
        search_input = driver.find_element_by_name("q")
        search_input.send_keys(u'{}'.format(key_word))
        time.sleep(5)

        #   點擊第一個
        try:
            num_seconds = 1.2
            pyautogui.moveTo(200, 250, duration=num_seconds)
            time.sleep(1)
            pyautogui.click()
            time.sleep(5)
        except Exception as e:
            print(e)
            
        #   點擊評論
        pyautogui.click(181, 476, duration=num_seconds)
        
        pyautogui.click(181, 486, duration=num_seconds)
      
        pyautogui.click(181, 496, duration=num_seconds)
        time.sleep(1)
        # pyautogui.click()
        time.sleep(1)
        
        #   鼠標將開發者工具切換到 network
        pyautogui.moveTo(967, 245, duration=num_seconds)
        pyautogui.click()

        #   重新整理
        driver.refresh()

        #   移動到評論區並滑動
        pyautogui.moveTo(316, 400, duration=num_seconds)
        time.sleep(3)
        pyautogui.scroll(-200)
        time.sleep(1)
        pyautogui.scroll(5)

        #  移動到搜尋欄輸入 listentitiesreviews
        pyautogui.moveTo(713, 326, duration=num_seconds)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        # pyautogui.typewrite('listentitiesreviews')
        pyautogui.write('listentitiesreviews',interval=0.2)

        #   移動到listentitiesreviews
        pyautogui.moveTo(724, 503, duration=num_seconds)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)

        #   移動到hearders
        pyautogui.moveTo(913, 473, duration=num_seconds)
        pyautogui.click()

        #   移動到url地址，並且點擊右鍵然後複製
        pyautogui.moveTo(915, 555, duration=num_seconds)
        pyautogui.mouseDown(button='right') 
        pyautogui.moveTo(945, 560, duration=num_seconds)
        pyautogui.click()

        #   等待然關閉網頁
        time.sleep(5)
        driver.close()
        
        self.split_url(key_word)
    
    def split_url(self,key_word):
        #   打印複製的網址
        try:
            url=c.paste()
            url=url.split("!")
            with open ("{}Raw_url.csv".format(self.url_path),"a") as f:
                f.write(self.category+','+key_word+'\t'+url[2]+','+url[3]+','+url[15]+'\n')
        except Exception as e:
            with open("{}bug.csv".format(self.bug_path),"a") as f:
                f.write("{}數據爬取失敗".format(key_word)+ ',' + e + '\n')
            print(e)

    def run(self):
        list1=[]
        list2=[]
        with open ("{}Raw_url.csv".format(self.url_path),"r") as f:
            for i in f.readlines():
                print(i)
                category_name,position=i.split('\t')
                category,name=category_name.split(',')
                list2.append(name)
        print(" 請輸入要查詢內容，若要結束請再按一次『Enter』")
        while True:
            inp=input(str(" 請輸入要抓取內容之名稱： "))
            # inp,none=inp.split('\t')
            if len(inp) == 0 :break
            if inp not in list2:list1.append(inp)
                
        print("即將抓取以下數據:" ,list1)
        pyautogui.click(960,10,duration=1)
        time.sleep(1)
        pyautogui.click(1000, 65, duration=1)
        for i in list1 :
            try:
                self.selen_pyau(i) #調用selenium 程式
            except Exception as e:
                with open("{}bug.csv".format(self.bug_path),"a") as f:
                    f.write("{}-數據爬取失敗".format(i)+ ',' + str(e) + '\n')
                    print(e)
                    
if __name__=='__main__':
    selen=selenium_pyautogui_geturl()
    selen.run()
    # mouse_postion()     #鼠標位置