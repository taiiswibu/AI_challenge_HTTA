import os

import torch
from transformers import AutoModel, AutoTokenizer
import py_vncorenlp


# Tải vncorenlp nếu chưa có file, còn ko kệ
#py_vncorenlp.download_model(save_dir='.')

class TextKIS:

    def __init__(self):
        self.rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='.')
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
        self.phobert = AutoModel.from_pretrained("vinai/phobert-base-v2")

    def _word_segment(self, text):
        return self.rdrsegmenter.word_segment(text)
    
    def _text_embedding(self, text):
        """
        Chuyển text sang word segments
        """
        text = self._word_segment(text)
        input_ids = torch.tensor([self.tokenizer.encode(text)])
        with torch.no_grad():
            features = self.phobert(input_ids)
        return features.last_hidden_state # [batch_size, seq-len, hidden_state]
    
    
    def _object_embedding(self, objects):
        pass
    

if __name__ == "__main__":
    kis = TextKIS()
    text = "Ông Nguyễn Khắc Chúc đang làm việc tại Đại học Quốc gia Hà Nội. ABC."
    
    print("\nWord Segment")
    w_segment = kis._word_segment(text)
    print(w_segment)

    print("\nText Encoding")
    emb_text = kis._text_embedding(text)
    print(emb_text.shape)
