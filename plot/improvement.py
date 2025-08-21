import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
easy_goal_oriented = [
    [81.00, 79.00, 87.00, 86.00],  # Flight
    [95.00, 97.00, 96.00, 90.00],  # Coffee
    [80.00, 80.00, 82.00, 80.00],  # Yelp
    [94.00, 95.00, 90.00, 89.00],  # Airbnb
    [33.00, 33.00, 34.00, 36.00],  # Dblp
    [9.00, 4.00, 5.00, 8.00],      # Scirex
    [65.00, 69.00, 66.00, 66.00],  # Agenda
    [74.00, 83.00, 77.00, 79.00],  # Gsm8k
    [66.38, 67.50, 67.12, 66.75]   # Avg (rounded to 2 decimal places)
]
easy_proc_oriented = [
    [37.00, 82.00, 70.00, 81.00],  # Flight
    [87.00, 87.00, 98.00, 95.00],  # Coffee
    [81.00, 90.00, 85.00, 78.00],  # Yelp
    [92.00, 94.00, 92.00, 94.00],  # Airbnb
    [31.00, 37.00, 33.00, 34.00],  # Dblp
    [6.00, 6.00, 5.00, 5.00],      # Scirex
    [64.00, 68.00, 65.00, 68.00],  # Agenda
    [37.00, 79.00, 79.00, 82.00],  # Gsm8k
    [54.38, 67.88, 66.62, 67.12]   # Avg (rounded)
]
hard_goal_oriented = [
    [18.00, 39.00, 39.00, 24.00],  # Flight
    [40.00, 39.23, 43.08, 50.77],  # Coffee
    [60.00, 61.00, 64.00, 62.00],  # Yelp
    [21.00, 24.00, 28.00, 24.00],  # Airbnb
    [27.00, 26.00, 32.00, 30.00],  # Dblp
    [22.00, 24.00, 20.00, 21.00],  # Scirex
    [4.00, 5.00, 6.00, 1.00],      # Agenda
    [27.43, 31.89, 33.44, 30.68]   # Avg
]
hard_proc_oriented = [
    [20.00, 25.00, 17.00, 21.00],      # Flight
    [41.54, 41.54, 40.77, 33.85],      # Coffee
    [52.00, 58.00, 50.00, 56.00],      # Yelp
    [30.00, 33.00, 28.00, 36.00],      # Airbnb
    [23.00, 35.00, 27.00, 40.00],      # Dblp
    [20.00, 23.00, 23.00, 23.00],      # Scirex
    [0.00, 2.00, 0.00, 0.00],          # Agenda
    [26.79, 31.79, 26.39, 29.41]       # Avg
]
def plot_num_demos():
    # labels = ["0-shot", "2-shot", "4-shot", "6-shot", "8-shot"]
    labels = range(0, 10, 2)
    x = range(len(labels))
    # Averaged accuracy values per task type and difficulty
    easy_goal_oriented_avg = [37.13, 66.38, 67.50, 67.12, 66.75]
    easy_proc_oriented_avg = [37.63, 54.38, 67.88, 66.62, 67.12]
    hard_goal_oriented_avg = [18.49, 27.43, 31.89, 33.44, 30.68]
    hard_proc_oriented_avg = [19.04, 26.79, 31.79, 26.39, 29.41]
    # plot easy Traj-based SEER
    fig, axs = plt.subplots(1, 1, figsize=(3, 3), sharex=True, sharey=True)
    # Plotting data into selected subplots
    axs.plot(x, easy_proc_oriented_avg, marker='s', label='Easy', color='#D86C50')
    # axs.plot(x, hard_proc_oriented_avg, marker='o', label='Hard', color='#0BCAC0')
    # Set labels and grid
    axs.set_xticks(x)
    # innner ticks
    axs.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs.set_xticklabels(labels)
    # Add a global legend
    # axs.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=10)
    plt.tight_layout()
    plt.savefig("easy_proc_num_demos.pdf")
    # clear the current figure
    plt.clf()
    plt.close()
    # plot hard Traj-based SEER
    fig, axs = plt.subplots(1, 1, figsize=(3, 3), sharex=True, sharey=True)
    # Plotting data into selected subplots
    axs.plot(x, hard_proc_oriented_avg, marker='s', label='Hard', color='#D86C50')
    # axs.plot(x, easy_proc_oriented_avg, marker='s', label='Easy', color='#D86C50')
    # Set labels and grid
    axs.set_xticks(x)
    axs.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs.set_xticklabels(labels)
    # Add a global legend
    # axs.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=10)
    plt.tight_layout()
    plt.savefig("hard_proc_num_demos.pdf")
    # clear the current figure
    plt.clf()
    plt.close()
    # plot easy and hard together
    fig, axs = plt.subplots(1, 2, figsize=(6, 3))
    # Plotting data into selected subplots
    axs[0].plot(x, easy_proc_oriented_avg, marker='s', label='Easy Traj-based SEER', color='#D86C50')
    axs[1].plot(x, hard_proc_oriented_avg, marker='s', label='Hard Traj-based SEER', color='#D86C50')
    axs[0].set_title("Easy")
    axs[1].set_title("Hard")
    axs[0].yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs[1].yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    # Set labels and grid
    for ax in axs.flat:
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=13)
        ax.tick_params(axis='y', labelsize=13)
        ax.tick_params(axis='x', labelsize=13)
    # Add a global legend
    # axs.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=10)
    plt.tight_layout()
    plt.savefig("easy_hard_proc_num_demos.pdf")
    # clear the current figure
    plt.clf()
    plt.close()
    # plot easy Query-based SEER
    fig, axs = plt.subplots(1, 1, figsize=(3, 3), sharex=True, sharey=True)
    # Plotting data into selected subplots
    axs.plot(x, easy_goal_oriented_avg, marker='s', label='Easy', color='#D86C50')
    # axs.plot(x, hard_goal_oriented_avg, marker='o', label='Hard', color='#0BCAC0')
    # Set labels and grid
    axs.set_xticks(x)
    axs.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs.set_xticklabels(labels)
    # Add a global legend
    # axs.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=10)
    plt.tight_layout()
    plt.savefig("easy_goal_num_demos.pdf")
    # clear the current figure
    plt.clf()
    plt.close()
    # plot hard Query-based SEER
    fig, axs = plt.subplots(1, 1, figsize=(3, 3), sharex=True, sharey=True)
    # Plotting data into selected subplots
    axs.plot(x, hard_goal_oriented_avg, marker='s', label='Hard', color='#D86C50')
    # axs.plot(x, easy_goal_oriented_avg, marker='s', label='Easy', color='#D86C50')
    # Set labels and grid
    axs.set_xticks(x)
    axs.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs.set_xticklabels(labels)
    # Add a global legend
    # axs.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=10)
    plt.tight_layout()
    plt.savefig("hard_goal_num_demos.pdf")
    # clear the current figure
    plt.clf()
    plt.close()
    # plot together
    fig, axs = plt.subplots(2, 2, figsize=(10, 10), sharex=True)
    # Plotting data into selected subplots
    axs[0, 0].plot(x, easy_goal_oriented_avg, marker='s', label='Easy Query-based SEER', color='#D86C50')
    axs[1, 0].plot(x, easy_proc_oriented_avg, marker='s', label='Easy Traj-based SEER', color='#D86C50')
    axs[0, 1].plot(x, hard_goal_oriented_avg, marker='s', label='Hard Query-based SEER', color='#D86C50')
    axs[1, 1].plot(x, hard_proc_oriented_avg, marker='s', label='Hard Traj-based SEER', color='#D86C50')
    axs[0, 0].set_title("Query-based SEER on Easy", fontsize=20)
    axs[1, 0].set_title("Traj-based SEER on Easy", fontsize=20)
    axs[0, 1].set_title("Query-based SEER on Hard", fontsize=20)
    axs[1, 1].set_title("Traj-based SEER on Hard", fontsize=20)
    axs[0, 0].yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs[1, 0].yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs[0, 1].yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    axs[1, 1].yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    # Set labels and grid
    for ax in axs.flat:
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=20)
        ax.tick_params(axis='y', labelsize=20)
        ax.tick_params(axis='x', labelsize=20)
    plt.tight_layout()
    plt.savefig("all_num_demos.pdf")
    # clear the current figure
    plt.clf()
    plt.close()
