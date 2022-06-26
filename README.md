
## 專案介紹：
#### 在收銀台放置智能音箱，可以辨別ＫＴＶ、餐廳、旅館三個類別，以及評論是否具有對於店家的負面消息，以利於店家完善相關服務。後續可以加上語音翻譯系統，完善用戶體驗。

   ### 1. 數據來源：
   由於想要在Command輸入店家名稱就能進行爬蟲，但礙於Google有一些反爬機制
  （網址內有串無法破譯的代碼：1y3765756447819973575!   2y11794027760928749997! xxxxxxxxx!  1s3Lq3YvjbA4iB-QaZy52gBA!7e81），因此進行以下研究。
  
          1. 本專案是利用爬蟲抓取ＧＯＯＧＬＥ評論進行深度學習的模型訓練。
          2. 爬蟲技術使用Requests、Selenium及PyAutoGUI 進行。
          3. PyAutoGUI 可以開啟開發者工具，抓取爬蟲需要的 JSON 網址，最後丟到Requests進行數據大量抓取。
          
   ### 2. 模型建立：
