# 检查log文件中的IMU数据是否丢失
# 检查美团数据
from pylab import *

FilePath = 'C:\\Users\\wy\\Desktop\\log\\'
# FilePath = 'E:\\项目\\零跑\\2021_07_28\\零跑C11#1（3号鲨鱼鳍）.tar.gz\\lplog\\sdk_log\\'
# FilePath = 'E:\\项目\\零跑\\2021_07_28\\零跑C11#2（4号鲨鱼鳍）.tar.gz\\lplog\\sdk_log\\'
FileName = 'pps.log'
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

DeltaTimeLostIMUDataThreshold = DeltaTimeIMU_Ref * 1.5  # ms
DeltaTimeLostGNSSDataThreshold = 2000  # ms


with open(FileFullPath, 'r') as ff:
    lines = ff.read().split('\n')
GyroX_theta = 0

for line in lines:
    # DataLine = line.split(',')
    index = line.find('qxsensor')
    DataLine = line[index:].split(' ')

    FlagLoopGPIMU = FlagLoopGPIMU + 1
    if FlagLoopGPIMU == 1:
        LastTimeIMUFusion = float(DataLine[2])
    TimeIMUFusion = float(DataLine[2])
    DeltaTimeIMU_Fusion = TimeIMUFusion - LastTimeIMUFusion
    if DeltaTimeIMU_Fusion > DeltaTimeLostIMUDataThreshold:
        print(
            f'GPIMU在时间戳{TimeIMUFusion}处丢失数据, 对应的时间间隔为{DeltaTimeIMU_Fusion}ms, 丢失了{DeltaTimeIMU_Fusion / DeltaTimeIMU_Ref - 1}个数据')
    elif DeltaTimeIMU_Fusion < 0:
        print(f'GPIMU在时间戳{TimeIMUFusion}处发生时间倒退, 对应的时间间隔为{DeltaTimeIMU_Fusion}ms')
    if len(DataLine) < 6:
        print(f'GPIMU在时间戳{TimeIMUFusion}处发生时间数据行缺失')
    LastTimeIMUFusion = TimeIMUFusion
    GyroX_Fusion = float(DataLine[6])
    GyroY_Fusion = float(DataLine[7])
    GyroZ_Fusion = float(DataLine[8])
    AccX_Fusion = float(DataLine[3])
    AccY_Fusion = float(DataLine[4])
    AccZ_Fusion = float(DataLine[5])
    # if GyroX_Fusion > 0.2 or GyroY_Fusion > 0.2 or GyroZ_Fusion > 0.2:
    #     print(
    #         f'GPIMU在时间戳{TimeIMUFusion}处数据异常')
        # GyroX_theta = GyroX_theta + GyroY_Fusion * DeltaTimeIMU_Fusion / 1000 * 180 / 3.14159

    DeltaTimeIMU_Fusion_list.append(DeltaTimeIMU_Fusion)
    TimeIMUFusion_list.append(TimeIMUFusion)
    GyroX_Fusion_list.append(GyroX_Fusion)
    GyroY_Fusion_list.append(GyroY_Fusion)
    GyroZ_Fusion_list.append(GyroZ_Fusion)
    AccX_Fusion_list.append(AccX_Fusion)
    AccY_Fusion_list.append(AccY_Fusion)
    AccZ_Fusion_list.append(AccZ_Fusion)


if IMU_Single:
    plt.figure()
    xlabel('Sample Number')
    ylabel('Time interval[ms]')
    plt.title('Time Interval of IMU')
    plt.grid()
    plt.plot(DeltaTimeIMU_Fusion_list[1:], linestyle='-', linewidth=0.5, color='r')

print(f'IMU log 记录了{(TimeIMUFusion_list[-1] - TimeIMUFusion_list[0]) / 1000 / 3600}小时')


plt.figure()
xlabel('Sample Number')
ylabel('Acc[m/s^2]')
plt.title('Acc')
plt.grid()
plt.plot(AccX_Fusion_list, linestyle='-', color='r', linewidth='0.5', label='x_axis')
plt.plot(AccY_Fusion_list, linestyle='-', color='g', linewidth='0.5', label='y_axis')
plt.plot(AccZ_Fusion_list, linestyle='-', color='b', linewidth='0.5', label='z_axis')
plt.legend()
# plt.legend(loc='upper right')

plt.figure()
xlabel('Sample Number')
ylabel('Gyro[rad/s]')
plt.title('Gyro')
plt.plot(GyroX_Fusion_list, linestyle='-', color='r', linewidth='0.5', label='x_axis')
plt.plot(GyroY_Fusion_list, linestyle='-', color='g', linewidth='0.5', label='y_axis')
plt.plot(GyroZ_Fusion_list, linestyle='-', color='b', linewidth='0.5', label='z_axis')
plt.grid()
plt.legend()
# plt.legend(loc='upper right')


plt.figure()
xlabel('Sample Number')
ylabel('Gyro[deg/s]')
plt.title('Gyro')
plt.plot(rad2deg(GyroX_Fusion_list), linestyle='-', color='r', linewidth='0.5', label='x_axis')
plt.plot(rad2deg(GyroY_Fusion_list), linestyle='-', color='g', linewidth='0.5', label='y_axis')
plt.plot(rad2deg(GyroZ_Fusion_list), linestyle='-', color='b', linewidth='0.5', label='z_axis')
plt.grid()
plt.legend()

plt.show()
