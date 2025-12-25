import board
import digitalio
import busio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
from datetime import datetime
import csv

# 初始化SPI和MCP3008（和测试脚本一致）
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP3008.P0)

# 数据保存路径（CSV文件）
csv_path = "/home/pi/sensor_data.csv"

# 初始化CSV文件（写表头）
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "raw_value", "voltage", "humidity(%)"])  # 时间戳、原始值、电压、湿度

# 采集参数：每30分钟一次，持续2天（48小时 = 96次采集）
interval = 30 * 60  # 30分钟（秒）
total_collections = 96  # 48小时 / 0.5小时 = 96次
collection_count = 0

# 开始采集
print(f"开始采集数据，共{total_collections}次，每30分钟一次...")
try:
    while collection_count < total_collections:
        # 获取当前时间
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 读取传感器数据
        raw_value = channel.value
        voltage = channel.voltage
        humidity = 100 - (voltage / 3.3) * 100  # 湿度计算（同测试脚本）
        # 写入CSV
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([now, raw_value, voltage, humidity])
        # 打印日志
        print(f"第{collection_count+1}/{total_collections}次：{now} | 湿度：{humidity:.2f}%")
        # 计数+等待
        collection_count += 1
        time.sleep(interval)
except KeyboardInterrupt:
    print("采集被手动停止")
finally:
    print("采集结束，数据保存在：", csv_path)
