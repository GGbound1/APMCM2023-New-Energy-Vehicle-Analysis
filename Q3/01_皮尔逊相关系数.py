第三问：皮尔逊相关系数分析
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def pearson_correlation():

    years = np.arange(2013, 2023)
 
    new_energy_sales = np.array([1.8, 7.5, 33.1, 50.7, 77.7, 125.6, 120.6, 136.7, 352.1, 688.7])
  
    oil_prices = np.array([108.4, 99.0, 52.4, 43.7, 54.2, 71.3, 64.0, 41.8, 70.9, 99.0])
 
    trad_rd = np.array([450, 460, 470, 480, 490, 500, 510, 520, 530, 540])
    
    trad_sales = np.array([85.0, 86.5, 88.0, 89.5, 90.0, 88.5, 87.0, 85.5, 84.0, 82.5])

    data = pd.DataFrame({
        'Year': years,
        'New_Energy_Sales': new_energy_sales,
        'Oil_Price': oil_prices,
        'Traditional_RD': trad_rd,
        'Traditional_Sales': trad_sales
    })
    
    corr_matrix = data[['New_Energy_Sales', 'Oil_Price', 'Traditional_RD', 'Traditional_Sales']].corr()
    
    print("="*50)
    print("皮尔逊相关系数矩阵")
    print("="*50)
    print(corr_matrix)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.3f', linewidths=1)
    plt.title('变量间皮尔逊相关系数热图', fontsize=14)
    plt.tight_layout()
    plt.savefig('../../结果/图表/Q3_相关系数热图.png', dpi=300)
    plt.show()
    
    corr_matrix.to_csv('../../结果/预测结果/相关系数矩阵.csv', encoding='utf-8-sig')
    
    print("\n关键发现:")
    print(f"1. 新能源汽车销量 vs 油价: {corr_matrix.loc['New_Energy_Sales', 'Oil_Price']:.3f}")
    print(f"2. 新能源汽车销量 vs 传统车销量: {corr_matrix.loc['New_Energy_Sales', 'Traditional_Sales']:.3f}")
    print(f"3. 油价 vs 传统车销量: {corr_matrix.loc['Oil_Price', 'Traditional_Sales']:.3f}")

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].plot(years, new_energy_sales, 'g-o', linewidth=2)
    axes[0, 0].set_title('新能源汽车全球销量')
    axes[0, 0].set_ylabel('销量（万辆）')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(years, oil_prices, 'r-s', linewidth=2)
    axes[0, 1].set_title('全球油价')
    axes[0, 1].set_ylabel('美元/桶')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].plot(years, trad_rd, 'b-^', linewidth=2)
    axes[1, 0].set_title('传统能源研发投入')
    axes[1, 0].set_ylabel('亿美元')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(years, trad_sales, 'm-D', linewidth=2)
    axes[1, 1].set_title('传统能源车销量')
    axes[1, 1].set_ylabel('百万辆')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../结果/图表/Q3_变量趋势图.png', dpi=300)
    plt.show()
    
    return data

if __name__ == "__main__":
    data = pearson_correlation()