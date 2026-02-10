import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def run_regression():
  
    data = pd.read_csv('../../数据/newenerge.csv')
    
    print("="*50)
    print("多元线性回归分析")
    print("="*50)
    
    model = ols("Y ~ X1 + X2 + X3 + X4 + X5", data=data).fit()
    
    print(model.summary())

    anova_results = anova_lm(model, typ=1)
    print("\n方差分析表:")
    print(anova_results)
  
    coefficients = model.params
    print("\n回归系数:")
    for name, value in coefficients.items():
        print(f"{name}: {value:.4f}")

    results = pd.DataFrame({
        '变量': list(coefficients.index),
        '系数': coefficients.values,
        '标准误': model.bse.values,
        't值': model.tvalues.values,
        'p值': model.pvalues.values
    })
    
    results.to_csv('../../结果/预测结果/回归分析结果.csv', index=False, encoding='utf-8-sig')
    print("\n结果已保存！")
    
    return model

def model_diagnosis(model, data):

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    residuals = model.resid
    fitted = model.fittedvalues

    axes[0, 0].scatter(fitted, residuals, alpha=0.6)
    axes[0, 0].axhline(y=0, color='r', linestyle='--')
    axes[0, 0].set_title('残差图')

    from scipy import stats
    stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title('Q-Q图')

    axes[1, 0].hist(residuals, bins=15, edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('残差分布')
    
    axes[1, 1].scatter(data['Y'], fitted, alpha=0.6)
    min_val = min(data['Y'].min(), fitted.min())
    max_val = max(data['Y'].max(), fitted.max())
    axes[1, 1].plot([min_val, max_val], [min_val, max_val], 'r--')
    axes[1, 1].set_title('实际值 vs 预测值')
    
    plt.tight_layout()
    plt.savefig('../../结果/图表/Q1_模型诊断.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    data = pd.read_csv('../../数据/newenerge.csv')
    model = run_regression()
    model_diagnosis(model, data)