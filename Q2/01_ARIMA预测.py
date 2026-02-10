import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def load_data():

    data = pd.read_csv('../../数据/新能源汽车销量_月度.csv')
    data['时间'] = pd.to_datetime(data['时间'])
    data.set_index('时间', inplace=True)
    return data['新能源汽车销量']

def check_stationarity(series):

    result = adfuller(series.dropna())
    print('ADF统计量:', result[0])
    print('p值:', result[1])
    print('临界值:')
    for key, value in result[4].items():
        print(f'\t{key}: {value:.3f}')
    return result[1] < 0.05

def arima_forecast(series, steps=120):

    print("平稳性检验:")
    is_stationary = check_stationarity(series)
    
    if not is_stationary:
        print("序列非平稳，进行差分")
        series_diff = series.diff().dropna()
    else:
        series_diff = series
    

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    plot_acf(series_diff, ax=axes[0])
    plot_pacf(series_diff, ax=axes[1])
    plt.tight_layout()
    plt.show()
    
    model = ARIMA(series, order=(2,1,2))
    model_fit = model.fit()
    
    print("\n模型摘要:")
    print(model_fit.summary())
    
    forecast = model_fit.forecast(steps=steps)
    
    last_date = series.index[-1]
    future_dates = pd.date_range(start=last_date, periods=steps+1, freq='M')[1:]
    
    plt.figure(figsize=(12, 6))
    plt.plot(series.index, series, 'b-', label='历史数据', linewidth=2)
    plt.plot(future_dates, forecast, 'r--', label='预测值', linewidth=2)
    plt.fill_between(future_dates, 
                     forecast * 0.9, 
                     forecast * 1.1, 
                     alpha=0.2, color='red', label='置信区间')
    
    plt.title('新能源汽车销量预测（未来10年）', fontsize=14)
    plt.xlabel('时间')
    plt.ylabel('销量（万辆）')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('../../结果/图表/Q2_销量预测.png', dpi=300)
    plt.show()
    
    forecast_df = pd.DataFrame({
        '时间': future_dates,
        '预测销量': forecast.values
    })
    forecast_df.to_csv('../../结果/预测结果/未来10年销量预测.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n未来10年月度预测已保存")
    print(f"2023年预测年销量: {forecast[:12].sum():.1f}万辆")
    print(f"2028年预测年销量: {forecast[60:72].sum():.1f}万辆")
    
    return forecast

if __name__ == "__main__":
    series = load_data()
    forecast = arima_forecast(series)