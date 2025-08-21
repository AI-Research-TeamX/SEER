import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 16})

# 类别和方法
categories = ['Easy', 'Hard', 'All']
methods = ['SEER', 'SEER (query-based)', 'SEER (w/o s2)', 'SEER (w/o s3)']

# 每种类别下不同方法的准确率
easy = [0.679, 0.675, 0.643, 0.561]
hard = [0.311, 0.305, 0.255, 0.301]
overall = [0.507, 0.502, 0.462, 0.440]

# 转置数据
data = np.array([easy, hard, overall]).T
data = data * 100

x = np.arange(len(categories))
width = 0.2  # 为容纳更多柱子，稍微减小宽度

colors = ['#4f81bd', '#c0504d', '#f79646', '#9bbb59']  # 深蓝、深红、深橙、深绿
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # 蓝，橙，绿，红

fig, ax = plt.subplots()

# 绘图，并设定颜色
for i in range(len(methods)):
    bars = ax.bar(x + (i - 1.5) * width, data[i], width, label=methods[i], color=colors[i])
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10,
                    )

# 设置标签
ax.set_ylabel('Accuracy (%)')
ax.set_xticks(x)
ax.set_ylim(0, 78)
ax.set_xticklabels(categories)
ax.legend(loc="upper right", fontsize=12)

plt.tight_layout()
plt.savefig('ablation.pdf')
