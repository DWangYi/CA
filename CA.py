import numpy as np
from matplotlib.font_manager import *
import matplotlib.pyplot as plt
import random

#设置画图字体
myfont = FontProperties(fname='ns.ttc')
#matplotlib.rcParams['axes.unicode_minus'] = False
#设置随机种子
np.random.seed(0)


#参数设置说明
path = 40000.0   # 元胞总数
n = 20         # 车辆数目
ltv = 3500      # 最大限速
p = 0.2         # 随机减速概率
times = 2000    # 模拟的时刻数目
PER = 0.4       # 网联车渗透率
RT_HV = 2      #人工车辆反应时间
RT_AV = 0.6      # AV车辆反应时间
Ac = 200        # 车辆一般加速度
De = 300         # 车辆一般减速度
DE = 500         # 车辆最大减速度
cl = 500        # 车辆车身长度
ds_cav = 50     # CAV车辆安全距离 定义为常数


#安全距离计算函数 v1为当前车，v2为前车
def d_safe(v1,v2):
    a = mat[0] # 车辆为人工车辆，则a=1，否则a=0
    b = mat[1] # 车辆为AV车辆，则b=1，否则b=0
    c = mat[2] # 车辆为CAV车辆，则c=1，否则c=0
    ds = v1*(a*RT_HV+b*RT_AV) + (a+b)*(v1**2-v2**2)/(2.0*DE) + c*ds_cav
    return round(ds)



#随机生成联网车辆编号
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
# 初始化速度，v保存每辆车当前时刻的速度，按对数正态分布进行速度初始化
v = np.round(np.random.rand(n)*ltv)      #速度随机分布
v1 = v.copy()      #v1作为下一时刻速度更新容器
Vlist = v.copy()   # Vlist作为每个时刻车辆速度的矩阵
#记录随机慢化
SDM = np.zeros((n,times))
#记录安全距离和距离
DSafeMtx = np.zeros((n,times))
DMtx = np.zeros((n,times))


plt.figure(figsize=(5, 4), facecolor='w')
#开始仿真
for t in range(times):  # 遍历每个时刻
    #plt.scatter(x, [t] * n, s=1, c='k', alpha=0.05)  #在图上绘制该时刻所有车辆的位置,横轴为t,纵轴为x
    #plt.plot(x, [t] * n, c='k', alpha=0.05)
    for i in range(n): # 遍历每辆车
        mat = matlist[i]  # 确定车辆类型
        # 计算当前车与前车的距离以及安全距离，注意是环形车道，i的前车为i-1
        if i == 0:
            d = path - x[i] + x[n-1] - cl
            ds = d_safe(v[i],v[n-1])  #计算当前车当前速度下的对应安全距离
        else:
            d = x[i-1] - x[i] - cl
            ds = d_safe(v[i], v[i-1])  #计算当前车当前速度下的对应安全距离
        #根据车辆跟车类型、当前速度、前车距离进行加速、减速、随机慢化
        if mat[0] == 1 :  #车辆为 HV
            if d > ds:    #当前车与前车之间的距离大于安全距离，车辆将加速
               v1[i] = min(v[i]+Ac, ltv, d)
            else:
                v1[i] = min(v[i]-De, d)
            #随机慢化
            if (np.random.random()<=p) & (t%RT_HV == 0):
                SDM[i][t] = 1
                v1[i] = max(v[i] - SDM[i][t]*De, 0)
            elif (np.random.random()>p) & (t%RT_HV == 0):
                SDM[i][t] = 0
                pass #v1[i] = max(v[i] - SDM[i][t]*De, 0)
            else:
                pass #v1[i] = v1[i]
        elif mat[1] == 1:   #车辆为 AV
            if d > ds:    #当前车与前车之间的距离大于安全距离，车辆将加速
               v1[i] = min(v[i]+Ac, ltv, d)
            else:
                v1[i] = min(v[i]-De, d)
        else:      #车辆为 CAV
            if d > ds:    #当前车与前车之间的距离大于安全距离，车辆将加速
               v1[i] = min(v[i]+Ac, ltv, d, d+v1[i-1]-ds)
            else:
                v1[i] = v1[i-1]
        DSafeMtx[i][t] = ds
        DMtx[i][t] = d


    Xlist = np.vstack((Xlist, (x + v)%(path-1)))
    Vlist = np.vstack((Vlist, v1))
    x = (x + v1)%(path-1)     #更新位置
    v = v1         #更新速度


# 画图展示
plt.plot(range(20), Xlist[0,:], c='k', alpha=0.05)
plt.xlim(0, path)
plt.ylim(0, times)
plt.xlabel(u'车辆位置', fontproperties=myfont)
plt.ylabel(u'模拟时间', fontproperties=myfont)
plt.title(u'交通模拟(车道长度%d,车辆数%d,初速度%s,减速概率%s)' % (path/100, n, 200, p), fontproperties=myfont)
# plt.tight_layout(pad=2)
plt.show()
