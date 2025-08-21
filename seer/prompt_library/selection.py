from prompt_library.library import Library
from sentence_transformers import SentenceTransformer
import json
import numpy as np

class ExampleSelection():
    '''
    This class is used to select examples for the prompt.
    '''
    def __init__(self, init_path):
        self.library = Library(init_path)
        self.model = SentenceTransformer('BAAI/bge-large-en-v1.5')

        self.embedding_cache = {}
        self.init_cache()

    def init_cache(self):
        # init embedding cache, key is question, value is embedding
        questions = [data['question'] for data in self.library.data]
        embeddings = self.model.encode(questions, normalize_embeddings=True)
        for question, embedding in zip(questions, embeddings):
            self.embedding_cache[question] = embedding

        # init embedding cache, key is steps, value is embedding of steps
        steps_list = ['\n'.join(data['steps']) for data in self.library.data]
        embeddings = self.model.encode(steps_list, normalize_embeddings=True)
        for steps, embedding in zip(steps_list, embeddings):
            self.embedding_cache[steps] = embedding

    def hit_cache(self, query):
        if self.embedding_cache.get(query, None) is not None:
            # if hit, return the embedding
            return self.embedding_cache[query]
        else:
            # if not hit, calculate the embedding and add to cache
            embedding = self.model.encode(query, normalize_embeddings=True)
            self.embedding_cache[query] = embedding
            return embedding

    def join_text(self, data: list[dict]):
        # assert isinstance(data, list)
        # assert all([isinstance(dd, dict) for dd in data])
        # assert all(['full_text' in dd for dd in data])
        test_list = [dd['full_text'] for dd in data]
        return '\n\n'.join(test_list) + '\n\n'

    def select_all(self):
        return self.library.data
    
    def select_random(self, num):
        print(f"----select_random----")
        return self.library.get_random(num)
    
    def select_goal_oriented(self, num, question, tools, classification):
        # query-based selection
        print(f"----select_goal_oriented----")
        target_embeddings = self.hit_cache(question)

        indexs = list(range(self.library.count))
        candidate_embeddings = np.array([self.hit_cache(data['question']) for data in self.library.data])
        similarity = target_embeddings @ candidate_embeddings.T

        # 0-1 score
        tool_match_score = np.array([
            len(set(tools) & set(data['tools'])) / len(tools) if len(tools) > 0 else 0
            for data in self.library.data
        ])
        class_score = np.array([data['class'] == classification for data in self.library.data])
        scores = similarity + tool_match_score + class_score
        # print(f"score: {scores} = {similarity} + {tool_match_score} + {class_score}")

        indexs = [index for _, index in sorted(zip(scores, indexs), reverse=True)]
        return self.library.get_by_index(indexs[:num])

    def select_process_oriented(self, num, steps, tools, classification):
        # trajectory-based selection
        print(f"----select_process_oriented----")
        steps_str = '\n'.join(steps)
        target_embeddings = self.hit_cache(steps_str)

        indexs = list(range(self.library.count))
        candidate_embeddings = np.array([self.hit_cache('\n'.join(data['steps'])) for data in self.library.data])
        similarity = target_embeddings @ candidate_embeddings.T

        # 0-1 score
        tool_match_score = np.array([
            len(set(tools) & set(data['tools'])) / len(tools) if len(tools) > 0 else 0
            for data in self.library.data
        ])
        class_score = np.array([data['class'] == classification for data in self.library.data])
        scores = similarity + tool_match_score + class_score
        # print(f"score: {scores} = {similarity} + {tool_match_score} + {class_score}")

        indexs = [index for _, index in sorted(zip(scores, indexs), reverse=True)]
        return self.library.get_by_index(indexs[:num])

    def select_mix_oriented(self, num, quesiton, classification, tools, params, steps):
        raise NotImplementedError
    
    def solver_select(self, strategy, num, quesiton, classification, tools, params, steps):
        print(f"----SELECT_DEBUGGING_START----")
        print(f"INPUT: strategy: {strategy}, num: {num}, quesiton: {quesiton}, classification: {classification}, tools: {tools}, params: {params}")

        if num == 0: res = []
        if num >= self.library.count: res = self.select_all()
        # case strategy: random, goal_oriented, process_oriented, mix_oriented
        if strategy == 'random':
            res = self.select_random(num)
        elif strategy == 'goal_oriented':
            res = self.select_goal_oriented(num, quesiton, tools, classification)
        elif strategy == 'process_oriented':
            res = self.select_process_oriented(num, steps, tools, classification)
        elif strategy == 'mix_oriented':
            res = self.select_mix_oriented(num, quesiton, classification, tools, params, steps)
        else:
            raise ValueError("Invalid strategy")
        
        print_res = '\n'.join([f"-- Question: {dd['question']}; tools: {dd['tools']}; parameters: {dd['parameters']}" for dd in res])
        print(f"OUTPUT: selected examples: \n{print_res}")
        print(f"----SELECT_DEBUGGING_END----")
        return self.join_text(res)
    
    def add_example(self, example):
        """ example data format
        {
            'question':str
            'key':str
            'class':str
            'tools':[]
            'paras':[]
            'steps':[]
            'results':[]
            'answer':str
            'scratchpad':str,
            'scratchpad_library':str
        }
        """
        data = {
            "id": f"id_{self.library.count + 1}",
            "class": example['class'],
            "question": example['question'],
            "steps": example['steps'],
            "tools": example['tools'],
            "parameters": example['paras'],
            "full_text": example['scratchpad_library'].strip(),
        }
        print(f"{'='*10}ADD_EXAMPLE{'='*10}")
        print(json.dumps(data, indent=4))
        
        self.library.add_data(data)

    def save_library(self, path):
        self.library.save_data(path)
