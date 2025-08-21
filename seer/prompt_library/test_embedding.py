from FlagEmbedding import FlagModel
from sentence_transformers import SentenceTransformer

model_flag = FlagModel('BAAI/bge-large-en-v1.5')
model_sent = SentenceTransformer('BAAI/bge-large-en-v1.5')

sentences_1 = ["Who is XXX"]
sentences_2 = ["Who is YYY", "Tim is a great writer", "John is a great artist"]

def flag_emb():
    for i in range(1):
        embeddings_1 = model_flag.encode(sentences_1)
        embeddings_2 = model_flag.encode(sentences_2)
        similarity = embeddings_1 @ embeddings_2.T
        print(f"{i}: {similarity}")

def sbert_emb():
    for i in range(1):
        embeddings_1 = model_sent.encode(sentences_1, normalize_embeddings=True)
        embeddings_2 = model_sent.encode(sentences_2, normalize_embeddings=True)
        similarity = embeddings_1 @ embeddings_2.T
        print(f"{i}: {similarity}")

import time
start = time.time()
flag_emb()
end = time.time()
print("Flag Embedding Time: ", end - start)

start = time.time()
sbert_emb()
end = time.time()
print("SBERT Embedding Time: ", end - start)
