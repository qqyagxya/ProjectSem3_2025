import board
import digitalio
import busio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
import time

# 初始化SPI总线（连接树莓派SPI引脚）
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# 初始化CS（芯片选择）引脚
cs = digitalio.DigitalInOut(board.D8)  # D8对应树莓派物理引脚24

# 初始化MCP3008
mcp = MCP3008(spi, cs)

# 初始化传感器通道（MCP3008的CH0）
channel = AnalogIn(mcp, MCP3008.P0)

# 循环读取数据（每2秒读一次）
try:
    while True:
        # 读取原始值（0-65535）和电压（0-3.3V）
        raw_value = channel.value
        voltage = channel.voltage
        # 转换为湿度百分比（电容式传感器：电压越高，湿度越低，需校准）
        humidity = 100 - (voltage / 3.3) * 100  # 粗略校准，后续可调整
        print(f"原始值：{raw_value} | 电压：{voltage:.2f}V | 湿度：{humidity:.2f}%")
        time.sleep(2)
except KeyboardInterrupt:
    # 按Ctrl+C停止脚本
    print("脚本已停止")
