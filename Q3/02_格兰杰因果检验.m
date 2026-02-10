% 第三问：格兰杰因果检验
clc, clear;

% 读取数据
y1 = readmatrix('全球新能源汽车销售量.xlsx');
y2 = readmatrix('全球油价销售量.xlsx');

data = [y1', y2'];
sigma = cov(data);
mu_y1 = mean(y1);
mu_y2 = mean(y2);

p = 1;
F = zeros(p, p);
f = zeros(p, 1);

for k = 1:p
    for j = 1:p
        if k > j
            continue;
        else
            F(k, j) = sigma(1, 1) / sigma(1, 1+j-k);
            f(k) = f(k) + F(k, j);
        end
    end
end

disp(['f = ', num2str(f)]);
if f > 1
    disp('y2 granger causes y1');
else
    disp('y1 granger causes y2');
end