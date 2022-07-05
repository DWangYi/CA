import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
from Fc_Te_Cal import FcTeCal, FMCal_VSP, EMCal_CO, EMCal_NO, EMCal_VOC, EMCal_PM

#设置画图字体
plt.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['axes.unicode_minus'] = False
#设置随机种子
#np.random.seed(0)

#参数设置说明
##环形车道长度400米，每个元胞0.01米，仿真时间200秒，仿真步长0.1秒。
path = 100000.0   # 元胞总数
n = 40       # 车辆数目
ltv = 3500      # 最大限速
p = 0.15        # 随机减速概率
times = 4000    # 模拟的时刻数目
step = 0.1      #仿真步长
PER = 0.5      # 网联车渗透率
RT_HV = 2.0      #人工车辆反应时间
RT_AV = 0.6      # AV车辆反应时间
Ac = 200        # 车辆一般加速度 2 m2/s
De = 300         # 车辆一般减速度  3 m2/s
DE = 500         # 车辆最大减速度  5 m2/s
cl = 500        # 车辆车身长度     5米
ds_cav = 50     # CAV车辆安全距离 定义为常数  0.5米
M = 10         # 随机次数
avg_V = np.zeros(M) #记录每个随机过程中的速度平均值
std_V = np.zeros(M) #记录每个随机过程中的速度标准差
avg_F = np.zeros(M) #记录每个随机过程中的流量平均值
avg_MOE = np.zeros((M, 4)) #记录每个随机过程中的污染物排放
avg_NFR = np.zeros(M) #记录每个随机过程中的油耗
avg_ECO = np.zeros(M) #记录每个随机过程中的CO2排放
avg_ENO = np.zeros(M) #记录每个随机过程中的NO排放
avg_EVOC = np.zeros(M) #记录每个随机过程中的VOC排放
avg_EPM = np.zeros(M) #记录每个随机过程中的PM排放

#定义相关函数
##安全距离计算函数 v1为当前车，v2为前车
def d_safe(v1,v2):
    a = mat[0] # 车辆为人工车辆，则a=1，否则a=0
    b = mat[1] # 车辆为AV车辆，则b=1，否则b=0
    c = mat[2] # 车辆为CAV车辆，则c=1，否则c=0
    ds = v1*(a*RT_HV+b*RT_AV) + (a+b)*(v1**2-v2**2)/(2.0*DE) + c*ds_cav
    return round(ds)
##FollowerStopper策略速度生成函数
def FSC(v, v1, dis, U):
    delta_x10 = 4.5; delta_x20 = 5.25; delta_x30 = 6.0
    d1 = 1.5; d2 = 1.0; d3 = 0.5
    delta_x1 = delta_x10 + (min(v1-v, 0) ** 2) / (2.0 * d1)
    delta_x2 = delta_x20 + (min(v1-v, 0) ** 2) / (2.0 * d2)
    delta_x3 = delta_x30 + (min(v1-v, 0) ** 2) / (2.0 * d3)
    if dis <= delta_x1:
        v_cmd = 0
    elif (dis > delta_x1)&(dis <= delta_x2):
        v_cmd = min(max(v1, 0), U)*(dis-delta_x1)/(delta_x2-delta_x1)
    elif (dis > delta_x2)&(dis <= delta_x3):
        v_cmd = min(max(v1, 0), U) + (U-min(max(v1, 0), U)) * (dis - delta_x2) / (delta_x3 - delta_x2)
    else:
        v_cmd = U
    return v_cmd

def DBP(v1, v2, dis1, dis2, deltaT):          #v1为t时刻车辆n-1速度；v2为t时刻车辆n+1速度；dis1为车辆n与车辆n-1的距离；dis2为车辆n+1与车辆n的距离
    return 0.5*(v1+v2-((dis1-dis2)/deltaT))




