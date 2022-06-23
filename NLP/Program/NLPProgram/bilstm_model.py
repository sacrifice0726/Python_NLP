import torch
import torch.nn as nn
from TorchCRF import CRF

#   建立模型
class classify_LSTM(nn.Module):
    
    def __init__(self,config) :
        super(classify_LSTM,self).__init__()
        self.embedding_dim = config.embedding_dim
        self.hidden_dim = config.hidden_dim
        self.vocab_size = (config.vocab_size+1)
        self.num_tags = config.num_tags
        self.dropout_config = config.dropout
        
        self.embeds = nn.Embedding(num_embeddings=self.vocab_size,\
                                   embedding_dim=self.embedding_dim,
                                   padding_idx=0,
                                   max_norm=1,
                                   scale_grad_by_freq=True)
        self.dropout = nn.Dropout(self.dropout_config)
        
        self.lstm = nn.LSTM(
            self.embedding_dim,
            self.hidden_dim // 2,
            num_layers=1,
            bidirectional=True, # True 雙向
            batch_first=True, 
        )
        
        self.linear = nn.Linear(self.hidden_dim,self.num_tags)
        self.crf = CRF(self.num_tags)
          
    def forward(self,y,mask):
        embeddings = self.embeds(y)
        feats, hidden = self.lstm(embeddings)
        emissions = self.linear(feats)
        outputs = self.crf.viterbi_decode(emissions,mask)
        return outputs

    def log_likelihood(self, x, y,mask):
        embeddings = self.embeds(y)
        feats, hidden = self.lstm(embeddings)
        emissions = self.linear(self.dropout(feats))
        loss = -self.crf.forward(emissions,x,mask)
        return torch.sum(loss)
        