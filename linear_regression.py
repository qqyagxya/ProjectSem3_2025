import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. 读取数据并准备特征（用“时间索引”作为X，湿度作为y）
input_csv = "/home/pi/normalized_data.csv"
df = pd.read_csv(input_csv)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["time_index"] = np.arange(len(df))  # 用时间索引（0,1,2...）作为特征X

# 2. 划分训练集和测试集（用前80%数据训练，后20%测试）
train_size = int(0.8 * len(df))
X = df[["time_index"]].values  # 特征：时间索引
y = df["normalized_humidity"].values  # 目标：归一化湿度

X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 3. 训练线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)

# 4. 预测（测试集+12小时预测，12小时=24次采集，因为每30分钟一次）
y_pred_test = model.predict(X_test)  # 测试集预测
# 12小时预测：生成未来24个时间索引
future_time_index = np.arange(len(df), len(df) + 24).reshape(-1, 1)
y_pred_future = model.predict(future_time_index)  # 未来12小时预测

# 5. 模型评估（计算误差）
mse = mean_squared_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)
print(f"线性回归模型评估：")
print(f"均方误差（MSE）：{mse:.4f}（越小越好）")
print(f"决定系数（R²）：{r2:.4f}（越接近1越好）")

# 6. 可视化结果
plt.figure(figsize=(14, 7))
# 绘制训练集、测试集、预测值
plt.plot(df["time_index"], df["normalized_humidity"], label="实际湿度", color="blue")
plt.plot(X_test, y_pred_test, label="测试集预测", color="red", linestyle="--")
plt.plot(future_time_index, y_pred_future, label="12小时预测", color="green", linestyle=":")
# 标注训练集和测试集分界线
plt.axvline(x=train_size, color="gray", linestyle="-.", label="训练/测试分界")
plt.xlabel("时间索引")
plt.ylabel("归一化湿度（0-1）")
plt.title("线性回归模型：实际湿度vs预测湿度（含12小时预测）")
plt.legend()
plt.grid(True)
plt.savefig("/home/pi/linear_regression_plot.png")
plt.close()
print("线性回归结果图已保存：/home/pi/linear_regression_plot.png")