for m in range(M):
    #随机生成联网车辆编号
    random.seed(100)
    AV_index = random.sample(range(0,n), int(n*PER))
    #AV_index = list(np.arange(0, n, 2))
    #AV_index.sort()
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
    v = np.random.randint(0.49*ltv, 0.5*ltv, [n])
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
            # 计算当前车n与前车n-1的距离以及安全距离，注意是环形车道，i的前车为i-1
            if x[i] > x[i-1]:
                d = path - x[i] + x[i-1] - cl
                ds = d_safe(v[i], v[i-1])  #计算当前车当前速度下的对应安全距离
            else:
                d = x[i-1] - x[i] - cl
                ds = d_safe(v[i], v[i-1])  #计算当前车当前速度下的对应安全距离

            # 计算n与n+1的距离以及安全距离，注意是环形车道，i的前车为i-1
            if i<39:
                if x[i+1] > x[i]:
                    d1 = path - x[i+1] + x[i] - cl
                else:
                    d1 = x[i] - x[i+1] - cl
            else:
                if x[0] > x[i]:
                    d1 = path - x[0] + x[i] - cl
                else:
                    d1 = x[i] - x[0] - cl


            #根据车辆跟车类型、当前速度、前车距离进行加速、减速、随机慢化
            if mat[0] == 1 :  #车辆为 HV
                if d > ds:    #当前车与前车之间的距离大于安全距离，车辆将加速
                   v1[i] = min(v[i]+Ac*step, ltv, d)
                else:
                    v1[i] = max(0, min(v[i], d))
                #随机慢化
                if t%(RT_HV/step) == 0:
                    ran = np.random.random()
                    if (ran <= p) :
                        SDM[i][t] = 1
                        v1[i] = min(max(v1[i] - SDM[i][t] * De * step, 0), d)
                else:
                    SDM[i][t] = SDM[i][t-1]
                    v1[i] = max(0, min(v1[i] - SDM[i][t] * De * step, d))
            elif mat[1] == 1:   #车辆为 AV
                #v_cmd = DBP(v[i-1], v[i+1],  DMtx[t][i], DMtx[t][i+1], step)
                v_cmd = DBP(v[i - 1], v[i + 1], d, d+1, step)
                v1[i] = max(0, min(v_cmd, ltv, d))
                #v1[i] = v_cmd
            else:      #车辆为 CAV
                if d > ds:  # 当前车与前车之间的距离大于安全距离，车辆将加速
                    v1[i] = min(v[i] + Ac * step, ltv, d + v1[i - 1] - ds)
                else:
                    v1[i] = v1[i - 1]
            DSafeMtx[t][i] = ds
            DMtx[t][i] = d
        # norm = matplotlib.colors.Normalize(vmin=0, vmax=300)
        # plt.scatter([t/10]*n, x/100, marker='o', s=0.1, alpha=1,linewidths=0.2, c=v, cmap='jet_r', norm=norm)  #在图上绘制该时刻所有车辆的位置,横轴为t,纵轴为x

        #保存每个时刻的每辆车的位置、速度数据；对位置数据和速度数据进行更新
        Xlist = np.vstack((Xlist, (x + v1*step)%(path)))
        Vlist = np.vstack((Vlist, v1))
        # 更新流量
        for i in range(n):
            if (x[i] + v1[i] * step) > path:
                flow_count += 1
        x = (x + v1*step)%(path-1)     #更新位置
        v = v1.copy()         #更新速度

    #指标 计算100秒以后的指标
    ##平均速度
    avg_V[m] = np.mean(Vlist[1000:,:], axis=0).mean()/100.0
    std_V[m] = np.std(Vlist[1000:, :] / 100.0)
    avg_F[m] = max(round(flow_count/(times*step)*3600, 0), 0)

    Alist = np.diff(Vlist[:], axis=0) / step
    avg_MOE[m] = FcTeCal(Vlist[1000:-1], Alist[1000:], step)
    avg_NFR[m] = FMCal_VSP(Vlist[1000:-1], Alist[1000:], step)
    avg_ECO[m] = EMCal_CO(Vlist[1000:-1], Alist[1000:], step)
    avg_ENO[m] = EMCal_NO(Vlist[1000:-1], Alist[1000:], step)
    avg_EVOC[m] = EMCal_VOC(Vlist[1000:-1], Alist[1000:], step)
    avg_EPM[m] = EMCal_PM(Vlist[1000:-1], Alist[1000:], step)

    avg_NFR1 = 1000.0 / avg_V.mean() * avg_NFR
    avg_ECO1 = 1000.0 / avg_V.mean() * avg_ECO
    avg_ENO1 = 1000.0 / avg_V.mean() * avg_ENO
    avg_EVOC1 = 1000.0 / avg_V.mean() * avg_EVOC
    avg_EPM1 = 1000.0 / avg_V.mean() * avg_EPM


print(np.mean(avg_MOE, axis=0))
print(avg_NFR1.mean())
print(avg_ECO1.mean())
print(avg_ENO1.mean())
print(avg_EVOC1.mean())
print(avg_EPM1.mean())
print(u'距离均衡模拟,车辆%.0f辆,渗透率%.2f,平均速度%.2f m/s,流量%.2f veh/s,平均速度标准差%.2f' % (n, PER, avg_V.mean(), avg_F.mean(), std_V.mean()))



#设置图片尺寸
plt.figure(figsize=(6, 4), facecolor='w')

for i in range(n):
    plty = Xlist[:, i]
    pltx = np.arange(0, times+1)
    if matlist[i][0] != 1:
        plt.scatter(pltx/10, plty/100, marker='o', c="red", s=0.1, alpha=1, linewidths=0.2)
    else:
        plt.scatter(pltx / 10, plty / 100, marker='o', c="green", s=0.1, alpha=1, linewidths=0.2)

# 画图展示
plt.xlim(0, times*step)
plt.ylim(0, path/100)
plt.ylabel(u'Position(meters)')
plt.xlabel(u'Time(sec.)')
cbar = plt.colorbar()
cbar.set_label('Velocity(m/s)')
plt.clim(0, 3)
#plt.colorbar()
plt.savefig(u'距离均衡轨迹模拟(密度%d,车辆数%d,渗透率%s,减速概率%s).png' % (round(n/(path/100000), 2), n, PER, p), dpi=600)
plt.show()
