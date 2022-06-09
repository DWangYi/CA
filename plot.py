import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns

##读取数据
stdV_CA = pd.read_csv('Std_VData-CA.csv', index_col = 0)
stdV_FSC = pd.read_csv('Std_VData-FSC.csv', index_col = 0)


data = (stdV_CA-stdV_FSC)/stdV_CA

f, ax= plt.subplots(figsize = (10, 10))
sns.heatmap(data, cmap='RdBu', linewidths = 0.05, ax = ax)
plt.show()