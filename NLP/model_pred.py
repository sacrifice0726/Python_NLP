from torch import tensor,load
from jieba import cut
import jieba.analyse
import time
jieba.load_userdict("NLP/userdict.txt")

"""
模型評論分析
"""
#   分詞及編碼
def inp_tokenization(input_str,word_to_id):
    inp_to_jieba = ','.join(cut(input_str, cut_all=False, HMM=True))

    input_vec = []
    inp_to_jieba = inp_to_jieba.split(',')
    for char in inp_to_jieba:
        if char not in word_to_id:
            input_vec.append(0)
        else:
            input_vec.append(word_to_id[char])
    return input_vec

#   預測店家種類   
def predict_type(input_str):
    from NLP.Program.NLPProgram.torch_dataloader_type import create_dataloader,load_data
    
    device, model=create_dataloader()
        
    label_to_id,id_to_label,word_to_id,id_to_word,\
        = load_data("complete.pkl")
        
    input_vec = inp_tokenization(input_str,word_to_id)
        
    model.load_state_dict(load("NLP/model_type.pkl"))
    model.eval()
    
    # convert to tensor
    sentences = tensor(input_vec).view(1, -1).to(device)
    mask = (sentences > 0).to(device)
    paths = model(sentences, mask)
    # print("判別店家為： " , paths[0][0])
    
    return paths[0][0]

#   預測好壞評論
def predict_comment_analyse(input_str):
    from NLP.Program.NLPProgram.torch_dataloader_comment import create_dataloader,load_data
    
    device,model=create_dataloader()
        
    label_to_id,id_to_label,word_to_id,id_to_word,\
         = load_data("complete.pkl")
    
    input_vec = inp_tokenization(input_str,word_to_id)
    model.load_state_dict(load("NLP/model_comment.pkl"))
    model.eval()
    
    # convert to tensor
    sentences = tensor(input_vec).view(1, -1).to(device)
    mask = (sentences > 0).to(device)
    paths = model(sentences, mask)
    # print("判別評論為： " , paths[0][0])
    
    return paths[0][0]

#   執行手動輸入並得出結果
def run(input_str):
    print("加載時間開始      ： ", time.ctime())
    from spt.speech import speech_to_text
    print("加載完成speech時間： ", time.ctime())
    from spt.tts import say
    print("加載完成tts時間   ： ", time.ctime())
    
    while True:
        if input_str == "":
            input_str = speech_to_text()    
            if input_str == "結束分析":break
            print(input_str)
        
        
        result_comment = predict_comment_analyse(input_str)
        result_type = predict_type(input_str)
        
        id_to_label = {"1":"bad review","2":"good review","3":"Hostel","4":"Restaurant","5":"KTV"}
        
        category = id_to_label[str(result_type)]
        review = id_to_label[str(result_comment)]
        
        print("提取評論： ",input_str)
        print("商家種類： ",category)
        print("好壞評論： ",review)
        say ("{} and {}".format(category , review))
        print("=========================================================================================================================================")
          
#   執行多個評論分析
def comment_list():
    A = "超呼想像的餐廳 好吃 料實在新鮮。湯頭很棒。下次還要來" 
    B = "用餐前未告知菜單註明有甜點❌實際並沒有（補一瓶養樂多???）這是什麼意思???自助吧沒有爆米花、冰淇淋❌"
    C = "非常感謝各個服務人員的親切與辛勞，能夠住在這邊我覺得非常幸運，中間曾經因為私人因素需要延長入住時間，但櫃檯服務人員也沒有嫌麻煩，反而每次接聽電話都非常的有耐心。"
    D = "酒店網路差且經常跳掉，服務人員態度不佳，食物變化多，但晚餐都較不優。提供外送服務，不過送上來的時間都非常不一定。"
    E = "很不錯的地方，每次早一點去會員都可以唱5個小時，有供餐，水餃超好吃👍👍👍"
    F = "全面禁菸,但是一半以上的包廂和員工都在抽菸的地方,本來想說禁煙才來,一上去就是嗆鼻的菸味,唱到一半還有人在門口開抽？？？"

        

# comment_list()

