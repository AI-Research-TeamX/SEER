# 数据集存在的问题
## 1
airbnb-easy.jsonl

问题：easy-airbnb-0070 和 easy-airbnb-0077 存在 NaN 问题。jsonlines读取数据出错。
jsonlines.Reader(f).iter(skip_invalid=True) 可以读取，但会跳过。

解决：NaN -> "NaN"

# 2
airbnb-hard.jsonl

问题：hard-yelp-0030 - hard-yelp-0039 名字错了

解决：yelp -> airbnb