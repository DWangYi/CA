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
import palettable
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
CO_res1 = ((CO_FSC_all-CO_FSC)/CO_FSC_all)*100   #CO2排放下降比例
NO_res1 = ((NO_FSC_all-NO_FSC)/NO_FSC_all).iloc[:, 1:]*100   #NOX排放下降比例
PM_res1 = ((PM_FSC_all-PM_FSC)/PM_FSC_all).iloc[:, 1:]*100   #PM排放下降比例
VOC_res1 = ((VOC_FSC_all-VOC_FSC)/VOC_FSC_all).iloc[:, 1:]*100   #VOC排放下降比例

#绘图
##本文模型排放热力图
###CO排放热力图
plt.figure(figsize=(6, 4), facecolor='w')
y, x = np.ogrid[5:100:20j, 0:100:11j]
z = np.flip(np.array(CO_FSC), axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0, 100, 100)
y1 = np.linspace(0, 100, 100)
z1 = func(x1, y1)
font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=0, vmax=600)
plt.xticks(np.arange(0, 102, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 102, step=10)) #设置Y轴刻度
ax = plt.gca()
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
cbar = plt.colorbar(c)
cbar.set_label('Emission of CO$_{2}$(g/km)', fontdict=font1)
cbar.set_ticks(np.arange(0, 605, step=100))
cbar.ax.tick_params(labelsize='12')
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font1)  #X轴标签
plt.ylabel("Density(veh/km)", font1) #Y轴标签
plt.savefig(u'FSC渗透率-密度-CO-热力图.png', dpi=800)

###NO排放热力图
plt.figure(figsize=(6, 4), facecolor='w')
y, x = np.ogrid[5:100:20j, 0:100:11j]
z = np.flip(np.array(NO_FSC*1000), axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0, 100, 100)
y1 = np.linspace(0, 100, 100)
z1 = func(x1, y1)
font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=0, vmax=350)
plt.xticks(np.arange(0, 102, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 102, step=10)) #设置Y轴刻度
ax = plt.gca()
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
cbar = plt.colorbar(c)
cbar.set_label('Emission of NOx(mg/km)', fontdict=font1)
cbar.set_ticks(np.arange(0, 355, step=50))
cbar.ax.tick_params(labelsize='12')
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font1)  #X轴标签
plt.ylabel("Density(veh/km)", font1) #Y轴标签
plt.savefig(u'FSC渗透率-密度-NOx-热力图.png', dpi=800)

###PM排放热力图
plt.figure(figsize=(6, 4), facecolor='w')
y, x = np.ogrid[5:100:20j, 0:100:11j]
z = np.flip(np.array(PM_FSC*1000), axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0, 100, 100)
y1 = np.linspace(0, 100, 100)
z1 = func(x1, y1)
font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=0, vmax=25)
plt.xticks(np.arange(0, 102, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 102, step=10)) #设置Y轴刻度
ax = plt.gca()
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
cbar = plt.colorbar(c)
cbar.set_label('Emission of PM(mg/km)', fontdict=font1)
cbar.set_ticks(np.arange(0, 26, step=5))
cbar.ax.tick_params(labelsize='12')
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font1)  #X轴标签
plt.ylabel("Density(veh/km)", font1) #Y轴标签
plt.savefig(u'FSC渗透率-密度-PM-热力图.png', dpi=800)

###VOC排放热力图
plt.figure(figsize=(6, 4), facecolor='w')
y, x = np.ogrid[5:100:20j, 0:100:11j]
z = np.flip(np.array(VOC_FSC*1000), axis=0)
extent = [np.min(x),np.max(x),np.min(0),np.max(y)]
ax = plt.subplot(111)
func = interpolate.interp2d(x, y, z, kind='cubic')
x1 = np.linspace(0, 100, 100)
y1 = np.linspace(0, 100, 100)
z1 = func(x1, y1)
font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=0, vmax=300)
plt.xticks(np.arange(0, 102, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 102, step=10)) #设置Y轴刻度
ax = plt.gca()
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
cbar = plt.colorbar(c)
cbar.set_label('Emission of VOC(mg/km)', fontdict=font1)
cbar.set_ticks(np.arange(0, 305, step=50))
cbar.ax.tick_params(labelsize='12')
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font1)  #X轴标签
plt.ylabel("Density(veh/km)", font1) #Y轴标签
plt.savefig(u'FSC渗透率-密度-VOC-热力图.png', dpi=800)


