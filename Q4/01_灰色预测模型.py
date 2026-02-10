import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def grey_model(x0):

    x1 = np.cumsum(x0)
    
    z1 = (x1[:-1] + x1[1:]) / 2.0
    
    B = np.vstack([-z1, np.ones(len(z1))]).T
    Y = x0[1:].reshape(-1, 1)
    
    [[a], [b]] = np.linalg.inv(B.T @ B) @ B.T @ Y
    
    n = len(x0)
    f = np.zeros(n)
    f[0] = x0[0]
    
    for i in range(1, n):
        f[i] = (x0[0] - b/a) * np.exp(-a*i) + b/a
    
    pred = np.zeros(n)
    pred[0] = f[0]
    for i in range(1, n):
        pred[i] = f[i] - f[i-1]
    
    return pred, a, b

def predict_future(x0, a, b, years):

    n = len(x0)
    future_pred = []
    
    for i in range(n, n + years):
        value = (x0[0] - b/a) * np.exp(-a*i) + b/a
        if i == n:
            pred_value = value - x0[-1]
        else:
            pred_value = value - future_pred[-1]
        future_pred.append(pred_value)
    
    return np.array(future_pred)

def main():

    data = pd.read_csv('../../数据/新能源汽车出口.csv')
    years = data['Year'].values
    exports = data['Export'].values
    
    print("="*50)
    print("灰色预测模型分析")
    print("="*50)
    print(f"数据年份: {years[0]} - {years[-1]}")
    print(f"出口数据: {exports}")
    
    train_years = years[:-2]  # 2011-2021
    train_exports = exports[:-2] 
    
    pred_values, a, b = grey_model(train_exports)
    
    print(f"\n模型参数:")
    print(f"发展系数 a = {a:.6f}")
    print(f"灰色作用量 b = {b:.6f}")
    
    future_years = 2
    future_pred = predict_future(train_exports, a, b, future_years)
    
    print(f"\n预测结果:")
    print(f"2022年预测出口量: {future_pred[0]:.1f}万辆")
    print(f"2023年预测出口量: {future_pred[1]:.1f}万辆")
    print(f"2022年实际出口量: {exports[-2]:.1f}万辆")
    print(f"2023年实际出口量: {exports[-1]:.1f}万辆")
    
    error_2022 = abs(future_pred[0] - exports[-2]) / exports[-2] * 100
    error_2023 = abs(future_pred[1] - exports[-1]) / exports[-1] * 100
    
    print(f"\n预测误差:")
    print(f"2022年误差: {error_2022:.1f}%")
    print(f"2023年误差: {error_2023:.1f}%")
    
    plt.figure(figsize=(12, 6))

    plt.plot(years[:-2], exports[:-2], 'b-o', label='历史数据', linewidth=2, markersize=8)
    plt.plot(years[:-2], pred_values, 'g--s', label='模型拟合', linewidth=2, markersize=6)

    plt.plot([2022, 2023], future_pred, 'r--^', label='灰色预测', linewidth=2, markersize=10)

    plt.plot([2022, 2023], exports[-2:], 'k-D', label='实际出口', linewidth=2, markersize=10)

    plt.axvline(x=2022, color='orange', linestyle='--', alpha=0.5, label='美国IRA法案(2022)')
    plt.axvline(x=2023, color='purple', linestyle='--', alpha=0.5, label='欧盟反补贴调查(2023)')
    
    plt.title('新能源汽车出口量：灰色预测 vs 实际数据', fontsize=14)
    plt.xlabel('年份')
    plt.ylabel('出口量（万辆）')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('../../结果/图表/Q4_灰色预测对比.png', dpi=300)
    plt.show()
    
    result_df = pd.DataFrame({
        '年份': list(years[:-2]) + [2022, 2023],
        '实际出口': list(exports[:-2]) + list(exports[-2:]),
        '预测出口': list(pred_values) + list(future_pred),
        '类型': ['历史']*len(years[:-2]) + ['预测']*2
    })
    
    result_df.to_csv('../../结果/预测结果/出口量预测结果.csv', index=False, encoding='utf-8-sig')

    print("\n" + "="*50)
    print("政策影响分析")
    print("="*50)
    print(f"2022年预测值: {future_pred[0]:.1f}万辆，实际值: {exports[-2]:.1f}万辆")
    print(f"差异: {exports[-2] - future_pred[0]:.1f}万辆")
    print(f"2023年预测值: {future_pred[1]:.1f}万辆，实际值: {exports[-1]:.1f}万辆")
    print(f"差异: {exports[-1] - future_pred[1]:.1f}万辆")
    
    if exports[-1] > future_pred[1]:
        print("\n结论：实际出口量超过预测值，国外政策影响有限")
    else:
        print("\n结论：实际出口量低于预测值，国外政策产生一定影响")

if __name__ == "__main__":
    main()