import os
import pickle
import torch 
from parameters_dict import load_parameters_dict
from bilstm_model import classify_LSTM

# pkl_path = os.path.abspath('Data/data_pkl')+'/'
pkl_path = os.path.abspath('NLP/Data/data_pkl/type_data_pkl')+'/'

#   create load data by pickle 
def load_data(dataset):
    with open("{}{}".format(pkl_path,dataset),"rb") as inp:
        
        label_to_id = pickle.load(inp)
        id_to_label = pickle.load(inp)
        
        word_to_id = pickle.load(inp)
        id_to_word = pickle.load(inp)
        
        return  label_to_id,id_to_label,word_to_id,id_to_word

def choose_dataset():
    # print("使用 complete_new.pkl 請按 1")
    # print("使用 hostel_new.pkl 請按 2")
    # print("使用 KTV_new.pkl 請按 3")
    # print("使用 restaurant_new.pkl 請按 4")
    # inp = print(input("請輸入要使用的數據集："))
    inp = 1
    if inp == 1:
        dataset = "complete.pkl"
    elif inp == 2:
        dataset = "hostel.pkl"
    elif inp == 3:
        dataset = "KTV.pkl"
    elif inp == 4:
        dataset = "restaurant.pkl"
    else :
        print("查無此數據集")
        quit()
        
    return dataset

print(choose_dataset())

label_to_id,id_to_label,word_to_id,id_to_word,\
=load_data(choose_dataset())

number_tag_dic,embedding_dic,hidden_dic,dropout_dic,lr_dic,weight_decay_dic,\
    max_epoch_dic,batch_size_dic,dic_num_dic=load_parameters_dict(choose_dataset(),0)

#   set torch parameter (embedding_size,hidden_size,dorpout ....)
class Config:
    embedding_dim = embedding_dic
    hidden_dim = hidden_dic
    vocab_size = len(word_to_id)
    # num_tags = len(label_to_id)
    num_tags = 6

    dropout = dropout_dic
    lr = lr_dic
    weight_decay = weight_decay_dic
    
def create_dataloader():
    
    #   craete torch_dataloader , device and train_parameter
    device = torch.device('cpu')
    max_epoch = max_epoch_dic
    batch_size = batch_size_dic
    dic_num = dic_num_dic
    # batch_size = 1  # To test
       
    config = Config()
    model = classify_LSTM(config).to(device)
    return device, model
        
if __name__=="__main__":   
    # load_data()    
    # create_dataloader()
    # classify_LSTM(Config)
    pass