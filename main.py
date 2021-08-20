# 检查log文件中的IMU数据是否丢失
from pylab import *

FilePath = 'E:\\项目\\零跑\\2021-08-10零跑鲨鱼鳍天线外中内环对比测试\\log\\零跑C11#1（5号鲨鱼鳍）\\lplog\\sdk_log\\'
# FilePath = 'E:\\项目\\零跑\\2021_07_28\\零跑C11#1（3号鲨鱼鳍）.tar.gz\\lplog\\sdk_log\\'
# FilePath = 'E:\\项目\\零跑\\2021_07_28\\零跑C11#2（4号鲨鱼鳍）.tar.gz\\lplog\\sdk_log\\'
FileName = 'algo_nmea_1.log'
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
DeltaTimeIMU1_list = []
GyroX1_list = []
GyroY1_list = []
GyroZ1_list = []
AccX1_list = []
AccY1_list = []
AccZ1_list = []
DeltaTimeIMU2_list = []
GyroX2_list = []
GyroY2_list = []
GyroZ2_list = []
AccX2_list = []
AccY2_list = []
AccZ2_list = []
DeltaTimeIMU3_list = []
GyroX3_list = []
GyroY3_list = []
GyroZ3_list = []
AccX3_list = []
AccY3_list = []
AccZ3_list = []
DeltaTimeGNSS_list = []
LatGNSS_list = []
LonGNSS_list = []
AltGNSS_list = []
DeltaTimeGPINR_list = []
LatGPINR_list = []
LonGPINR_list = []
AltGPINR_list = []
DeltaTimeGPPPS_list = []

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
    DataLine = (line.split(','))
    if DataLine[0] == '$GPIMU':
        FlagLoopGPIMU = FlagLoopGPIMU + 1
        if FlagLoopGPIMU == 1:
            LastTimeIMUFusion = float(DataLine[3])
        TimeIMUFusion = float(DataLine[3])
        DeltaTimeIMU_Fusion = TimeIMUFusion - LastTimeIMUFusion

        if DeltaTimeIMU_Fusion > DeltaTimeLostIMUDataThreshold:
            print(
                f'GPIMU在时间戳{TimeIMUFusion}处丢失数据, 对应的时间间隔为{DeltaTimeIMU_Fusion}ms, 丢失了{DeltaTimeIMU_Fusion / DeltaTimeIMU_Ref - 1}个数据')
        elif DeltaTimeIMU_Fusion < 0:
            print(f'GPIMU在时间戳{TimeIMUFusion}处发生时间倒退, 对应的时间间隔为{DeltaTimeIMU_Fusion}ms')

        LastTimeIMUFusion = TimeIMUFusion
        GyroX_Fusion = float(DataLine[4])
        GyroY_Fusion = float(DataLine[5])
        GyroZ_Fusion = float(DataLine[6])
        AccX_Fusion = float(DataLine[7])
        AccY_Fusion = float(DataLine[8])
        AccZ_Fusion = float(DataLine[9])
        # if 2299427 > TimeIMUFusion > 2298343:
        #     GyroX_theta = GyroX_theta + GyroY_Fusion * DeltaTimeIMU_Fusion / 1000 * 180 / 3.14159

        DeltaTimeIMU_Fusion_list.append(DeltaTimeIMU_Fusion)
        TimeIMUFusion_list.append(TimeIMUFusion)
        GyroX_Fusion_list.append(GyroX_Fusion)
        GyroY_Fusion_list.append(GyroY_Fusion)
        GyroZ_Fusion_list.append(GyroZ_Fusion)
        AccX_Fusion_list.append(AccX_Fusion)
        AccY_Fusion_list.append(AccY_Fusion)
        AccZ_Fusion_list.append(AccZ_Fusion)

    if IMU_Array:
        if DataLine[0] == '$GPIMU1':
            FlagLoopGPIMU1 = FlagLoopGPIMU1 + 1
            if FlagLoopGPIMU1 == 1:
                LastTimeIMU1 = float(DataLine[3])
            TimeIMU1 = float(DataLine[3])
            DeltaTimeIMU1 = TimeIMU1 - LastTimeIMU1

            if DeltaTimeIMU1 > DeltaTimeLostIMUDataThreshold:
                print(
                    f'GPIMU1在时间戳{TimeIMU1}处丢失数据, 对应的时间间隔为{DeltaTimeIMU1}ms, 丢失了{DeltaTimeIMU1 / DeltaTimeIMU_Ref - 1}个数据')
            elif DeltaTimeIMU1 < 0:
                print(f'IMU1在时间戳{TimeIMU1}处发生时间倒退, 对应的时间间隔为{DeltaTimeIMU1}ms')

            LastTimeIMU1 = TimeIMU1
            GyroX1 = float(DataLine[4])
            GyroY1 = float(DataLine[5])
            GyroZ1 = float(DataLine[6])
            AccX1 = float(DataLine[7])
            AccY1 = float(DataLine[8])
            AccZ1 = float(DataLine[9])

            DeltaTimeIMU1_list.append(DeltaTimeIMU1)
            GyroX1_list.append(GyroX1)
            GyroY1_list.append(GyroY1)
            GyroZ1_list.append(GyroZ1)
            AccX1_list.append(AccX1)
            AccY1_list.append(AccY1)
            AccZ1_list.append(AccZ1)

        elif DataLine[0] == '$GPIMU2':
            FlagLoopGPIMU2 = FlagLoopGPIMU2 + 1
            if FlagLoopGPIMU2 == 1:
                LastTimeIMU2 = float(DataLine[3])
            TimeIMU2 = float(DataLine[3])
            DeltaTimeIMU2 = TimeIMU2 - LastTimeIMU2

            if DeltaTimeIMU2 > DeltaTimeLostIMUDataThreshold:
                print(
                    f'GPIMU2在时间戳{TimeIMU2}处丢失数据, 对应的时间间隔为{DeltaTimeIMU2}ms, 丢失了{DeltaTimeIMU2 / DeltaTimeIMU_Ref - 1}个数据')
            elif DeltaTimeIMU2 < 0:
                print(f'GPIMU2在时间戳{TimeIMU2}处发生时间倒退, 对应的时间间隔为{DeltaTimeIMU2}ms')

            LastTimeIMU2 = TimeIMU2
            GyroX2 = float(DataLine[4])
            GyroY2 = float(DataLine[5])
            GyroZ2 = float(DataLine[6])
            AccX2 = float(DataLine[7])
            AccY2 = float(DataLine[8])
            AccZ2 = float(DataLine[9])

            DeltaTimeIMU2_list.append(DeltaTimeIMU2)
            GyroX2_list.append(GyroX2)
            GyroY2_list.append(GyroY2)
            GyroZ2_list.append(GyroZ2)
            AccX2_list.append(AccX2)
            AccY2_list.append(AccY2)
            AccZ2_list.append(AccZ2)

        elif DataLine[0] == '$GPIMU3':
            FlagLoopGPIMU3 = FlagLoopGPIMU3 + 1
            if FlagLoopGPIMU3 == 1:
                LastTimeIMU3 = float(DataLine[3])
            TimeIMU3 = float(DataLine[3])
            DeltaTimeIMU3 = TimeIMU3 - LastTimeIMU3

            if DeltaTimeIMU3 > DeltaTimeLostIMUDataThreshold:
                print(
                    f'GPIMU3在时间戳{TimeIMU3}处丢失数据, 对应的时间间隔为{DeltaTimeIMU3}ms, 丢失了{DeltaTimeIMU3 / DeltaTimeIMU_Ref - 1}个数据')
            elif DeltaTimeIMU3 < 0:
                print(f'GPIMU3在时间戳{TimeIMU3}处发生时间倒退, 对应的时间间隔为{DeltaTimeIMU3}ms')

            LastTimeIMU3 = TimeIMU3
            GyroX3 = float(DataLine[4])
            GyroY3 = float(DataLine[5])
            GyroZ3 = float(DataLine[6])
            AccX3 = float(DataLine[7])
            AccY3 = float(DataLine[8])
            AccZ3 = float(DataLine[9])

            DeltaTimeIMU3_list.append(DeltaTimeIMU3)
            GyroX3_list.append(GyroX3)
            GyroY3_list.append(GyroY3)
            GyroZ3_list.append(GyroZ3)
            AccX3_list.append(AccX3)
            AccY3_list.append(AccY3)
            AccZ3_list.append(AccZ3)

    if ProcessGNSS:
        if DataLine[0] == '$GNOLY':
            FlagLoopGPOLY = FlagLoopGPOLY + 1
            if FlagLoopGPOLY == 1:
                LastTimeGNSS = float(DataLine[3])
            TimeGNSS = float(DataLine[3])
            DeltaTimeGNSS = TimeGNSS - LastTimeGNSS

            if DeltaTimeGNSS > DeltaTimeLostGNSSDataThreshold:
                print(
                    f'GNOLY在时间戳{TimeGNSS}处丢失数据, 对应的时间间隔为{DeltaTimeGNSS}ms, 丢失了{DeltaTimeGNSS / DeltaTimeGNSS_Ref - 1}个数据')
            elif DeltaTimeGNSS < 0:
                print(f'GNOLY在时间戳{TimeGNSS}处发生时间倒退, 对应的时间间隔为{DeltaTimeGNSS}ms')

            LastTimeGNSS = TimeGNSS
            GGAFlag = float(DataLine[4])
            Lat = float(DataLine[5])
            Lon = float(DataLine[6])
            Alt = float(DataLine[7])
            Heading = float(DataLine[8])
            Speed = float(DataLine[9])
            SatInUse = float(DataLine[10])

            DeltaTimeGNSS_list.append(DeltaTimeGNSS)
            LatGNSS_list.append(Lat)
            LonGNSS_list.append(Lon)
            AltGNSS_list.append(Alt)

        if DataLine[0] == '$GPINR':
            FlagLoopGPINR = FlagLoopGPINR + 1
            if FlagLoopGPINR == 1:
                LastTimeGPINR = float(DataLine[3])
            TimeGPINR = float(DataLine[3])
            DeltaTimeGPINR = TimeGPINR - LastTimeGPINR

            if DeltaTimeGPINR > DeltaTimeLostGNSSDataThreshold:
                print(
                    f'GPINR在时间戳{TimeGPINR}处丢失数据, 对应的时间间隔为{DeltaTimeGPINR}ms, 丢失了{DeltaTimeGPINR / DeltaTimeGNSS_Ref - 1}个数据')
            elif DeltaTimeGPINR < 0:
                print(f'GPINR在时间戳{TimeGPINR}处发生时间倒退, 对应的时间间隔为{DeltaTimeGPINR}ms')

            LastTimeGPINR = TimeGPINR
            Lat = float(DataLine[4])
            Lon = float(DataLine[5])
            Alt = float(DataLine[6])

            DeltaTimeGPINR_list.append(DeltaTimeGPINR)
            LatGPINR_list.append(Lat)
            LonGPINR_list.append(Lon)
            AltGPINR_list.append(Alt)

        if DataLine[0] == '$GPPPS':
            FlagLoopGPPPS = FlagLoopGPPPS + 1
            if FlagLoopGPPPS == 1:
                LastTimeGPPPS = float(DataLine[3])
            TimeGPPPS = float(DataLine[3])
            DeltaTimeGPPPS = TimeGPPPS - LastTimeGPPPS

            if DeltaTimeGPPPS > DeltaTimeLostGNSSDataThreshold:
                print(
                    f'GPPPS在时间戳{TimeGPPPS}处丢失数据, 对应的时间间隔为{DeltaTimeGPPPS}ms, 丢失了{DeltaTimeGPPPS / DeltaTimeGNSS_Ref - 1}个数据')
            elif DeltaTimeGPPPS < 0:
                print(f'GPPPS在时间戳{TimeGPPPS}处发生时间倒退, 对应的时间间隔为{DeltaTimeGPPPS}ms')

            LastTimeGPPPS = TimeGPPPS
            DeltaTimeGPPPS_list.append(DeltaTimeGPPPS)

