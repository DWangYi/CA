import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
import pandas as pd
from matplotlib.pyplot import MultipleLocator
import seaborn as sn
#from skimage import transform
from scipy import interpolate
import numpy as np
format = "{0:.02f}".format

#设置画图字体
plt.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['axes.unicode_minus'] = False

#读取数据
##读取速度
V_CA = pd.read_csv('./data/VData-CA.csv', sep=',', index_col=0)
V_FSC = pd.read_csv('./data/VData-FSC.csv', sep=',', index_col=0)
##读取速度标准差
Std_CA = pd.read_csv('./data/Std_VData-CA.csv', sep=',', index_col=0)
Std_FSC = pd.read_csv('./data/Std_VData-FSC.csv', sep=',', index_col=0)
##读取流量
Flow_CA = pd.read_csv('./data/FlowData-CA.csv', sep=',', index_col=0)
Flow_FSC = pd.read_csv('./data/FlowData-FSC.csv', sep=',', index_col=0)
##读取油耗
NFR_CA = pd.read_csv('./data/NFRData-CA.csv', sep=',', index_col=0)
NFR_FSC = pd.read_csv('./data/NFRData-FSC.csv', sep=',', index_col=0)
##读取CO
CO_CA = pd.read_csv('./data/ECOData-CA.csv', sep=',', index_col=0)
CO_FSC = pd.read_csv('./data/ECOData-FSC.csv', sep=',', index_col=0)
##读取NO
NO_CA = pd.read_csv('./data/ENOData-CA.csv', sep=',', index_col=0)
NO_FSC = pd.read_csv('./data/ENOData-FSC.csv', sep=',', index_col=0)
##读取PM
PM_CA = pd.read_csv('./data/EPMData-CA.csv', sep=',', index_col=0)
PM_FSC = pd.read_csv('./data/EPMData-FSC.csv', sep=',', index_col=0)
##读取VOC
VOC_CA = pd.read_csv('./data/EVOCData-CA.csv', sep=',', index_col=0)
VOC_FSC = pd.read_csv('./data/EVOCData-FSC.csv', sep=',', index_col=0)

#数据处理
##速度数据处理
V_res1 = V_CA.sub(V_CA['0%'], axis='index')

##速度标准差数据处理
C0F_FSC = Std_FSC/V_FSC   #FSC变异系数
C0F_CA = Std_CA/V_CA      #CA变异系数
Std_res1 = (Std_FSC-Std_CA)/Std_CA    #FSC下降比例
Std_FSC_res2 = C0F_FSC.sub(C0F_FSC['0%'], axis='index').iloc[:,1:].div(C0F_FSC['0%'], axis='index')*-1
Std_CA_res2 = C0F_CA .sub(C0F_CA['0%'], axis='index').iloc[:,1:].div(C0F_CA['0%'], axis='index')*-1

##油耗数据处理
NFR_res1 = ((NFR_CA-NFR_FSC)/NFR_CA).iloc[:, 1:]*100   #油耗下降比例
NFR_FSC_res2 = NFR_FSC.sub(NFR_FSC['0%'], axis='index').iloc[:,1:].div(NFR_FSC['0%'], axis='index')*-1
NFR_CA_res2 = NFR_CA .sub(NFR_CA['0%'], axis='index').iloc[:,1:].div(NFR_CA['0%'], axis='index')*-1

##污染物排放数据处理
CO_res1 = ((CO_CA-CO_FSC)/CO_CA).iloc[:, 1:]*100   #CO2排放下降比例
NO_res1 = ((NO_CA-NO_FSC)/NO_CA).iloc[:, 1:]*100   #NOX排放下降比例
PM_res1 = ((PM_CA-PM_FSC)/PM_CA).iloc[:, 1:]*100   #PM排放下降比例
VOC_res1 = ((VOC_CA-VOC_FSC)/VOC_CA).iloc[:, 1:]*100   #VOC排放下降比例

