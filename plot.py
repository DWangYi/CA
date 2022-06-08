import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
format = "{0:.02f}".format

#设置画图字体
plt.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['axes.unicode_minus'] = False

#读取数据
##读取速度
V_CA = pd.read_csv('./data/VData-CA.csv', sep=';', index_col=0)
V_FSC = pd.read_csv('./data/VData-FSC.csv', sep=';', index_col=0)
##读取速度标准差
Std_CA = pd.read_csv('./data/Std_VData-CA.csv', sep=';', index_col=0)
Std_FSC = pd.read_csv('./data/Std_VData-FSC.csv', sep=';', index_col=0)
##读取流量
Flow_CA = pd.read_csv('./data/FlowData-CA.csv', sep=';', index_col=0)
Flow_FSC = pd.read_csv('./data/FlowData-FSC.csv', sep=';', index_col=0)
##读取油耗
NFR_CA = pd.read_csv('./data/NFRData-CA.csv', sep=';', index_col=0)
NFR_FSC = pd.read_csv('./data/NFRData-FSC.csv', sep=';', index_col=0)
##读取CO
CO_CA = pd.read_csv('./data/ECOData-CA.csv', sep=';', index_col=0)
CO_FSC = pd.read_csv('./data/ECOData-FSC.csv', sep=';', index_col=0)
##读取NO
NO_CA = pd.read_csv('./data/ENOData-CA.csv', sep=';', index_col=0)
NO_FSC = pd.read_csv('./data/ENOData-FSC.csv', sep=';', index_col=0)
##读取PM
PM_CA = pd.read_csv('./data/EPMData-CA.csv', sep=';', index_col=0)
PM_FSC = pd.read_csv('./data/EPMData-FSC.csv', sep=';', index_col=0)
##读取VOC
VOC_CA = pd.read_csv('./data/EVOCData-CA.csv', sep=';', index_col=0)
VOC_FSC = pd.read_csv('./data/EVOCData-FSC.csv', sep=';', index_col=0)

#数据处理
##速度数据处理
V_res1 = V_CA.sub(V_CA['0%'], axis='index')

##速度标准差数据处理
STD_res1 = (Std_FSC - Std_CA) / Std_CA
STD_FSC_res2 = Std_FSC.sub(Std_FSC['0%'], axis='index').iloc[:,1:].div(Std_FSC['0%'], axis='index')*-1
STD_CA_res2 = Std_CA.sub(Std_CA['0%'], axis='index').iloc[:,1:].div(Std_CA['0%'], axis='index')*-1

##油耗数据处理
NFR_res1 = (NFR_FSC - NFR_CA) / NFR_CA



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
#plt.ylim(0, 10) # 限定纵轴的范围
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Enstd(m/s)") #Y轴标签

###同一密度、不同渗透率情况下，两种策略速度标准差提升情况
plt.figure(figsize=(6, 4), facecolor='w')
x = STD_FSC_res2.columns.values
y1 = STD_FSC_res2.loc[60]
y2 = STD_CA_res2.loc[60]
plt.plot(x, y1, c='#E4392E', marker='o', mec='#E4392E', mfc='w', label=u'FSC')
plt.plot(x, y2, c='#3979F2', marker='^', mec='#3979F2', mfc='w', label=u'CA')
plt.legend() # 让图例生效
#plt.ylim(0, 10) # 限定纵轴的范围
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Performance Improvement(%)") #Y轴标签


##绘制油耗图
###不同密度、不同渗透率下油耗变化
plt.figure(figsize=(6, 4), facecolor='w')
x = NFR_FSC.columns.values
y1 = NFR_FSC.loc[20]
y2 = NFR_FSC.loc[40]
y3 = NFR_FSC.loc[60]
y4 = NFR_FSC.loc[80]
y5 = NFR_FSC.loc[100]
plt.plot(x, y1, c='#2986DB', marker='o', mec='#2986DB', mfc='w', label=u'20')
plt.plot(x, y2, c='#3F4756', marker='^', mec='#3F4756', mfc='w', label=u'40')
plt.plot(x, y3, c='#A3ABBD', marker='^', mec='#A3ABBD', mfc='w', label=u'60')
plt.plot(x, y4, c='#D25A7F', marker='^', mec='#D25A7F', mfc='w', label=u'80')
plt.plot(x, y5, c='#98224E', marker='^', mec='#98224E', mfc='w', label=u'100')
plt.legend() # 让图例生效
#plt.ylim(0, 10) # 限定纵轴的范围
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Percentage of AVs(%)") #X轴标签
plt.ylabel("Performance Improvement(%)") #Y轴标签




plt.show()