if IMU_Array:
    plt.figure()
    xlabel('Sample Number')
    ylabel('Time interval[ms]')
    plt.title('TimeDiff_IMU_Fusion_in_IMUArray')
    plt.plot(DeltaTimeIMU_Fusion_list[1:], linestyle='-', linewidth=0.5, color='r')

    plt.figure()
    xlabel('Sample Number')
    ylabel('Time interval[ms]')
    plt.title('TimeDiff_IMU_First_in_IMUArray')
    plt.plot(DeltaTimeIMU1_list[1:], linestyle='-', linewidth=0.5, color='r')

    plt.figure()
    xlabel('Sample Number')
    ylabel('Time interval[ms]')
    plt.title('TimeDiff_IMU_Second_in_IMUArray')
    plt.plot(DeltaTimeIMU2_list[1:], linestyle='-', linewidth=0.5, color='r')

    plt.figure()
    xlabel('Sample Number')
    ylabel('Time interval[ms]')
    plt.title('TimeDiff_IMU_Third_in_IMUArray')
    plt.plot(DeltaTimeIMU3_list[1:], linestyle='-', linewidth=0.5, color='r')

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
ylabel('Time interval[ms]')
plt.title('Time Interval of GNOLY')
plt.grid()
plt.plot(DeltaTimeGNSS_list[2:], linestyle='-', linewidth=0.5, color='r')

plt.figure()
xlabel('Sample Number')
ylabel('Time interval[ms]')
plt.title('Time Interval of GPPPS')
plt.grid()
plt.plot(DeltaTimeGPPPS_list[1:], linestyle='-', linewidth=0.5, color='r')

plt.figure()
xlabel('Sample Number')
ylabel('Time interval[ms]')
plt.title('Time Interval of GPINR')
plt.grid()
plt.plot(DeltaTimeGPINR_list[1:], linestyle='-', linewidth=0.5, color='r')

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

plt.show()
