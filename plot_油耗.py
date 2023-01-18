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
##读取油耗
NFR_FSC_all = pd.read_csv('./data-2 2 2.5 5/NFRData-FSC-all.csv', sep=',', index_col=0)
NFR_FSC = pd.read_csv('./data-2 2 2.5 5/NFRData-FSC.csv', sep=',', index_col=0)
##读取CO
CO_FSC_all = pd.read_csv('./data-2 2 2.5 5/ECOData-FSC-all.csv', sep=',', index_col=0)
CO_FSC = pd.read_csv('./data-2 2 2.5 5/ECOData-FSC.csv', sep=',', index_col=0)
##读取NO
NO_FSC_all = pd.read_csv('./data-2 2 2.5 5/ENOData-FSC-all.csv', sep=',', index_col=0)
NO_FSC = pd.read_csv('./data-2 2 2.5 5/ENOData-FSC.csv', sep=',', index_col=0)
##读取PM
PM_FSC_all = pd.read_csv('./data-2 2 2.5 5/EPMData-FSC-all.csv', sep=',', index_col=0)
PM_FSC = pd.read_csv('./data-2 2 2.5 5/EPMData-FSC.csv', sep=',', index_col=0)
##读取VOC
VOC_FSC_all = pd.read_csv('./data-2 2 2.5 5/EVOCData-FSC-all.csv', sep=',', index_col=0)
VOC_FSC = pd.read_csv('./data-2 2 2.5 5/EVOCData-FSC.csv', sep=',', index_col=0)

#数据处理
##油耗数据处理
NFR_res1 = ((NFR_FSC_all-NFR_FSC)/NFR_FSC_all).iloc[:, 1:]*100   #油耗下降比例
NFR_FSC_res2 = NFR_FSC.sub(NFR_FSC['0%'], axis='index').iloc[:,1:].div(NFR_FSC['0%'], axis='index')*-1*100
NFR_FSC_all_res2 = NFR_FSC_all.sub(NFR_FSC_all['0%'], axis='index').iloc[:,1:].div(NFR_FSC_all['0%'], axis='index')*-1*100
##污染物排放数据处理
CO_res1 = ((CO_FSC_all-CO_FSC)/CO_FSC_all).iloc[:, 1:]*100   #CO2排放下降比例
NO_res1 = ((NO_FSC_all-NO_FSC)/NO_FSC_all).iloc[:, 1:]*100   #NOX排放下降比例
PM_res1 = ((PM_FSC_all-PM_FSC)/PM_FSC_all).iloc[:, 1:]*100   #PM排放下降比例
VOC_res1 = ((VOC_FSC_all-VOC_FSC)/VOC_FSC_all).iloc[:, 1:]*100   #VOC排放下降比例

