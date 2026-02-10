import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def calculate_carbon_emissions():

    national_data = {
        '总人口': 141175,  
        '传统燃油车': 31179,  
        '新能源汽车': 1621,   
        '纯电动车占比': 0.7,   
        '混动车占比': 0.3      
    }

    emission_factors = {
        '燃油车': 55,    
        '纯电动车': 39,   
        '混动车': 47     
    }
    

    city_population = 100  
    scale_factor = city_population / national_data['总人口']
    
    city_vehicles = {
        '燃油车': national_data['传统燃油车'] * scale_factor,
        '纯电动车': national_data['新能源汽车'] * national_data['纯电动车占比'] * scale_factor,
        '混动车': national_data['新能源汽车'] * national_data['混动车占比'] * scale_factor
    }
    
    print("="*50)
    print(f"百万人口城市车辆分布（单位：辆）")
    print("="*50)
    for vehicle_type, count in city_vehicles.items():
        print(f"{vehicle_type}: {count:,.0f}辆")
    

    emissions_before = {
        '燃油车': city_vehicles['燃油车'] * emission_factors['燃油车'],
        '纯电动车': city_vehicles['纯电动车'] * emission_factors['纯电动车'],
        '混动车': city_vehicles['混动车'] * emission_factors['混动车']
    }
    
    total_before = sum(emissions_before.values())
    

    conversion_rate = 0.8
    
    city_vehicles_after = {
        '燃油车': city_vehicles['燃油车'] * (1 - conversion_rate),
        '纯电动车': (city_vehicles['纯电动车'] + 
                   city_vehicles['燃油车'] * conversion_rate * 0.8),
        '混动车': (city_vehicles['混动车'] + 
                  city_vehicles['燃油车'] * conversion_rate * 0.2)
    }
    
    emissions_after = {
        '燃油车': city_vehicles_after['燃油车'] * emission_factors['燃油车'],
        '纯电动车': city_vehicles_after['纯电动车'] * emission_factors['纯电动车'],
        '混动车': city_vehicles_after['混动车'] * emission_factors['混动车']
    }
    
    total_after = sum(emissions_after.values())
    

    reduction = total_before - total_after
    reduction_rate = reduction / total_before * 100
    
    return {
        'city_vehicles': city_vehicles,
        'city_vehicles_after': city_vehicles_after,
        'emissions_before': emissions_before,
        'emissions_after': emissions_after,
        'total_before': total_before,
        'total_after': total_after,
        'reduction': reduction,
        'reduction_rate': reduction_rate
    }

def visualize_results(results):

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    categories = ['燃油车', '纯电动车', '混动车']
    before = [results['city_vehicles'][cat] for cat in categories]
    after = [results['city_vehicles_after'][cat] for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    axes[0].bar(x - width/2, before, width, label='电动化前', alpha=0.8, color='#FF6B6B')
    axes[0].bar(x + width/2, after, width, label='电动化后', alpha=0.8, color='#4ECDC4')
    axes[0].set_xlabel('车辆类型')
    axes[0].set_ylabel('车辆数量（辆）')
    axes[0].set_title('电动化前后车辆分布对比')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(categories)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # 2. 碳排放对比
    em_before = [results['emissions_before'][cat]/10000 for cat in categories]
    em_after = [results['emissions_after'][cat]/10000 for cat in categories]
    
    axes[1].bar(x - width/2, em_before, width, label='电动化前', alpha=0.8, color='#FF6B6B')
    axes[1].bar(x + width/2, em_after, width, label='电动化后', alpha=0.8, color='#4ECDC4')
    axes[1].set_xlabel('车辆类型')
    axes[1].set_ylabel('碳排放（万吨CO2e）')
    axes[1].set_title('电动化前后碳排放对比')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(categories)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')
    
    totals = [results['total_before']/10000, results['total_after']/10000]
    reduction = results['reduction']/10000
    
    bars = axes[2].bar(['电动化前', '电动化后'], totals, color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
    axes[2].set_ylabel('总碳排放（万吨CO2e）')
    axes[2].set_title(f'总碳排放减少: {reduction:.1f}万吨 ({results["reduction_rate"]:.1f}%)')
    axes[2].grid(True, alpha=0.3, axis='y')
 
    for bar, value in zip(bars, totals):
        height = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2, height + 5,
                    f'{value:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('../../结果/图表/Q5_碳减排效果.png', dpi=300)
    plt.show()

def generate_report(results):

    print("\n" + "="*50)
    print("碳排放分析报告")
    print("="*50)
    
    print(f"\n1. 车辆分布（电动化前）:")
    for vehicle_type, count in results['city_vehicles'].items():
        print(f"   {vehicle_type}: {count:,.0f}辆")
    
    print(f"\n2. 车辆分布（电动化后，80%燃油车转换）:")
    for vehicle_type, count in results['city_vehicles_after'].items():
        print(f"   {vehicle_type}: {count:,.0f}辆")
    
    print(f"\n3. 碳排放量（全生命周期）:")
    print(f"   电动化前总排放: {results['total_before']:,.1f} 吨CO2e")
    print(f"   电动化后总排放: {results['total_after']:,.1f} 吨CO2e")
    print(f"   减排量: {results['reduction']:,.1f} 吨CO2e")
    print(f"   减排比例: {results['reduction_rate']:.1f}%")

    report_data = {
        '指标': ['总人口(万人)', '电动化前总排放(吨)', '电动化后总排放(吨)', 
                '减排量(吨)', '减排比例(%)'],
        '数值': [100, results['total_before'], results['total_after'],
                results['reduction'], results['reduction_rate']]
    }
    
    df_report = pd.DataFrame(report_data)
    df_report.to_csv('../../结果/预测结果/碳排放分析报告.csv', index=False, encoding='utf-8-sig')
    print(f"\n分析报告已保存！")

def main():

    print("APMCM2023 C题 - 第五问：城市电动化环境效益分析")
    print("假设城市人口: 100万")
    print("="*50)

    results = calculate_carbon_emissions()

    visualize_results(results)

    generate_report(results)

if __name__ == "__main__":
    main()