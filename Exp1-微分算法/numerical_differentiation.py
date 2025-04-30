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
    f_prime_func = lambdify(x, f_prime_sym, 'numpy')
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
    dy = []
    for i in range(1, len(x)-1):
        h = x[i+1] - x[i]
        dy.append((f(x[i+1]) - f(x[i-1])) / (2 * h))
    return np.array(dy)

def richardson_derivative_all_orders(x, f, h=0.1, max_order=3):
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
    R = np.zeros((max_order + 1, max_order + 1))
    
    for i in range(max_order + 1):
        hi = h / (2**i)
        R[i, 0] = (f(x + hi) - f(x - hi)) / (2 * hi)
    
    # Richardson外推
    for j in range(1, max_order + 1):
        for i in range(max_order - j + 1):
            R[i, j] = (4**j * R[i+1, j-1] - R[i, j-1]) / (4**j - 1)
    
    return [R[0, j] for j in range(1, max_order + 1)]
    
    
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
    ax1.plot(x_central, dy_central, label='Central Difference')
    ax1.plot(x, dy_richardson[0], label='Richardson (Order 1)')  # 使用第1阶Richardson方法
    ax1.plot(x, df_analytical(x), label='Analytical', linestyle='--')
    ax1.set_title('Derivative Comparison')
    ax1.set_xlabel('x')
    ax1.set_ylabel("f'(x)")
    ax1.legend()
    # 2. 误差分析图（对数坐标）
    error_central = np.abs(dy_central - df_analytical(x_central))
    error_richardson = np.abs(dy_richardson[0] - df_analytical(x))
    ax2.plot(x_central, error_central, 'ro', markersize=4, label='Central Difference Error')
    ax2.plot(x, error_richardson, 'g-', markersize=4, label='Richardson Error')
    ax2.set_yscale('log')
    ax2.set_title('Error Analysis')
    ax2.set_xlabel('x')
    ax2.set_ylabel('Absolute Error (log scale)')
    ax2.legend()
    ax2.grid(True)
    # 3. Richardson外推不同阶数误差对比图（对数坐标）
    for i, order in enumerate(['1st', '2nd', '3rd']):
        error = np.abs(dy_richardson[i] - df_analytical(x))
        ax3.plot(x, error, marker='^', markersize=4, label=f'Richardson {order}')
    ax3.set_yscale('log')
    ax3.set_title('Richardson Extrapolation Error Comparison')
    ax3.set_xlabel('x')
    ax3.set_ylabel('Absolute Error (log scale)')
    ax3.legend()
    ax3.grid(True)

    # 4. 步长敏感性分析图（双对数坐标）
    h_values = np.logspace(-6, -1, 20)
    x_test = 0.0
    central_errors = []
    richardson_errors = []
    expected = df_analytical(x_test)

    for h in h_values:
        # 中心差分误差
        central_result = (f(x_test + h) - f(x_test - h)) / (2 * h)
        central_errors.append(abs(central_result - expected))

        # Richardson外推误差（2阶）
        rich_result = richardson_derivative_all_orders(x_test, f, h, max_order=3)[1]
        richardson_errors.append(abs(rich_result - expected))

    ax4.loglog(h_values, central_errors, 'ro-', label='Central Difference')
    ax4.loglog(h_values, richardson_errors, 'g-', label='Richardson (2nd Order)')
    ax4.set_title('Step Size Sensitivity Analysis')
    ax4.set_xlabel('Step Size h (log scale)')
    ax4.set_ylabel('Absolute Error (log scale)')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    plt.show()
    plt.savefig('derivative_comparison.png')
    

def main():
    """运行数值微分实验的主函数"""
    # TODO: 设置实验参数
    x = np.linspace(-6, -1, 20)
    h = 0.1
    max_order = 3
    
    # TODO: 获取解析导数函数
    df_analytical = get_analytical_derivative()
    # TODO: 计算中心差分导数
    dy_central = calculate_central_difference(x, f)
    x_central = x[1:-1]
    # TODO: 计算Richardson外推导数
    dy_richardson = np.array([
        richardson_derivative_all_orders(xi, f, h_initial, max_order=max_order)
        for xi in x
    ])
    
    create_comparison_plot(x, x, dy_central, dy_richardson, df_analytical)
    plt.savefig('derivative_comparison.png')

if __name__ == '__main__':
    main()
