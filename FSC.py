import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
from matplotlib.pyplot import MultipleLocator, FormatStrFormatter
import pandas as pd
from Fc_Te_Cal import FMCal_VSP, EMCal_CO, EMCal_NO, EMCal_VOC, EMCal_PM

#设置画图字体
plt.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['axes.unicode_minus'] = False
#设置随机种子
#np.random.seed(0)


#参数设置说明
path = 100000.0   # 元胞总数
ltv = 3500      # 最大限速
p = 0.15         # 随机减速概率
times = 4000    # 模拟的时刻数目
step = 0.1      #仿真步长
RT_HV = 2      #人工车辆反应时间
RT_AV = 0.6      # AV车辆反应时间
Ac = 200        # 车辆一般加速度 2 m2/s
De1 = 200         # 车辆一般减速度  3 m2/s
De2 = 250         # 车辆一般减速度  3 m2/s
DE = 500         # 车辆最大减速度  5 m2/s
cl = 500        # 车辆车身长度     5米
ds_cav = 50     # CAV车辆安全距离 定义为常数  0.5米
avg_VList = np.zeros((20, 11))
std_VList = np.zeros((20, 11))
avg_CVList = np.zeros((20, 11))  #记录每个饱和度、密度对应平均速度变异系数
avg_CRList = np.zeros((20, 11))  #记录每个饱和度、密度对应拥堵比例
flowList = np.zeros((20, 11))
NFRList = np.zeros((20, 11))  #记录每个饱和度、密度对应油耗
ECOList = np.zeros((20, 11))  #记录每个饱和度、密度对应CO2排放
ENOList = np.zeros((20, 11))  #记录每个饱和度、密度对应NO排放
EVOCList = np.zeros((20, 11))  #记录每个饱和度、密度对应VOC排放
EPMList = np.zeros((20, 11))  #记录每个饱和度、密度对应PM排放

M = 15          # 随机次数



#定义相关函数
##安全距离计算函数 v1为当前车，v2为前车
def d_safe(v1,v2):
    a = mat[0] # 车辆为人工车辆，则a=1，否则a=0
    b = mat[1] # 车辆为AV车辆，则b=1，否则b=0
    c = mat[2] # 车辆为CAV车辆，则c=1，否则c=0
    ds = v1*(a*RT_HV+b*RT_AV) + (a+b)*(v1**2-v2**2)/(2.0*DE) + c*ds_cav
    return round(ds)
##FollowerStopper策略速度生成函数
def FSC(v, delta_v, dis, U):
    delta_x10 = 4.5; delta_x20 = 5.25; delta_x30 = 6.0
    d1 = 1.5; d2 = 1.0; d3 = 0.5
    delta_x1 =  delta_x10 + (min(delta_v,0)**2)/(2.0*d1)
    delta_x2 = delta_x20 + (min(delta_v, 0) ** 2) / (2.0 * d2)
    delta_x3 = delta_x30 + (min(delta_v, 0) ** 2) / (2.0 * d3)
    if dis <= delta_x1:
        v_cmd = 0
    elif (dis > delta_x1)&(dis <= delta_x2):
        v_cmd = v*(dis-delta_x1)/(delta_x2-delta_x1)
    elif (dis > delta_x2)&(dis <= delta_x3):
        v_cmd = v + (U-v) * (dis - delta_x2) / (delta_x3 - delta_x2)
    else:
        v_cmd = U
    return v_cmd


