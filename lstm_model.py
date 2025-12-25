import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 1. 读取数据并准备（用归一化后的湿度数据）
input_csv = "/home/pi/normalized_data.csv"
df = pd.read_csv(input_csv)
data = df["normalized_humidity"].values.reshape(-1, 1)  # 转换为2D数组

# 2. 准备LSTM输入数据（时间步长=10，即用前10个数据预测第11个）
def create_dataset(dataset, time_step=10):
    X, y = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]
        X.append(a)
        y.append(dataset[i+time_step, 0])
    return np.array(X), np.array(y)

time_step = 10
X, y = create_dataset(data, time_step)
# 转换为LSTM需要的格式：[样本数, 时间步长, 特征数]
X = X.reshape(X.shape[0], X.shape[1], 1)

# 3. 划分训练集和测试集（前80%训练）
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 4. 构建LSTM模型（轻量级，避免过拟合）
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))  # 第一层LSTM
model.add(LSTM(50, return_sequences=False))  # 第二层LSTM
model.add(Dense(25))  # 全连接层
model.add(Dense(1))   # 输出层（预测1个值）
model.compile(optimizer="adam", loss="mean_squared_error")  # 编译模型

# 5. 训练模型（ epochs=50，训练50轮，足够收敛）
model.fit(X_train, y_train, batch_size=64, epochs=50, validation_data=(X_test, y_test))

# 6. 预测（测试集+未来周期预测）
y_pred_test = model.predict(X_test)  # 测试集预测
# 未来周期预测：用最后10个数据预测未来20个值（10小时，每30分钟一次）
x_input = data[-time_step:].reshape(1, -1)
temp_input = list(x_input[0])
future_predictions = []

for i in range(20):
    if len(temp_input) > time_step:
        x_input = np.array(temp_input[1:])
        x_input = x_input.reshape(1, -1)
        x_input = x_input.reshape((1, time_step, 1))
        yhat = model.predict(x_input, verbose=0)
        temp_input.extend(yhat[0].tolist())
        temp_input = temp_input[1:]
        future_predictions.extend(yhat.tolist())
    else:
        x_input = x_input.reshape((1, time_step, 1))
        yhat = model.predict(x_input, verbose=0)
        temp_input.extend(yhat[0].tolist())
        future_predictions.extend(yhat.tolist())

# 7. 可视化结果
plt.figure(figsize=(14, 7))
# 绘制训练集、测试集、预测值
train_range = np.arange(len(y_train))
test_range = np.arange(len(y_train), len(y_train) + len(y_test))
future_range = np.arange(len(data), len(data) + len(future_predictions))

plt.plot(train_range, y_train, label="训练集实际湿度", color="blue")
plt.plot(test_range, y_test, label="测试集实际湿度", color="green")
plt.plot(test_range, y_pred_test, label="测试集预测湿度", color="red", linestyle="--")
plt.plot(future_range, future_predictions, label="未来10小时预测", color="orange", linestyle=":")

plt.xlabel("时间步")
plt.ylabel("归一化湿度（0-1）")
plt.title("LSTM模型：实际湿度vs预测湿度（含未来周期预测）")
plt.legend()
plt.grid(True)
plt.savefig("/home/pi/lstm_plot.png")
plt.close()
print("LSTM模型结果图已保存：/home/pi/lstm_plot.png")

# 8. 保存模型（可选，方便后续复用）
model.save("/home/pi/lstm_humidity_model.h5")
print("LSTM模型已保存：/home/pi/lstm_humidity_model.h5")
