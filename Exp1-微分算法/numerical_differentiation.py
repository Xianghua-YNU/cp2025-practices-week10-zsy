import numpy as np
import matplotlib.pyplot as plt
from sympy import tanh, symbols, diff, lambdify

def f(x):
    """计算函数值 f(x) = 1 + 0.5*tanh(2x)
    
    参数：
        x: 标量或numpy数组，输入值
    
    返回：
        标量或numpy数组，函数值
    """
    # TODO: 实现函数 f(x) = 1 + 0.5*tanh(2x)
    return 1 + 0.5 * np.tanh(2 * x)

def get_analytical_derivative():
    """使用sympy获取解析导数函数
    
    返回：
        可调用函数，用于计算导数值
    """
    # TODO: 使用sympy计算解析导数并返回可调用的函数
    x = symbols('x')
    f_sym = 1 + 0.5 * tanh(2 * x)
    f_prime_sym = diff(f_sym, x)
    f_prime_func = lambdify(x, f_prime_sym)
    return f_prime_func

def calculate_central_difference(x, f):
    """使用中心差分法计算数值导数
    
    参数：
        x: numpy数组，要计算导数的点
        f: 可调用函数，要求导的函数
    
    返回：
        numpy数组，x[1:-1]处的导数值
    """
    # TODO: 实现中心差分法计算导数
    x = np.asarray(x)  # 将输入转换为numpy数组
    h = 0.1
    df = (f(x + h) - f(x - h)) / (2 * h)
    return df

def richardson_derivative_all_orders(x, f, h, max_order=3):
    """使用Richardson外推法计算不同阶数的导数值
    
    参数：
        x: 标量，要计算导数的点
        f: 可调用函数，要求导的函数
        h: 浮点数，初始步长
        max_order: 整数，最大外推阶数
    
    返回：
        列表，不同阶数计算的导数值
    """
    # TODO: 实现Richardson外推法计算不同阶数的导数值
    x = np.asarray(x)  # 将输入转换为numpy数组
    is_scalar = False
    if x.ndim == 0:  # 检查是否为标量
        x = np.array([x])
        is_scalar = True
    
    n = len(x)
    d = np.zeros((max_order + 1, n), float)
    for i in range(max_order + 1):
        di = (f(x + h) - f(x - h)) / (2 * h)
        if i > 0:
            di = (4 ** i * d[i - 1] - d[i - 1]) / (4 ** i - 1)
        d[i] = di
        h *= 0.5  # 每层外推步长减半
    
    if is_scalar:  # 如果输入是标量，返回一维数组
        return d[:, 0]
    return d

def create_comparison_plot(x, x_central, dy_central, dy_richardson, df_analytical):
    """创建对比图，展示导数计算结果和误差分析
    
    参数：
        x: numpy数组，所有x坐标点
        x_central: numpy数组，中心差分法使用的x坐标点
        dy_central: numpy数组，中心差分法计算的导数值
        dy_richardson: numpy数组，Richardson方法计算的导数值
        df_analytical: 可调用函数，解析导数函数
    """
    # 创建四个子图
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))
    plt.tight_layout()
    # TODO: 实现四个子图的绘制：
    # 1. 导数对比图
    ax1.plot(x, dy_central, label='Central Difference')
    ax1.plot(x, dy_richardson[0], label='Richardson (Order 0)')
    ax1.plot(x, df_analytical(x), label='Analytical', linestyle='--')
    ax1.set_title('Derivative Comparison')
    ax1.set_xlabel('x')
    ax1.set_ylabel("f'(x)")
    ax1.legend()
    # 2. 误差分析图（对数坐标）
    ax2.loglog(x, np.abs(dy_central - df_analytical(x)), label='Central Difference')
    ax2.loglog(x, np.abs(dy_richardson[0] - df_analytical(x)), label='Richardson (Order 0)')
    ax2.set_title('Error Analysis')
    ax2.set_xlabel('x')
    ax2.set_ylabel('Error')
    ax2.legend()
    # 3. Richardson外推不同阶数误差对比图（对数坐标）
    for i in range(dy_richardson.shape[0]):
        ax3.loglog(x, np.abs(dy_richardson[i] - df_analytical(x)), label=f'Order {i}')
    ax3.set_title('Richardson Extrapolation Error')
    ax3.set_xlabel('x')
    ax3.set_ylabel('Error')
    ax3.legend()
    # 4. 步长敏感性分析图（双对数坐标）
    h_values = np.array([0.1, 0.01, 0.001, 1e-4, 1e-5, 1e-6])
    mean_errors = []
    for h in h_values:
        dy_rich = richardson_derivative_all_orders(x, f, h, max_order=3)
        mean_errors.append(np.mean(np.abs(dy_rich - df_analytical(x).reshape(1, -1)), axis=1))
    mean_errors = np.array(mean_errors)
    for i in range(dy_rich.shape[0]):
        ax4.loglog(h_values, mean_errors[:, i], marker='o', label=f'Order {i}')
    ax4.set_title('Step Size Sensitivity')
    ax4.set_xlabel('Step Size (h)')
    ax4.set_ylabel('Mean Error')
    ax4.legend()
    ax4.grid(True)
    plt.show()

    plt.savefig('derivative_comparison.png')

def main():
    """运行数值微分实验的主函数"""
    # TODO: 设置实验参数
    x = np.linspace(-2, 2, 100)
    h = 0.1
    max_order = 3
    # TODO: 获取解析导数函数
    df_analytical = get_analytical_derivative()
    # TODO: 计算中心差分导数
    dy_central = calculate_central_difference(x, f, h)
    # TODO: 计算Richardson外推导数
    dy_richardson = richardson_derivative_all_orders(x, f, h, max_order)
    # TODO: 绘制结果对比图
    create_comparison_plot(x, x, dy_central, dy_richardson, df_analytical)

    plt.savefig('derivative_comparison.png')

if __name__ == '__main__':
    main()
