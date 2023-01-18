import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
import pandas as pd
from matplotlib.pyplot import MultipleLocator
import palettable
import seaborn as sn
#from skimage import transform
from scipy import interpolate
import numpy as np
format = "{0:.02f}".format

#设置画图字体
plt.rcParams['font.sans-serif'] = ['Palatino Linotype']
matplotlib.rcParams['axes.unicode_minus'] = False

#读取数据
##读取速度
#V_CA = pd.read_csv('./data/VData-CA.csv', sep=',', index_col=0)
V_FSC = pd.read_csv('./data-2 2 2.5 5/VData-FSC.csv', sep=',', index_col=0)
V_FSC_all = pd.read_csv('./data-2 2 2.5 5/VData-FSC-all.csv', sep=',', index_col=0)
##读取流量
#Flow_CA = pd.read_csv('./data/FlowData-CA.csv', sep=',', index_col=0)
Flow_FSC = pd.read_csv('./data-2 2 2.5 5/FlowData-FSC.csv', sep=',', index_col=0)

##绘制不同渗透率下密度-速度图
###不同渗透率情况下，密度-速度的变化情况
plt.figure(figsize=(6, 4), facecolor='w')
x = V_FSC.index.values
y1 = V_FSC['0%']
y2 = V_FSC['20%']
y3 = V_FSC['40%']
y4 = V_FSC['60%']
y5 = V_FSC['80%']
y6 = V_FSC['100%']
#colorlist = palettable.tableau.BlueRed_6.hex_colors
colorlist = palettable.scientific.diverging.Vik_6.hex_colors
plt.plot(x, y1, c=colorlist[0], marker='o', mec=colorlist[0], mfc='w', ms=5, label=u'PR=0%', linewidth=1.0)
plt.plot(x, y2, c=colorlist[1], marker='^', mec=colorlist[1], mfc='w', ms=5, label=u'PR=20%', linewidth=1.0)
plt.plot(x, y3, c=colorlist[2], marker='D', mec=colorlist[2], mfc='w', ms=5, label=u'PR=40%', linewidth=1.0)
plt.plot(x, y4, c=colorlist[3], marker='s', mec=colorlist[3], mfc='w', ms=5, label=u'PR=60%', linewidth=1.0)
plt.plot(x, y5, c=colorlist[4], marker='*', mec=colorlist[4], mfc='w', ms=5, label=u'PR=80%', linewidth=1.0)
plt.plot(x, y6, c=colorlist[5], marker='v', mec=colorlist[5], mfc='w', ms=5, label=u'PR=100%', linewidth=1.0)

font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
font2 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }

plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 0.95), edgecolor='0.4') # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Density(veh/km)", font2) #X轴标签
plt.ylabel("Velocity(m/s)", font2) #Y轴标签
plt.xticks(np.arange(0, 105, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 40, step=4)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator=MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator=MultipleLocator(2) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(0, 36)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC密度-速度图.png', dpi=600)

##绘制不同渗透率下密度-流量图
###不同渗透率情况下，密度-流量的变化情况
plt.figure(figsize=(6, 4), facecolor='w')
x = Flow_FSC.index.values
y1 = Flow_FSC['0%']
y2 = Flow_FSC['20%']
y3 = Flow_FSC['40%']
y4 = Flow_FSC['60%']
y5 = Flow_FSC['80%']
y6 = Flow_FSC['100%']
#colorlist = palettable.tableau.BlueRed_6.hex_colors
colorlist = palettable.scientific.diverging.Vik_6.hex_colors
plt.plot(x, y1, c=colorlist[0], marker='o', mec=colorlist[0], mfc='w', ms=5, label=u'PR=0%', linewidth=1.0)
plt.plot(x, y2, c=colorlist[1], marker='^', mec=colorlist[1], mfc='w', ms=5, label=u'PR=20%', linewidth=1.0)
plt.plot(x, y3, c=colorlist[2], marker='D', mec=colorlist[2], mfc='w', ms=5, label=u'PR=40%', linewidth=1.0)
plt.plot(x, y4, c=colorlist[3], marker='s', mec=colorlist[3], mfc='w', ms=5, label=u'PR=60%', linewidth=1.0)
plt.plot(x, y5, c=colorlist[4], marker='*', mec=colorlist[4], mfc='w', ms=5, label=u'PR=80%', linewidth=1.0)
plt.plot(x, y6, c=colorlist[5], marker='v', mec=colorlist[5], mfc='w', ms=5, label=u'PR=100%', linewidth=1.0)

plt.legend(prop=font1, edgecolor='0.4') # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Density(veh/km)", font2) #X轴标签
plt.ylabel("Flow(veh/h)", font2) #Y轴标签
plt.xticks(np.arange(0, 105, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 13001, step=1000)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator=MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator=MultipleLocator(500) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(0, 13000)  #设置y轴刻度值范围为[0,13000]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC密度-流量图.png', dpi=600)


###不同渗透率情况下，渗透率-速度的变化情况
plt.figure(figsize=(6, 4), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = V_FSC.loc[20]
y2 = V_FSC.loc[40]
y3 = V_FSC.loc[60]
y4 = V_FSC.loc[80]
y5 = V_FSC.loc[100]
#colorlist = palettable.tableau.BlueRed_6.hex_colors
colorlist = palettable.scientific.diverging.Vik_6.hex_colors
plt.plot(x, y1, c=colorlist[0], marker='o', mec=colorlist[0], mfc='w', ms=5, label=u'Density=20veh/km', linewidth=1.0)
plt.plot(x, y2, c=colorlist[1], marker='^', mec=colorlist[1], mfc='w', ms=5, label=u'Density=40veh/km', linewidth=1.0)
plt.plot(x, y3, c=colorlist[2], marker='D', mec=colorlist[2], mfc='w', ms=5, label=u'Density=60veh/km', linewidth=1.0)
plt.plot(x, y4, c=colorlist[3], marker='s', mec=colorlist[3], mfc='w', ms=5, label=u'Density=80veh/km', linewidth=1.0)
plt.plot(x, y5, c=colorlist[4], marker='*', mec=colorlist[4], mfc='w', ms=5, label=u'Density=100veh/km', linewidth=1.0)
#plt.plot(x, y6, c=colorlist[5], marker='v', mec=colorlist[5], mfc='w', ms=5, label=u'PR=100%', linewidth=1.0)

font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 10,
         }
font2 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }

plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(0.4, 1), edgecolor='0.4') # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Velocity(m/s)", font2) #Y轴标签
plt.xticks(np.arange(0, 105, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 40, step=4)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator=MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator=MultipleLocator(2) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(0, 36)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC渗透率-速度图.png', dpi=600)



###同一密度情况下，变异系数的对比变化情况
plt.figure(figsize=(6, 4), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = V_FSC.loc[40]
y2 = V_FSC_all.loc[40]
y3 = V_FSC.loc[60]
y4 = V_FSC_all.loc[60]
y5 = V_FSC.loc[80]
y6 = V_FSC_all.loc[80]
colorlist = palettable.cartocolors.qualitative.Bold_3.hex_colors
plt.plot(x, y1, c=colorlist[0], marker='o', linestyle="-", mec=colorlist[0], mfc=colorlist[0], ms=5, label=u'Proposed strategy(40veh/km)', linewidth=1.0)
plt.plot(x, y2, c=colorlist[0], marker='^', linestyle="--", mec=colorlist[0], mfc=colorlist[0], ms=5, label=u'Baseline strategy(40veh/km)', linewidth=1.0)
plt.plot(x, y3, c=colorlist[1], marker='D', linestyle="-", mec=colorlist[1], mfc=colorlist[1], ms=5, label=u'Proposed strategy(60veh/km)', linewidth=1.0)
plt.plot(x, y4, c=colorlist[1], marker='s', linestyle="--", mec=colorlist[1], mfc=colorlist[1], ms=5, label=u'Baseline strategy(60veh/km)', linewidth=1.0)
plt.plot(x, y5, c=colorlist[2], marker='*', linestyle="-", mec=colorlist[2], mfc=colorlist[2], ms=5, label=u'Proposed strategy(80veh/km)', linewidth=1.0)
plt.plot(x, y6, c=colorlist[2], marker='v', linestyle="--", mec=colorlist[2], mfc=colorlist[2], ms=5, label=u'Baseline strategy(80veh/km)', linewidth=1.0)
font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 10,
         }
font2 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(0.55, 1), edgecolor='0.4') # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Velocity(m/s)", font2) #Y轴标签
plt.xticks(np.arange(0, 101, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 40, step=4)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置x轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(2) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(0, 36)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC vs. FSC_all 渗透率-速度图.png', dpi=600)