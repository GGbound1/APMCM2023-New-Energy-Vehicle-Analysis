% 第二问：ARIMA预测
clear; clc

% 加载数据
DD = readmatrix("现有数据.xlsx");
P = DD(1:35, 2);
N = length(P);
n = 20;

F = P(1:n+2);
Yt = [0, diff(P, 1)];
L = diff(P, 2);
Y = L(1:n);

a = length(L) - length(Y);
aa = a;
Ux = sum(Y) / n;

yt = Y - Ux;
b = 0;

for i = 1:n
    b = yt(i)^2 / n + b;
end

v = sqrt(b);
Y = zscore(Y);
f = F(1:n);
t = 1:n;

% 自相关计算
R0 = 0;
for i = 1:n
    R0 = Y(i)^2 / n + R0;
end

for k = 1:20
    R(k) = 0;
    for i = k+1:n
        R(k) = Y(i) * Y(i-k) / n + R(k);
    end
end

x = R / R0;
X1 = x(1);
xx(1,1) = 1;
X(1,1) = x(1);
B(1,1) = x(1);
K = 0;
T = X1;

for t = 2:n
    at = Y(t) - T(1) * Y(t-1);
    K = at^2 + K;
end

U(1) = K / (n-1);

for i = 1:19
    B(i+1,1) = x(i+1);
    xx(1,i+1) = x(i);
    A = toeplitz(xx);
    XX = A \ B;
    XXX = XX(i+1);
    X(1,i+1) = XX;
    K = 0;
    T = XX;
    
    for t = i+2:n
        r = 0;
        for j = 1:i+1
            r = T(j) * Y(t-j) + r;
        end
        at = Y(t) - r;
        K = at^2 + K;
    end
    U(i+1) = K / (n - i + 1);
end

% 预测
q = 2;  % AR阶数
W = X(:, q);  % AR系数

% 单步预测
Z1 = zeros(a, 1);
for i = 1:a
    r = 0;
    for j = 1:q
        r = W(j) * Y(n+i-j) + r;
    end
    Z1(i) = r;
end

r1 = Z1 * v + Ux;
r1(1) = Yt(n+2) + r1(1);
z1(1) = P(n+2) + r1(1);

for i = 2:a
    r1(i) = r1(i-1) + r1(i);
    z1(i) = z1(i-1) + r1(i);
end

% 计算误差
D_a = P(n+2:end-1);
for i = 1:a
    e6_a(i) = D_a(i) - z1(i);
    PE6_a(i) = (e6_a(i) / D_a(i)) * 100;
end

mae6_a = sum(abs(e6_a)) / 10;
MAPE6_a = sum(abs(PE6_a)) / 10;

% 绘图
figure;
plot(1:a, D_a, '-+');
hold on;
plot(z1, 'r-*');
title('单步预测值和实际值对比图');
legend("真实值", "预测值", "Location", "best");
hold off;

% 多步预测
Z = zeros(aa, 1);
Xt = zeros(1, q);

for i = 1:q
    Xt(1,i) = Y(n-q+i);
end

Z(1) = 0;
for i = 1:q
    Z(1) = W(i) * Xt(q-i+1) + Z(1);
end

for l = 2:q
    K = 0;
    for i = 1:l-1
        K = W(i) * Z(l-i) + K;
    end
    G = 0;
    for j = l:q
        G = W(j) * Xt(q+l-j) + G;
    end
    Z(l) = K + G;
end

for l = q+1:aa
    K = 0;
    for i = 1:q
        K = W(i) * Z(l-i) + K;
    end
    Z(l) = K;
end

r = Z * v + Ux;
r(1) = Yt(n+2) + r(1);
z(1) = P(n+2) + r(1);

for i = 2:aa
    r(i) = r(i-1) + r(i);
    z(i) = z(i-1) + r(i);
end

D = P(n+2:end-1);
for i = 1:aa
    e6(i) = D(i) - z(i);
    PE6(i) = (e6(i) / D(i)) * 100;
end

mae6 = sum(abs(e6)) / 10;
MAPE6 = sum(abs(PE6)) / 10;

% 绘制多步预测图
figure;
plot(1:aa, D, '-+');
hold on;
plot(z, 'r-*');
title('多步预测值和实际值对比图');
legend("真实值", "预测值", "Location", "best");
hold off;

disp(['单步预测MAE: ', num2str(mae6_a)]);
disp(['单步预测MAPE: ', num2str(MAPE6_a), '%']);
disp(['多步预测MAE: ', num2str(mae6)]);
disp(['多步预测MAPE: ', num2str(MAPE6), '%']);