#绘图
##绘制速度图
#plt.figure(figsize=(6, 4), facecolor='w')


##绘制速度标准差图
###同一密度、不同渗透率情况下，两种策略速度标准差的变化情况
plt.figure(figsize=(6, 4), facecolor='w')
x = Std_FSC.columns.values
y1 = Std_FSC.loc[60]
y2 = Std_CA.loc[60]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Enstd(m/s)") #Y轴标签
#plt.grid(b="True", axis="x")
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(1) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-0.5, max(y1.max(), y2.max())+0.5)


###同一密度、不同渗透率情况下，两种策略速度变异系数的变化情况
plt.figure(figsize=(6, 4), facecolor='w')
x = C0F_FSC.columns.values
y1 = C0F_FSC.loc[60]
y2 = C0F_CA.loc[60]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Coefficient of Variation") #Y轴标签
#plt.grid(b="True", axis="x")
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(0.1) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-0.05, max(y1.max(), y2.max())+0.1)


###同一密度、不同渗透率情况下，两种策略速度标准差提升情况
plt.figure(figsize=(6, 4), facecolor='w')
x = Std_FSC_res2.columns.values
y1 = Std_FSC_res2.loc[60]
y2 = Std_CA_res2.loc[60]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
#plt.ylim(0, 10) # 限定纵轴的范围
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Performance Improvement(%)") #Y轴标签
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(0.1) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-0.05, max(y1.max(), y2.max())+0.05)

##绘制油耗图
###FSC策略不同密度、不同渗透率下油耗变化
plt.figure(figsize=(6, 4), facecolor='w')
x = NFR_FSC.columns.values
y1 = NFR_FSC.loc[20]
y2 = NFR_FSC.loc[40]
y3 = NFR_FSC.loc[60]
y4 = NFR_FSC.loc[80]
y5 = NFR_FSC.loc[100]
plt.plot(x, y1, c='#2986DB', marker='o', mec='#2986DB', mfc='w', label=u'Density=20veh/km')
plt.plot(x, y2, c='#3F4756', marker='^', mec='#3F4756', mfc='w', label=u'N=Density=40veh/km')
plt.plot(x, y3, c='#A3ABBD', marker='D', mec='#A3ABBD', mfc='w', label=u'N=Density=60veh/km')
plt.plot(x, y4, c='#D25A7F', marker='s', mec='#D25A7F', mfc='w', label=u'Density=80veh/km')
plt.plot(x, y5, c='#98224E', marker='v', mec='#98224E', mfc='w', label=u'Density=100veh/km')
plt.legend() # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Fuel consumption(g/km)") #Y轴标签
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(100) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(0, 800)

###CA策略不同密度、不同渗透率下油耗变化
plt.figure(figsize=(6, 4), facecolor='w')
x = NFR_CA.columns.values
y1 = NFR_CA.loc[20]
y2 = NFR_CA.loc[40]
y3 = NFR_CA.loc[60]
y4 = NFR_CA.loc[80]
y5 = NFR_CA.loc[100]
plt.plot(x, y1, c='#2986DB', marker='o', mec='#2986DB', mfc='w', label=u'Density=20veh/km')
plt.plot(x, y2, c='#3F4756', marker='^', mec='#3F4756', mfc='w', label=u'N=Density=40veh/km')
plt.plot(x, y3, c='#A3ABBD', marker='D', mec='#A3ABBD', mfc='w', label=u'N=Density=60veh/km')
plt.plot(x, y4, c='#D25A7F', marker='s', mec='#D25A7F', mfc='w', label=u'Density=80veh/km')
plt.plot(x, y5, c='#98224E', marker='v', mec='#98224E', mfc='w', label=u'Density=100veh/km')
plt.legend() # 让图例生效
#plt.ylim(0, 10) # 限定纵轴的范围
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Fuel consumption(g/km)") #Y轴标签
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(100) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(0,800)


