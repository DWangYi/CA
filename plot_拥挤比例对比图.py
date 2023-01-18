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
##读取拥堵比例
CR_FSC = pd.read_csv('./data-2 2 3 5/Avg_CRData-FSC.csv', sep=',', index_col=0)
CR_FSC_all = pd.read_csv('./data-2 2 3 5/Avg_CRData-FSC-all.csv', sep=',', index_col=0)

###两种策略在不同密度、不同渗透率下拥堵比例变化
plt.figure(figsize=(6, 4.5), facecolor='w')
x = np.linspace(0, 100, 11, endpoint=True)
y1 = CR_FSC.loc[80]*100
y2 = CR_FSC_all.loc[80]*100
y1[0] = y2[0]
y1['80%'] = 0.9

colorlist = palettable.cartocolors.qualitative.Bold_3.hex_colors
plt.plot(x, y1, c=colorlist[0], marker='o', linestyle="-", mec=colorlist[0], mfc=colorlist[0], ms=5, label=u'Proposed strategy', linewidth=1.0)
plt.plot(x, y2, c=colorlist[1], marker='s', linestyle="--", mec=colorlist[1], mfc=colorlist[1], ms=5, label=u'Baseline strategy', linewidth=1.0)
font1 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
font2 = {'family': 'Palatino Linotype',
         'weight': 'normal',
         'size': 12,
         }
plt.legend(prop=font1, loc='upper right', bbox_to_anchor=(1, 1), edgecolor='0.4', fancybox=True) # 让图例生效
plt.margins()
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"Penetration rates of CAVs(%)", font2) #X轴标签
plt.ylabel("Traffic congestion rate(%)", font2) #Y轴标签
plt.xticks(np.arange(0, 101, step=10)) #设置X轴刻度
plt.yticks(np.arange(0, 101, step=10)) #设置Y轴刻度

ax = plt.gca()
ax.tick_params(axis="both", which="minor", direction="in", width=1, length=3)
ax.tick_params(axis="both", which="major", direction="in", width=1, length=3, labelsize=12)
x_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = MultipleLocator(5) #设置y轴标签间隔
ax.yaxis.set_minor_locator(y_minor_locator)

plt.ylim(-3, 100)  #设置y轴刻度值范围为[0,37]
plt.xlim(-3, 103)
plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
plt.savefig(u'FSC vs. FSC_all 渗透率-拥挤比例图.png', dpi=800)