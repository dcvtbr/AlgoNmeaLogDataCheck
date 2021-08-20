# 检查log文件中的IMU数据是否丢失
from pylab import *

FilePath = 'E:\\项目\\'
# FilePath = 'E:\\项目\\零跑\\2021_07_28\\零跑C11#1（3号鲨鱼鳍）.tar.gz\\lplog\\sdk_log\\'
# FilePath = 'E:\\项目\\零跑\\2021_07_28\\零跑C11#2（4号鲨鱼鳍）.tar.gz\\lplog\\sdk_log\\'
FileName = 'pps1.log'
FileFullPath = FilePath + FileName

IMU_Array = False  # 对应IMU阵列的log文件
IMU_Single = not IMU_Array  # 对应单个IMU的log文件
ProcessGNSS = True  # 查看GNSS数据
FlagLoopGPIMU = 0
FlagLoopGPIMU1 = 0
FlagLoopGPIMU2 = 0
FlagLoopGPIMU3 = 0
FlagLoopGPOLY = 0
FlagLoopGPINR = 0
FlagLoopGPPPS = 0

SampleRateIMU = 50  # Hz
SampleRateGNSS = 1  # Hz
DeltaTimeLostIMUDataThreshold = 100  # ms
DeltaTimeLostGNSSDataThreshold = 2000  # ms

DeltaTimeIMU_Fusion_list = []
TimeIMUFusion_list = []
GyroX_Fusion_list = []
GyroY_Fusion_list = []
GyroZ_Fusion_list = []
AccX_Fusion_list = []
AccY_Fusion_list = []
AccZ_Fusion_list = []

# IMU丢失的数量
CountIMUFusionLost = CountIMU1Lost = CountIMU2Lost = CountIMU3Lost = 0

# IMU和 GNSS上一个时间戳
LastTimeIMU3 = LastTimeIMU2 = LastTimeIMU1 = LastTimeIMUFusion = 0
LastTimeGNSS = float(0)
LastTimeGPINR = float(0)
LastTimeGPPPS = float(0)

# 采样间隔
DeltaTimeIMU_Ref = float((1 / SampleRateIMU) * 1000)
DeltaTimeGNSS_Ref = float((1 / SampleRateGNSS) * 1000)

with open(FileFullPath, 'r') as ff:
    lines = ff.read().split('\n')
GyroX_theta = 0

for line in lines:
    # DataLine = line.split(',')
    index = line.find('m_Time')
    # print(type(line))
    # print(line[index:].split(' '))
    Data = line[index:].split(' ')
    print(type(Data))
    print(Data[1])
