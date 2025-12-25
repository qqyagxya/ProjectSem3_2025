import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取归一化后的数据
input_csv = "/home/pi/normalized_data.csv"
df = pd.read_csv(input_csv)

# 2. 转换时间戳为日期格式（方便时间序列分析）
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 3. 计算描述性统计（均值、标准差、最值等）
stats = df[["denoised_humidity", "normalized_humidity"]].describe()
print("描述性统计结果：")
print(stats)

# 4. 保存统计结果到TXT（放入报告）
stats.to_csv("/home/pi/descriptive_stats.csv", index=True)
print("\n统计结果已保存：/home/pi/descriptive_stats.csv")

# 5. 绘制时间序列图（湿度随时间变化）
plt.figure(figsize=(14, 7))
# 子图1：去噪后湿度趋势
plt.subplot(2, 1, 1)
plt.plot(df["timestamp"], df["denoised_humidity"], color="green")
plt.title("2天土壤湿度时间序列（去噪后）")
plt.ylabel("湿度(%)")
plt.grid(True)

# 子图2：归一化后湿度趋势
plt.subplot(2, 1, 2)
plt.plot(df["timestamp"], df["normalized_humidity"], color="orange")
plt.title("2天土壤湿度时间序列（归一化后）")
plt.xlabel("时间")
plt.ylabel("归一化湿度（0-1）")
plt.grid(True)
plt.xticks(rotation=45)

# 保存图片
plt.tight_layout()
plt.savefig("/home/pi/time_series_plot.png")
plt.close()
print("时间序列图已保存：/home/pi/time_series_plot.png")
