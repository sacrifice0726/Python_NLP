import os

class make_dictionary():
    
    #   存放路徑
    def __init__(self):
        print(" jieba分詞:   1")
        print(" 生成字典請按: 2")
        print(" 進行編碼請按: 3")
        self.select=input(str(" 請輸入      :" ))
        self.raw_path = os.path.abspath('Data/Raw_process_data')+'/'
        self.url_path = os.path.abspath('Data/url_data')+'/'
        self.bug_path = os.path.abspath('Data/Bug_data')+'/'
        self.dict_path = os.path.abspath('Data/Dictionary')+'/'
        self.encoding_path = os.path.abspath('Data/Encoding_data')+'/'
        self.tokenizer_path = os.path.abspath('Data/Token_jieba_data')+'/'
        self.name = os.listdir(self.raw_path)
        
    #   打開原始csv檔案，並且用jieba，dict去重
    def tokenizer(self,name):
        import jieba
        import jieba.analyse
        jieba.load_userdict("./userdict.txt")
        list1=[]
        with open("{}{}".format(self.raw_path,name),"r",errors="ignore") as f:
            for line in f.readlines():
                category,remark=line.split('\t')
                char=','.join(jieba.cut(remark, cut_all=False, HMM=True))
                if self.select == "1" :
                    with open ("{}{}".format(self.tokenizer_path,name),"a") as fw:
                        fw.write(category+'\t'+char)
                        
                    
                ch=char.split(',')
                for i in range(0,len(ch)):
                    list1.append(ch[i])
            
        list1.sort()        
        list2 = list(dict.fromkeys(list1))
        return list2
    
    def jieba_tokenizer(self,name):
        list1=[]
        with open("{}{}".format(self.tokenizer_path,name),"r",errors="ignore") as f:
            for line in f.readlines():
                category,char=line.split('\t')
                
                ch=char.split(',')
                for i in range(0,len(ch)):
                    list1.append(ch[i])
            
        list1.sort()        
        list2 = list(dict.fromkeys(list1))
        return list2
    
    
    #   加載字典    
    def load_dic(self,ch,dic_len):
        with open ("{}dict.csv".format(self.dict_path),"a+") as f:
            f.seek(0,0)
            key=f.readlines()
            if len(key) != 0:
                word=eval(key[0])
                if dic_len == True :
                    return word[ch]
                else :
                    return word
            else:
                return {}
             
    #   生成數字字典
    def make_dict(self,list):
        complete_dict_csv_path = "{}dict.csv".format(self.dict_path)  
        dic={}
        character=self.jieba_tokenizer(list)  #返回去重後的文字list
        word=self.load_dic(None,dic_len=False) #返回word 類型dict
        count=len(word)+1
       
        for ch in character: 
            if ch not in word:
                dic[ch]=count
                count+=1

        with open(complete_dict_csv_path,"w+") as f:
            c={**word,**dic}      
            f.write(str(c))
     
    #   加載原始數據傳給encodig_data            
    def load_raw_data(self,list):
        """
        目的：加載數據並傳給encoding_data做編碼
        """
        with open ("{}dict.csv".format(self.dict_path),"a+") as f:
            f.seek(0,0)
            key=f.readlines()
            dict_encoding=eval(key[0])
            
        with open("{}{}".format(self.tokenizer_path,list),"r") as f1:
            for line in f1.readlines():
                category,comment=line.split('\t')
                self.encoding_data(list,comment,category,dict_encoding)        
           
    #   對分詞完進行數字編碼     
    def encoding_data(self,list,comment,category,dict_encoding):
        """
        目的：編碼用
        """
        
        path=self.encoding_path+"{}".format(list)
        with open (path,"a" ) as fw:
            fw.write(category+'\t')
            comment = comment.replace('\n','')
            comment = comment.split(',')
            
            for i in range(0,len(comment)): 
                if comment[i] != '' and comment[i] != '/':
                    dic=dict_encoding[comment[i]]
                    fw.write(str(dic)+',')                    
                    
                if i==(len(comment)-1):    
                    fw.write('\n') 
                     
    def run(self):
        name=self.name
        print(self.name)
        
        for list in name:
            if list.endswith('csv'):
                if self.select == "1":
                    self.tokenizer(list)    #   進行jieba分詞
                elif self.select == "2":
                    self.make_dict(list)  #   生成字典
                elif self.select == "3":
                    if "{}".format(list) not in os.listdir(self.encoding_path):
                        self.load_raw_data(list)   # 將原始數據進行字典編碼
                else:
                    print(" 請選擇正確指令!!!!!!!!")
                    break
                      
if __name__=='__main__':
    dict2=make_dictionary()
    dict2.run()