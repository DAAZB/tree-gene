import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import main


def plot_gantt(gantt_data: dict):
    colors = ['#FF00FF', '#BD7AFF', '#0080FF', '#00FFFF', '#00FF80', '#FFFF00', '#FF8000', '#FF0000'] #配色方案
    plt.figure(figsize = (8,4), dpi = 200).subplots_adjust(right=0.8) #画布大小和分辨率
    for key in gantt_data: #循环绘制方块
        data = gantt_data[key]
        for time_set in data:
            plt.barh(time_set[0], time_set[2]-time_set[1], 1, left=time_set[1], color = colors[key], edgecolor = 'white', lw = 0.2)
    labels = ['job' + str(i) for i in range(main.job_number)]
    patches = [mpatches.Patch(color=colors[i], label = '{:s}'.format(labels[i])) for i in range(main.job_number)]
    plt.legend(handles = patches, loc = 3, bbox_to_anchor = (1.05, 0), borderaxespad = 0) #添加图例
    plt.grid(axis ='x', ls = '--', lw = 0.5) #添加网格
    ylabels = [i for i in range(main.machine_number)]
    plt.yticks(ylabels) #y轴标签
    plt.title('GANTT')
    plt.xlabel('Time')
    plt.ylabel('Machine')
    plt.show()


if __name__ == '__main__':
    gantt_data = {0: [[5, 0, 2], [5, 2, 9], [3, 8, 17], [3, 21, 30]], 1: [[3, 17, 21], [3, 31, 32], [2, 7, 8], [4, 23, 26]], 2: [[2, 0, 4], [5, 27, 28], [4, 12, 16], [3, 32, 34]], 3: [[3, 30, 31], [1, 8, 9], [2, 9, 12], [4, 16, 20]], 4: [[0, 0, 5], [3, 5, 6], [5, 22, 27], [0, 21, 25]], 5: [[4, 0, 2], [4, 6, 8], [5, 17, 22], [2, 34, 39]], 6: [[2, 5, 7], [2, 20, 23], [2, 26, 28], [5, 42, 46]], 7: [[2, 4, 5], [0, 30, 33], [3, 39, 41], [4, 41, 42]]}
    plot_gantt(gantt_data)