for per in range(0,11,1):   #遍历不同的渗透率
    PER = per * 0.1
    for u in range(5,101,5):  #遍历不同的密度
        n = u
        print(u'渗透率%.2f ,密度%.2f' % (PER, n))
        avg_V = np.zeros(M)  # 记录每个随机过程中的速度平均值
        std_V = np.zeros(M)  # 记录每个随机过程中的速度标准差
        avg_CV = np.zeros(M)  # 记录每个随机过程中的速度变异系数
        avg_CR = np.zeros(M)  # 记录每个随机过程中的拥堵比例
        avg_F = np.zeros(M)  # 记录每个随机过程中的流量平均值
        avg_NFR = np.zeros(M)  # 记录每个随机过程中的油耗
        avg_ECO = np.zeros(M)  # 记录每个随机过程中的CO2排放
        avg_ENO = np.zeros(M)  # 记录每个随机过程中的NO排放
        avg_EVOC = np.zeros(M)  # 记录每个随机过程中的VOC排放
        avg_EPM = np.zeros(M)  # 记录每个随机过程中的PM排放
        for m in range(M):   #遍历每一个随机过程
            #随机生成联网车辆编号
            random.seed(100)
            AV_index = random.sample(range(0,n), int(n*PER))
            AV_index.sort()
            # 初始化车辆类型列表并对列表进行遍历更新，得到每个车辆的跟车类型(HV\AV\CAV)
            matlist=[[0]*3 for i in range(n)]
            nlist = range(n)
            for i in range(n):
                if i in AV_index:
                    if nlist[i - 1] in AV_index:
                        matlist[i][2] = 1
                    else:
                        matlist[i][1] = 1
                else:
                    matlist[i][0] = 1

            # x保存每辆车在当前时刻道路上的位置，初始化均匀分布,编号为0的车对应x越大
            x = np.round(np.linspace(path, 0, n, endpoint=False))
            Xlist = x.copy()   # Xlist作为每个时刻车辆位置的矩阵
            # 初始化速度，v保存每辆车当前时刻的速度，按正态分布进行速度初始化，按截断正态分布进行生成
            v=np.random.randint(0.99*ltv, 1.0*ltv, [n])
            #v[-1] = ltv       #当渗透率为100%时，将头车的速度设置为最大速度
            v1 = v.copy()      #v1作为下一时刻速度更新容器
            Vlist = v.copy()   # Vlist作为每个时刻车辆速度的矩阵
            flow_count = 0     # flow_count记录流量
            #记录随机慢化
            SDM = np.zeros((n,times))
            #记录安全距离和距离
            DSafeMtx = np.zeros((times,n))
            DMtx = np.zeros((times,n))
            # 记录加速度
            Alist = np.zeros((times, n))
            #开始仿真
            for t in range(times):  # 遍历每个时刻
                for i in range(n): # 遍历每辆车
                    mat = matlist[i]  # 确定车辆类型
                    # 计算当前车与前车的距离以及安全距离，注意是环形车道，i的前车为i-1
                    if x[i] > x[i-1]:
                        d = path - x[i] + x[i-1] - cl
                        ds = d_safe(v[i],v[i-1])  #计算当前车当前速度下的对应安全距离
                    else:
                        d = x[i-1] - x[i] - cl
                        ds = d_safe(v[i], v[i-1])  #计算当前车当前速度下的对应安全距离
                    #根据车辆跟车类型、当前速度、前车距离进行加速、减速、随机慢化
                    if mat[0] == 1 :  #车辆为 HV
                        if d > ds:    #当前车与前车之间的距离大于安全距离，车辆将加速
                           v1[i] = min(v[i]+Ac*step, ltv, d)
                        else:
                            v1[i] = max(0, min(v[i], d))
                        #随机慢化
                        if t%(RT_HV/step) == 0:
                            ran = np.random.random()
                            if (ran <= p):
                                SDM[i][t] = 1
                                if v[i] < v[i - 1]:
                                    v1[i] = min(max(v1[i] - SDM[i][t] * De2 * step, 0), d)
                                else:
                                    v1[i] = min(max(v1[i] - SDM[i][t] * De1 * step, 0), d)
                        else:
                            SDM[i][t] = SDM[i][t - 1]
                            if v[i] < v[i - 1]:
                                v1[i] = min(max(v1[i] - SDM[i][t] * De2 * step, 0), d)
                            else:
                                v1[i] = min(max(v1[i] - SDM[i][t] * De1 * step, 0), d)
                    elif mat[1] == 1:   #车辆为 AV
                        v_cmd = FSC(v[i] / 100, v[i - 1] / 100, d / 100, Vlist.mean() / 100) * 100
                        a = v_cmd - v[i]
                        v1[i] = max(0, min(v[i] + a * step, ltv, d))
                    else:      #车辆为 CAV
                        if d > ds:  # 当前车与前车之间的距离大于安全距离，车辆将加速
                            v1[i] = min(v[i] + Ac * step, ltv, d + v1[i - 1] - ds)
                        else:
                            v1[i] = v1[i - 1]
                        # v_cmd = FSC(v[i] / 100, v[i - 1] / 100, d / 100, Vlist.mean() / 100) * 100
                        # a = v_cmd - v[i]
                        # v1[i] = max(0, min(v[i] + a * step, ltv, d))
                    DSafeMtx[t][i] = ds
                    DMtx[t][i] = d
                #保存每个时刻的每辆车的位置、速度数据；对位置数据和速度数据进行更新
                Xlist = np.vstack((Xlist, (x + v1*step)%(path)))
                Vlist = np.vstack((Vlist, v1))
                # 更新流量
                for i in range(n):
                    if (x[i] + v1[i] * step) > path:
                        flow_count += 1
                x = (x + v1*step)%(path-1)     #更新位置
                v = v1.copy()        #更新速度

            #指标  计算100秒以后的运行指标
            avg_V[m] = np.mean(Vlist[1000:-1, :], axis=0).mean() / 100.0
            std_V[m] = np.std(Vlist[1000:-1, :]) / 100.0
            avg_CV[m] =  std_V[m] / avg_V[m]
            avg_CR[m] = np.sum(Vlist[1000:-1, :] < 300) / np.sum(Vlist[1000:-1, :] > -1000)
            avg_F[m] = max(round(flow_count / (times * step) * 3600, 0), 0)
            # 计算油耗、排放指标
            Alist = np.diff(Vlist[:], axis=0) / step
            avg_NFR[m] = FMCal_VSP(Vlist[1000:-1], Alist[1000:], step)
            avg_ECO[m] = EMCal_CO(Vlist[1000:-1], Alist[1000:], step)
            avg_ENO[m] = EMCal_NO(Vlist[1000:-1], Alist[1000:], step)
            avg_EVOC[m] = EMCal_VOC(Vlist[1000:-1], Alist[1000:], step)
            avg_EPM[m] = EMCal_PM(Vlist[1000:-1], Alist[1000:], step)
            # 计算安全指标




        avg_NFR1 = 1000.0 / avg_V.mean() * avg_NFR
        avg_ECO1 = 1000.0 / avg_V.mean() * avg_ECO
        avg_ENO1 = 1000.0 / avg_V.mean() * avg_ENO
        avg_EVOC1 = 1000.0 / avg_V.mean() * avg_EVOC
        avg_EPM1 = 1000.0 / avg_V.mean() * avg_EPM


        j = int(u/5) - 1
        k = int(per/1)
        avg_VList[j, k] = round(avg_V.mean(), 2)
        std_VList[j, k] = round(std_V.mean(), 2)
        avg_CVList[j, k] = round(avg_CV.mean(), 2)
        avg_CRList[j, k] = round(avg_CR.mean(), 2)
        flowList[j, k] = round(avg_F.mean(), 2)
        NFRList[j, k] = round(avg_NFR1.mean(), 5)
        ECOList[j, k] = round(avg_ECO1.mean(), 5)
        ENOList[j, k] = round(avg_ENO1.mean(), 5)
        EVOCList[j, k] = round(avg_EVOC1.mean(), 5)
        EPMList[j, k] = round(avg_EPM1.mean(), 5)