def plot_improvement():
    # 数据
    # CoT 28.23529412
    # ReAct 38.62745098
    # TUMS 39.08496732
    # ART 41.37254902
    # ExpeL 45.03267974
    # data = [58, 67, 81, 62, 80, 82, 70, 88, 80, 84]

    # 6组种子数据: goal-oriented
    data1 = [66, 68, 78, 64, 85, 84, 68, 85, 79, 89]
    data2 = [77, 80, 79, 77, 78, 77, 84, 83, 80, 74]
    data3 = [70, 70, 73, 93, 73, 78, 66, 86, 81, 73]
    data4 = [76, 86, 75, 80, 95, 89, 77, 75, 82, 75]
    data5 = [65, 69, 74, 77, 83, 81, 83, 73, 74, 82]
    data6 = [61, 77, 68, 84, 90, 83, 91, 82, 79, 80]
    # 6组种子数据: process-oriented
    # data1 = [63,70,71,62,81,83,74,93,84,87]
    # data2 = [81,75,73,74,82,76,84,76,77,72]
    # data3 = [69,73,80,91,76,78,70,87,76,75]
    # data4 = [79,73,73,71,89,89,73,80,80,73]
    # data5 = [67,71,74,75,86,85,87,77,79,89]
    # data6 = [65,79,72,87,83,78,83,82,76,71]
    
    all_data = np.array([data1, data2, data3, data4, data5, data6])
    all_data_pct = (all_data / 153) * 100
    
    # 计算平均正确率作为 SEER 的表现
    data_mean = np.mean(all_data_pct, axis=0)
    data_std = np.std(all_data_pct, axis=0)
    data_se = data_std / np.sqrt(all_data.shape[0])

    # cot = [28.23529412] * len(data)
    react = [38.62745098] * len(data_mean)
    tums = [39.08496732] * len(data_mean)
    art = [41.37254902] * len(data_mean)
    expel = [45.03267974] * len(data_mean)
    # 计算3点移动平均
    window_size = 3
    smoothed_data = np.convolve(data_mean, np.ones(window_size) / window_size, mode='valid')
    # 创建图表
    plt.figure(figsize=(10, 5))
    # 绘制 SEER 及误差带
    plt.plot(data_mean, marker='o', label='SEER', color='#D86C50', linewidth=2.5)
    plt.fill_between(range(len(data_mean)),
                     data_mean - data_se,
                     data_mean + data_se,
                     color='#D86C50',
                     alpha=0.2,
                     label='SEER ± Std Dev')
    # 绘制平滑后的曲线
    plt.plot(range(window_size - 2, len(data_mean) - 1), smoothed_data, linestyle='--', marker='s',
             label='SEER Smoothed', color='#377eb8', linewidth=2.5)
    # 模型对照线
    plt.plot(expel, marker='v', label='ExpeL', color="#4DAF4A")
    # plt.plot(art, marker='s', label='ART', color="#FFB74D")
    # plt.plot(tums, marker='x', label='TUMS', color='#984EA3')
    # plt.plot(react, marker='o', label='ReAct', color='#6A9FB5')
    # plt.title('Model Performance Over Training Rounds')
    plt.xlabel('Batch Number', fontsize=20)
    plt.ylabel('Accuracy (%)', fontsize=20)
    plt.xticks(range(len(data_mean)), [f"{i+1}" for i in range(len(data_mean))], fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(fontsize=16, loc='lower right')
    plt.tight_layout()
    plt.savefig("improvement-seed-goal.pdf")

if __name__ == "__main__":
    # plot_num_demos()
    plot_improvement()
