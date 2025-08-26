import re
import torch
import numpy as np
import py_vncorenlp
from transformers import AutoModel, AutoTokenizer

torch.manual_seed(42)

# Load VnCoreNLP once at the module level
rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='.')

class TRAKE:
    def __init__(self):
        self.phobert = AutoModel.from_pretrained("vinai/phobert-base-v2")
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

    def query_summary(self, text: str) -> list[str]:
        """
        Chuyển text về các danh sách khoảnh khắc.
        Nếu btc làm đúng định dạng, thì chỉ cần tách các chữ phía sau số.
        Ví dụ {Query_dài_dòng}: (1) giậm nhảy, (2) bay qua xà, (3) tiếp đất, (4) đứng dậy."
                -> ["giậm nhảy", "bay qua xà", "tiếp đất", "đứng dậy"].
        """
        moments = re.findall(r"\(\d+\)\s*([^,\.]+)", text)
        return [moment.strip() for moment in moments]

    def word_segment(self, moments: list[str]):
        """
        Tách các từ ra (nếu là một từ phức).
        """
        results = [rdrsegmenter.word_segment(sent)[0].lower() for sent in moments]
        return results

    def query_embedding(self, moments: list[str]):
        """
        Embedding query bằng PhoBert
        """
        results = []
        for sent in moments:
            input_ids = torch.tensor([self.tokenizer.encode(sent)])
            with torch.no_grad():
                features = self.phobert(input_ids).pooler_output  # Mean pooling
            results.append(features.squeeze().numpy())
        return np.array(results)


if __name__ == "__main__":
    trake = TRAKE()

    # Test các khoảnh khắc
    query = "Tìm 4 khoảnh khắc chính khi vận động viên thực hiện cú nhảy: " \
            "(1) giậm nhảy, (2) bay qua xà, (3) tiếp đất, (4) đứng dậy"
    moments = trake.query_summary(query)
    print("Moments:", moments)

    # Test word segment
    wseg = trake.word_segment(moments)
    print("Word segmented:", wseg)

    # Test query embedding
    query_emb = trake.query_embedding(moments)
    print("Query embedding shape:", query_emb.shape)