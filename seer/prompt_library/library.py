"""
This library is used to maintain an example Library, which includes multiple examples such as:

- Decomposer examples
- Handler examples

示例库是一个dict类型：
{
    "decomposer": {
        "id_1": {
            "class": "flight",
            "question": "xxx",
            "decomposition": ["q1", "q2", ...],
        },
        "id_2": {
            "description": "example2 description",
            "handler": "example2 handler"
        }
    },
    "handler": {

    }
}

"""
from pathlib import Path

folder_path = Path(__file__).parent
file_path = folder_path / 'library.json'

import json
import random
random.seed(42)

class Library:
    def __init__(self, data_path=file_path):
        self.data: list[dict] = None
        self.count: int = 0
        
        with open(data_path, 'r') as f:
            self.data = json.load(f)
        self.count = len(self.data)

    def add_data(self, data):
        self.data.append(data)
        self.count += 1
        assert self.count == len(self.data)

    def get_random(self, k):
        return random.sample(self.data, k)
    
    def get_by_index(self, indexs):
        res_data = [self.data[i] for i in indexs]
        random.shuffle(res_data)
        return res_data

    def save_data(self, data_path):
        with open(data_path, 'w') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    print(Library().data)