#绘图
##绘制油耗图
###FSC策略不同密度、不同渗透率下油耗变化
plt.figure(figsize=(6, 4), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = NFR_FSC.loc[20]
y2 = NFR_FSC.loc[40]
y3 = NFR_FSC.loc[60]
y4 = NFR_FSC.loc[80]
y5 = NFR_FSC.loc[100]
colorlist = palettable.scientific.diverging.Vik_6.hex_colors
plt.plot(x, y1, c=colorlist[0], marker='o', mec=colorlist[0], mfc='w', ms=5, label=u'Density=20veh/km', linewidth=1.0)
plt.plot(x, y2, c=colorlist[1], marker='^', mec=colorlist[1], mfc='w', ms=5, label=u'Density=40veh/km', linewidth=1.0)
plt.plot(x, y3, c=colorlist[2], marker='D', mec=colorlist[2], mfc='w', ms=5, label=u'Density=60veh/km', linewidth=1.0)
plt.plot(x, y4, c=colorlist[3], marker='s', mec=colorlist[3], mfc='w', ms=5, label=u'Density=80veh/km', linewidth=1.0)
plt.plot(x, y5, c=colorlist[4], marker='v', mec=colorlist[4], mfc='w', ms=5, label=u'Density=100veh/km', linewidth=1.0)
font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
font2 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1), edgecolor='0.4') # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Fuel consumption(g/km)", font2) #Y轴标签
plt.xticks(np.arange(0, 101, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 610, step=100)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(50) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(0, 600)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC渗透率-油耗图.png', dpi=600)



# #本文模型油耗热力图
# plt.figure(figsize=(6, 4), facecolor='w')
# y, x = np.ogrid[5:100:20j, 0:100:11j]
# z = np.flip(np.array(NFR_FSC), axis=0)
# extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
# ax = plt.subplot(111)
# func = interpolate.interp2d(x, y, z, kind='cubic')
# x1 = np.linspace(0, 100, 100)
# y1 = np.linspace(0, 100, 100)
# z1 = func(x1, y1)
# font1 = {'family': 'Palatino Linotype',
#          'weight': 'normal',
#          'size': 12,
#          }
# c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=100, vmax=600)
# plt.xticks(np.arange(0, 102, step=10)) #设置X轴刻度
# plt.yticks(np.arange(0, 102, step=10)) #设置Y轴刻度
# ax = plt.gca()
# ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
# cbar = plt.colorbar(c)
# cbar.set_label('Fuel consumption(g/km)', fontdict=font1)
# cbar.set_ticks(np.arange(100, 605, step=100))
# cbar.ax.tick_params(labelsize='12')
# plt.subplots_adjust(bottom=0.15)
# plt.xlabel(u"Penetration rates of CAVs(%)", font1)  #X轴标签
# plt.ylabel("Density(veh/km)", font1) #Y轴标签
# plt.savefig(u'FSC渗透率-密度-油耗-热力图.png', dpi=600)

##同一密度情况下，不同模型油耗的对比变化情况
# plt.figure(figsize=(6, 4), facecolor='w')
# x = NFR_FSC.columns.values
# y1 = NFR_FSC.loc[80]
# y2 = NFR_FSC_all.loc[80]
# y1[0] = y2[0]
# y3 = y1.sub(y1.loc['0%'], axis='index').div(y1.loc['0%'], axis='index')*-1
# y4 = y2.sub(y1.loc['0%'], axis='index').div(y1.loc['0%'], axis='index')*-1
# colorlist = palettable.cartocolors.qualitative.Bold_3.hex_colors
# plt.plot(x, y1, c=colorlist[0], marker='o', linestyle="-", mec=colorlist[0], mfc=colorlist[0], ms=5, label=u'Proposed model', linewidth=1.0)
# plt.plot(x, y2, c=colorlist[1], marker='^', linestyle="--", mec=colorlist[1], mfc=colorlist[1], ms=5, label=u'Baseline model', linewidth=1.0)
# font1 = {'family': 'Palatino Linotype',
#          'weight': 'normal',
#          'size': 12,
#          }
# font2 = {'family': 'Palatino Linotype',
#          'weight': 'normal',
#          'size': 12,
#          }
# plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1)) # 让图例生效
# plt.margins()
# plt.subplots_adjust(bottom=0.15)
# plt.xlabel(u"Percentage of CAVs(%)", font2) #X轴标签
# plt.ylabel("Fuel consumption(g/km)", font2) #Y轴标签
# plt.xticks(np.arange(0, 10.05, step=1)) #设置X轴刻度
# plt.yticks(np.arange(100, 510, step=50)) #设置Y轴刻度
#
# ax = plt.gca()
# ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
# ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
# x_minor_locator = MultipleLocator(0.5) #设置y轴标签间隔
# ax.xaxis.set_minor_locator(x_minor_locator)
# y_minor_locator = MultipleLocator(25) #设置y轴标签间隔
# ax.yaxis.set_minor_locator(y_minor_locator)
#
# plt.ylim(100, 500)  #设置y轴刻度值范围为[0,37]
# plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
# plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
# plt.savefig(u'FSC vs. FSC_all 渗透率-油耗图-80密度.png', dpi=600)


##同一密度情况下，不同模型油耗的对比变化情况
plt.figure(figsize=(6, 4), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = NFR_FSC.loc[40]
y2 = NFR_FSC_all.loc[40]
y3 = NFR_FSC.loc[60]
y4 = NFR_FSC_all.loc[60]
y5 = NFR_FSC.loc[80]
y6 = NFR_FSC_all.loc[80]
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
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1), edgecolor='0.4') # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Fuel consumption(g/km)", font2) #Y轴标签
plt.xticks(np.arange(0, 101, step=10)) #设置X轴刻度
plt.yticks(np.arange(150, 510, step=50)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(25) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(150, 500)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC vs. FSC_all 渗透率-油耗图.png', dpi=600)



plt.show()







