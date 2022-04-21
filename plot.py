import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

#设置画图字体
plt.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['axes.unicode_minus'] = False

#读取数据
##读取速度
V_CA = pd.read_csv('./data/VData-CA.csv', sep=';', index_col=0)
V_FSC = pd.read_csv('./data/VData-FSC.csv', sep=';',index_col=0)
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
V_CA_PR = V_CA.sub(V_CA['0'], axis='index') / V_CA * 100

##速度数据处理


#绘图
##绘制速度图
#plt.figure(figsize=(6, 4), facecolor='w')










