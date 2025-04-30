import numpy as np
import matplotlib.pyplot as plt

def q3a(T):
    """
    计算 3-alpha 反应速率中与温度相关的部分 q / (rho^2 Y^3)
    输入: T - 温度 (K)
    返回: 速率因子 (erg * cm^6 / (g^3 * s))
    """
    # TODO: 在此实现3-α反应速率计算
    # 提示：
    # 1. 将温度转换为以 10^8 K 为单位
    # 2. 注意处理温度为零的特殊情况
    # 3. 使用公式：q_{3α} = 5.09×10^11 ρ^2 Y^3 T_8^(-3) exp(-44.027/T_8)
    if T <= 0:
        return 0.0
    
    # 将温度转换为以 1e8 K 为单位的温度
    T8 = T / 1e8
    
    # 使用公式计算 q3a
    return 5.09e-11 * T8**3 * np.exp(-44.027 / T8)

def plot_rate(filename="rate_vs_temp.png"):
    """绘制速率因子随温度变化的 log-log 图"""
    # TODO: 在此实现绘图函数
    # 提示：
    # 1. 使用 np.logspace 生成温度数据点
    # 2. 计算对应的速率值
    # 3. 使用 plt.loglog 绘制双对数图
    # 4. 添加适当的标签和标题
    temps = np.logspace(8, 10, 200)  # 从1e8 K到1e10 K生成200个点
    
    # 计算对应的速率值
    rates = [q3a(T) for T in temps]
    
    # 使用 plt.loglog 绘制双对数图
    plt.figure(figsize=(10, 6))
    plt.loglog(temps, rates, label='3-alpha反应速率')
    
    # 添加适当的标签和标题
    plt.xlabel(' T (K)')
    plt.ylabel('Rate factor q / (rho^2 Y^3) (erg cm^6 / (g^3 s))')
    plt.title('3-alpha the relationship between reaction rate and temperature')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    # 计算并打印 nu 值
    print("   温度 T (K)    :   ν (敏感性指数)")
    print("--------------------------------------")

    temperatures_K = [1.0e8, 2.5e8, 5.0e8, 1.0e9, 2.5e9, 5.0e9]
    h = 1.0e-8  # 扰动因子

    # TODO: 实现温度敏感性指数的计算
    # 提示：
    # 1. 对每个温度点计算 q3a
    # 2. 使用前向差分计算导数
    # 3. 计算敏感性指数 nu
    # 4. 注意处理特殊情况（如 q = 0）

    # TODO: 调用绘图函数展示结果
    for T0 in temperatures_K:
        # 计算 q3a 在 T0 处的值
        q0 = q3a(T0)
        
        # 计算 T0 + h*T0 处的 q3a 值
        q_plus = q3a(T0 + h*T0)
        
        # 计算导数 dq/dT 的近似值
        dq_dT = (q_plus - q0) / (h*T0)
        
        # 计算温度敏感性指数 nu
        if q0 == 0:
            nu = 0
        else:
            nu = T0 * dq_dT / q0
        
        # 打印结果
        print(f"{T0:.1e}   :   {nu:.3f}")
    
    # 调用绘图函数展示结果
    plot_rate()
