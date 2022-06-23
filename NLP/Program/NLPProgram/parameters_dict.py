import os
dict_path = os.path.abspath("NLP/Program/NLPProgram")+'/'


#   加載超參數
def load_parameters_dict(dataset,dic_num):
    with open("{}dict_para.csv".format(dict_path),"r") as f:
        key=f.readlines()
        if len(key) != 0:
            word=eval(key[dic_num])
            return word['number_tag'],word["embedding_dim"],word["hidden_dim"],word["dropout"],word["lr"],word["wight_decay"],word["max_epoch"],word["batch_size"],dic_num

#   寫超參數
def write_dict():
    with open("dict_para.csv","r") as f:
        print("即將添加到第 %s 行" %(len(f.readlines())))
        
    dic={}  
    embedding_size=dic["embedding_dim"]= int(input("請輸入embedding_size(0~128)： "))
    hidden_dim = dic["hidden_dim"] = int(input("請輸入hidden_dim(0~256)： "))
    dropout=dic["dropout"] = float(input("請輸入dropout(0~1)： "))
    lr=dic["lr"] = float(input("請輸入lr(0.000001~1)： "))
    wight_decay=dic["wight_decay"] = float(input("請輸入wight_decay(1e-3~1e-10)： "))
    
    max_epoch=dic["max_epoch"] = int(input("請輸入max_epoch(0 以上)： "))
    batch_size=dic["batch_size"] = int(input("請輸入batch_size(16以上)： "))

    if embedding_size <1 or hidden_dim <1:
        print("輸入數值異常，請再確認。您輸入的數值為: "+'\n',
              "embedding_dim:" ,str(embedding_size)+'\n',
              "hidden_din: " ,str(hidden_dim)+'\n')
        exit()

    with open("dict_para.csv","a") as f:
        f.write(str(dic)+'\n')
        
            
if __name__=='__main__':
    # while True:
    #     write_dict()
    pass



