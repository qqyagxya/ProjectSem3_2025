import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. 读取去噪后的数据
input_csv = "/home/pi/denoised_data.csv"
df = pd.read_csv(input_csv)

# 2. 初始化Min-Max缩放器（目标范围[0,1]）
scaler = MinMaxScaler(feature_range=(0, 1))

# 3. 对湿度数据归一化（只处理需要建模的列）
df["normalized_humidity"] = scaler.fit_transform(df[["denoised_humidity"]])

# 4. 保存归一化后的数据
output_csv = "/home/pi/normalized_data.csv"
df.to_csv(output_csv, index=False)
print(f"归一化后数据已保存：{output_csv}")

# 5. 查看归一化结果
print("\n归一化后湿度统计：")
print(df["normalized_humidity"].describe())
print(f"归一化最小值：{df['normalized_humidity'].min():.4f}")
print(f"归一化最大值：{df['normalized_humidity'].max():.4f}")  # 应接近1
