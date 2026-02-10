import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def load_and_visualize():

    data = pd.read_csv('../../数据/newenerge.csv')
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].bar(data['Year'], data['Y'], alpha=0.6, color='skyblue')
    axes[0, 0].plot(data['Year'], data['Y'], 'r-o', linewidth=2)
    axes[0, 0].set_title('新能源汽车销量趋势')
    axes[0, 0].set_xlabel('年份')
    axes[0, 0].set_ylabel('销量（万辆）')
    axes[0, 0].grid(True, alpha=0.3)
    
    factors = [('X1', '充电桩数量'), ('X2', '电池装机量'), ('X3', '产业链投资'),
               ('X4', '碳排放'), ('X5', '人均GNI')]
    
    for idx, (col, title) in enumerate(factors, 1):
        row, col_idx = divmod(idx, 3)
        axes[row, col_idx].plot(data['Year'], data[col], 'g-s', linewidth=2)
        axes[row, col_idx].set_title(title)
        axes[row, col_idx].set_xlabel('年份')
        axes[row, col_idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../结果/图表/Q1_各因素趋势.png', dpi=300)
    plt.show()
    
    print("数据可视化完成！")

if __name__ == "__main__":
    load_and_visualize()