###密度40、不同渗透率下油耗提升比例
plt.figure(figsize=(6, 4), facecolor='w')
x = NFR_FSC_res2.columns.values
y1 = NFR_FSC_res2.loc[40]
y2 = NFR_CA_res2.loc[40]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
#plt.ylim(0, 10) # 限定纵轴的范围
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Performance Improvement(%)") #Y轴标签
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(0.1) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-0.05, max(y1.max(), y2.max())+0.05)

###密度60、不同渗透率下油耗提升比例
plt.figure(figsize=(6, 4), facecolor='w')
x = NFR_FSC_res2.columns.values
y1 = NFR_FSC_res2.loc[60]
y2 = NFR_CA_res2.loc[60]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Performance Improvement(%)") #Y轴标签
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(0.1) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-0.05, max(y1.max(), y2.max())+0.05)

###密度80、不同渗透率下油耗提升比例
plt.figure(figsize=(6, 4), facecolor='w')
x = NFR_FSC_res2.columns.values
y1 = NFR_FSC_res2.loc[80]
y2 = NFR_CA_res2.loc[80]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)")  #X轴标签
plt.ylabel("Performance Improvement(%)")  #Y轴标签
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(0.1) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-0.05, max(y1.max(), y2.max())+0.05)

###密度100、不同渗透率下油耗提升比例
plt.figure(figsize=(6, 4), facecolor='w')
x = NFR_FSC_res2.columns.values
y1 = NFR_FSC_res2.loc[100]
y2 = NFR_CA_res2.loc[100]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)")  #X轴标签
plt.ylabel("Performance Improvement(%)")  #Y轴标签
plt.grid(b="True", axis="y")
y_major_locator=MultipleLocator(0.1) #设置y轴标签间隔
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-0.05, max(y1.max(), y2.max())+0.05)

###两种策略油耗对比热力图
plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,0:100:11j]
z = np.flip(np.array(NFR_FSC),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=160, vmax=800)
plt.colorbar(c, label='Fuel consumption(g/km)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签

plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,0:100:11j]
z = np.flip(np.array(NFR_CA),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=160, vmax=800)
plt.colorbar(c, label='Fuel consumption(g/km)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签

plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,10:100:10j]
z = np.flip(np.array(NFR_res1),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.coolwarm, vmin=-35, vmax=35)
plt.colorbar(c, label='Performance Improvement(%)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签




##绘制污染物排放图
###两种策略CO排放对比热力图
plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,0:100:11j]
z = np.flip(np.array(CO_FSC),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=100, vmax=1500)
plt.colorbar(c, label='CO2 Emissions(g/km)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签

plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,0:100:11j]
z = np.flip(np.array(CO_CA),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=100, vmax=1500)
plt.colorbar(c, label='CO2 Emissions(g/km)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签

plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,10:100:10j]
z = np.flip(np.array(CO_res1),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.coolwarm, vmin=-z1.max(), vmax=z1.max())
plt.colorbar(c, label='Performance Improvement(%)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签

###两种策略NO排放对比热力图
plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,10:100:10j]
z = np.flip(np.array(NO_res1),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.coolwarm, vmin=-z1.max(), vmax=z1.max())
plt.colorbar(c, label='Performance Improvement(%)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签

###两种策略PM排放对比热力图
plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,10:100:10j]
z = np.flip(np.array(PM_res1),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.coolwarm, vmin=-z1.max(), vmax=z1.max())
plt.colorbar(c, label='Performance Improvement(%)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签

###两种策略VOC排放对比热力图
plt.figure(figsize=(5, 5), facecolor='w')
y,x = np.ogrid[10:100:10j,10:100:10j]
z = np.flip(np.array(VOC_res1),axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0,100,100)
y1 = np.linspace(0,100,100)
z1 = func(x1,y1)
c = ax.imshow(z1, extent=extent, cmap=cm.coolwarm, vmin=-z1.max(), vmax=z1.max())
plt.colorbar(c, label='Performance Improvement(%)')
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Density(veh/km)") #Y轴标签




plt.show()







