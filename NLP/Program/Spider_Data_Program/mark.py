import os
import pandas as pd


data_csv_path = os.path.abspath('Data/Raw_data')+'/'
data_process_path=os.path.abspath('Data/Raw_process_data')+'/'
data_list=os.listdir(data_csv_path)

def data_classify_by_pandas(name):
    # print(name)
    list1=[]
    with open ("{}restaurant2.csv".format(data_process_path),"a+") as fw2 , \
        open ("{}hostel2.csv".format(data_process_path),"a+") as fw1, \
        open("{}KTV2.csv".format(data_process_path),"a+") as fw3:
        
        df=pd.read_csv("{}{}".format(data_csv_path,name),sep="\t",names=["comment"],index_col=0,on_bad_lines="skip") #讀取csv 按\t拆分 並賦予列名
        
        ds=df.sample(frac=1)    #打亂讀取
        
        for i in range(0,len(ds)):
            if len(ds["comment"][i]) > 2:
                data=ds.index[i]+"\t"+ds["comment"][i]+'\n'
            
                if ds.index[i]=="A" and list1.count("A")<500 : 
                    fw1.write(data),list1.append(ds.index[i])
                elif ds.index[i]=="B" and list1.count("B")<400 : 
                    fw1.write(data),list1.append(ds.index[i])
                elif ds.index[i]=="C" and list1.count("C")<230 : 
                    fw2.write(data),list1.append(ds.index[i])
                elif ds.index[i]=="D" and list1.count("D")<236 : 
                    fw2.write(data),list1.append(ds.index[i])
                elif ds.index[i]=="E" and list1.count("E")<300 : 
                    fw3.write(data),list1.append(ds.index[i])
                elif ds.index[i]=="F" and list1.count("F")<280 : 
                    fw3.write(data),list1.append(ds.index[i])
                else:
                    continue
    
def data_count():
    list1=[]
    with open ("{}restaurant2.csv".format(data_process_path),"a+") as fw2 , \
        open ("{}hostel2.csv".format(data_process_path),"a+") as fw1, \
        open("{}KTV2.csv".format(data_process_path),"a+") as fw3:
            
        fw1.seek(0,0),fw2.seek(0,0),fw3.seek(0.0)
        file=[fw1.readlines(),fw2.readlines(),fw3.readlines()]
        for file1 in file:
            for i in file1:
                label,comment=i.split('\t')
                if label=="A":
                    list1.append(label)
                elif label=="B":
                    list1.append(label)
                elif label=="C":
                    list1.append(label)
                elif label=="D":
                    list1.append(label)
                elif label=="E":
                    list1.append(label)
                elif label=="F":
                    list1.append(label)
                else:
                    continue 
    print("數量 A： ",list1.count("A"))
    print("數量 B： ",list1.count("B"))
    print("數量 C： ",list1.count("C"))
    print("數量 D： ",list1.count("D"))
    print("數量 E： ",list1.count("E"))
    print("數量 F： ",list1.count("F"))
    
# data_count()   
         
for name in data_list:
    data_classify_by_pandas(name)
    # pass  