flowdata = pd.DataFrame(flowList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
vdata = pd.DataFrame(avg_VList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
std_vdata = pd.DataFrame(std_VList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
avg_cvdata = pd.DataFrame(avg_CVList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
avg_crdata = pd.DataFrame(avg_CRList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
NFRdata = pd.DataFrame(NFRList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
ECOdata = pd.DataFrame(ECOList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
ENOdata = pd.DataFrame(ENOList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
EVOCdata = pd.DataFrame(EVOCList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))
EPMdata = pd.DataFrame(EPMList, columns=['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'], index=np.arange(5,101,5))

# flowdata.to_csv('./data-2 2 2.5 5/FlowData-FSC.csv')
# vdata.to_csv('./data-2 2 2.5 5/VData-FSC.csv')
# std_vdata.to_csv('./data-2 2 2.5 5/Std_VData-FSC.csv')
# avg_cvdata.to_csv('./data-2 2 2.5 5/Avg_CVData-FSC.csv')
# avg_crdata.to_csv('./data-2 2 2.5 5/Avg_CRData-FSC.csv')
# NFRdata.to_csv('./data-2 2 2.5 5/NFRData-FSC.csv')
# ECOdata.to_csv('./data-2 2 2.5 5/ECOData-FSC.csv')
# ENOdata.to_csv('./data-2 2 2.5 5/ENOData-FSC.csv')
# EVOCdata.to_csv('./data-2 2 2.5 5/EVOCData-FSC.csv')
# EPMdata.to_csv('./data-2 2 2.5 5/EPMData-FSC.csv')

# flowdata.to_csv('./data/FlowData-FSC-all.csv')
# vdata.to_csv('./data/VData-FSC-all.csv')
# std_vdata.to_csv('./data/Std_VData-FSC-all.csv')
# avg_cvdata.to_csv('./data/Avg_CVData-FSC-all.csv')
# avg_crdata.to_csv('./data/Avg_CRData-FSC-all.csv')
# NFRdata.to_csv('./data/NFRData-FSC-all.csv')
# ECOdata.to_csv('./data/ECOData-FSC-all.csv')
# ENOdata.to_csv('./data/ENOData-FSC-all.csv')
# EVOCdata.to_csv('./data/EVOCData-FSC-all.csv')
# EPMdata.to_csv('./data/EPMData-FSC-all.csv')


'''
# 设置画布尺寸
plt.figure(figsize=(6, 4), facecolor='w')
marklist = ['o', '^', 's', '*', '+', 'X']
##设置图片格式
plt.xlim(0, 180)
plt.ylim(0, 25000)
plt.ylabel(u'Flow(veh/h)')
plt.xlabel(u'Density(veh/km)')
ax = plt.gca()
xmajorLocator = MultipleLocator(20) #将X轴主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%5.0f') #设置X轴主刻度标签文本的格式
xminorLocator = MultipleLocator(5) #将X轴次刻度标签设置为5的倍数
#设置主刻度标签的位置,标签文本的格式
ax.xaxis.set_major_locator(xmajorLocator)
ax.xaxis.set_major_formatter(xmajorFormatter)
#显示次刻度标签的位置,沒有标签文本
ax.xaxis.set_minor_locator(xminorLocator)
plt.legend(loc='upper left', labels=['P=0%', 'P=20%', 'P=40%', 'P=60%', 'P=80%', 'P=100%'])
plt.show()
plt.savefig(u'流量-密度-CA.png', dpi=600)
plt.clf() #清除图形
'''