# ###两种策略CO排放对比图
# plt.figure(figsize=(6, 4), facecolor='w')
# y, x = np.ogrid[5:100:20j, 0:100:11j]
# z = np.flip(np.array(CO_res1), axis=0)
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
# c = ax.imshow(z1, extent=extent, cmap=cm.rainbow, vmin=0, vmax=100)
# plt.xticks(np.arange(0, 102, step=10)) #设置X轴刻度
# plt.yticks(np.arange(0, 102, step=10)) #设置Y轴刻度
# ax = plt.gca()
# ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
# cbar = plt.colorbar(c)
# cbar.set_label('Performance reduction(%)', fontdict=font1)
# cbar.set_ticks(np.arange(0, 101, step=20))
# cbar.ax.tick_params(labelsize='12')
# plt.subplots_adjust(bottom=0.15)
# plt.xlabel(u"Percentage of CAVs(%)", font1)  #X轴标签
# plt.ylabel("Density(veh/km)", font1) #Y轴标签
#plt.savefig(u'FSC vs. FSC_all 渗透率-密度-VOC-热力图.png', dpi=600)



###两种策略在不同密度、不同渗透率下CO排放变化
plt.figure(figsize=(6, 5), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = CO_FSC.loc[40]
y2 = CO_FSC_all.loc[40]
y3 = CO_FSC.loc[60]
y4 = CO_FSC_all.loc[60]
y5 = CO_FSC.loc[80]
y6 = CO_FSC_all.loc[80]
colorlist = palettable.cartocolors.qualitative.Bold_3.hex_colors

plt.plot(x, y1, c=colorlist[0], marker='o', linestyle="-", mec=colorlist[0], mfc=colorlist[0], ms=5, label=u'Proposed strategyl(40veh/km)', linewidth=1.0)
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
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1)) # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Emission of CO$_{2}$(g/km)", font2) #Y轴标签
plt.xticks(np.arange(0, 105, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 605, step=100)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(50) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(000, 600)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC vs. FSC_all 渗透率-CO图.png', dpi=800)

###两种策略在不同密度、不同渗透率下NO排放变化
plt.figure(figsize=(6, 5), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = NO_FSC.loc[40]*1000
y2 = NO_FSC_all.loc[40]*1000
y3 = NO_FSC.loc[60]*1000
y4 = NO_FSC_all.loc[60]*1000
y5 = NO_FSC.loc[80]*1000
y6 = NO_FSC_all.loc[80]*1000
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
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1)) # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Emission of NO$_{x}$(mg/km)", font2) #Y轴标签
plt.xticks(np.arange(0, 105, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 405, step=50)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(25) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(-10, 400)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC vs. FSC_all 渗透率-NO图.png', dpi=800)

###两种策略在不同密度、不同渗透率下PM排放变化
plt.figure(figsize=(6, 5), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = PM_FSC.loc[40]*1000
y2 = PM_FSC_all.loc[40]*1000
y3 = PM_FSC.loc[60]*1000
y4 = PM_FSC_all.loc[60]*1000
y5 = PM_FSC.loc[80]*1000
y6 = PM_FSC_all.loc[80]*1000
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
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1)) # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Emission of PM(mg/km)", font2) #Y轴标签
plt.xticks(np.arange(0, 105, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 33, step=4)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(2) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(-1, 32)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC vs. FSC_all 渗透率-PM图.png', dpi=800)

##两种策略在不同密度、不同渗透率下VOC排放变化
plt.figure(figsize=(6, 5), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = VOC_FSC.loc[40]*1000
y2 = VOC_FSC_all.loc[40]*1000
y3 = VOC_FSC.loc[60]*1000
y4 = VOC_FSC_all.loc[60]*1000
y5 = VOC_FSC.loc[80]*1000
y6 = VOC_FSC_all.loc[80]*1000
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
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1)) # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Emission of VOC(mg/km)", font2) #Y轴标签
plt.xticks(np.arange(0, 105, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 251, step=50)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(25) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(0, 250)  #设置y轴刻度值范围为[0,37]
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC vs. FSC_all 渗透率-VOC图.png', dpi=800)


plt.show()







