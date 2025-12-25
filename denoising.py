import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取原始数据
input_csv = "/home/pi/sensor_data.csv"  # 你的数据路径
df = pd.read_csv(input_csv)

# 2. 查看原始数据（可选，看是否有异常值）
print("原始数据前5行：")
print(df.head())
print("\n原始数据统计：")
print(df["humidity(%)"].describe())

# 3. 移动平均去噪（窗口大小=5，即取前后5个数据的平均值，可调整）
df["denoised_humidity"] = df["humidity(%)"].rolling(window=5, center=True).mean()

# 4. 去除空值（移动平均后首尾会有空值）
df_clean = df.dropna(subset=["denoised_humidity"])

# 5. 保存去噪后的数据
output_csv = "/home/pi/denoised_data.csv"
df_clean.to_csv(output_csv, index=False)
print(f"\n去噪后数据已保存：{output_csv}")

# 6. 可视化原始数据vs去噪数据（可选，验证效果）
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["humidity(%)"], label="原始湿度", color="gray", alpha=0.5)
plt.plot(df_clean["timestamp"], df_clean["denoised_humidity"], label="去噪后湿度", color="blue")
plt.xlabel("时间")
plt.ylabel("湿度(%)")
plt.title("原始湿度vs去噪后湿度")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/home/pi/denoising_plot.png")  # 保存图片
plt.close()
print("去噪对比图已保存：/home/pi/denoising_plot.png")
