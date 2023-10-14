import numpy as np
def numerical_gradient(f, x):
    h = 1e-4  # 0.0001
    grad = np.zeros_like(x)  # x와 형상이 같은 배열을 생성

    # The partial differential of function f with respect to x_idx
    for idx in range(x.size):
        tmp_val = x[idx]

        # f(x+h)
        x[idx] = tmp_val + h
        f_x_plus_h = f(x)

        # f(x)
        x[idx] = tmp_val
        fx = f(x)

        grad[idx] = (f_x_plus_h - fx) / h
        x[idx] = tmp_val

    return grad

# 목적 함수
def function_3(x):
    return (x[0]-2)**2 + (x[1]-5)**2

x_k = np.array([-3.0, 10.0])                  # initial point
eta = 0.01                                    # step size, learning rate, momentum

for k in range(1000):
  g_k = numerical_gradient(function_3, x_k)   # 목적험수를 이용하여 미분 식을 만들 수 있다.
  partial_x_k = -g_k                          # step 2
  x_k = x_k + eta * partial_x_k               # step 3
print(x_k)


def gradient_descent(f, x_0, eta=0.01, max_iter=100):
    x_k = x_0

    for k in range(max_iter):
        g_k = numerical_gradient(f, x_k)
        partial_x_k = -g_k
        x_k = x_k + eta * partial_x_k  # update variable

    return x_k


x_0 = np.array([-3.0, 4.0])
x_opt = gradient_descent(function_3, x_0=x_0, eta=0.005, max_iter=1000)
print(x_opt)