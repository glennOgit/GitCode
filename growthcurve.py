import pandas as pd
import numpy as np
from statistics import stdev 
from pylab import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys, getopt

ifile=''
ofile=''
try:
    myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -i input -o output" % sys.argv[0])
    sys.exit(2)

for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a

from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=['olivedrab','saddlebrown','darkorange','dodgerblue','darkgoldenrod','red','teal','forestgreen','purple','steelblue','orchid','gold','cadetblue'])
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams["axes.spines.right"] = False
mpl.rcParams["axes.spines.top"] = False
mpl.rcParams['xtick.major.size'] = 4
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['xtick.minor.size'] = 2
mpl.rcParams['xtick.minor.width'] = 2
mpl.rcParams['ytick.major.size'] = 4
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.minor.size'] = 2
mpl.rcParams['ytick.minor.width'] = 2
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 7
fig_size[1] = 8
mpl.rcParams["figure.figsize"] = fig_size

df = pd.read_csv(ifile, sep='\t',names=("name","titer1"))

print(df.name.str[-1])
df["dpi"] = df.name.str[-1]
df['name'] = df['name'].str[:-4]

nameSeries = df['name'].drop_duplicates(keep='first', inplace=False)

df["titer2"] = df.iloc[1::3,1]
df["titer3"] = df.iloc[2::3,1]
df["titer2"] = df["titer2"].shift(-1)
df["titer3"] = df["titer3"].shift(-2)
df = df.iloc[0::3]

df["mean"] = (df.titer1 + df.titer2 + df.titer3)/3
stdf = df.drop("dpi",axis=1)
stdf = df.drop("mean",axis=1)

df["stdevtn"] = stdf.std(axis=1)

print(df)
fig = plt.figure()
ax = fig.add_subplot(111)

for name in nameSeries:
	loopdf = df[df['name']==name]
	loopdf = loopdf.append(pd.Series([loopdf.iloc[0,0],1,str(0),1,1,1,0],index=["name","titer1","dpi","titer2","titer3","mean","stdevtn"]),ignore_index=True)
	loopdf = pd.concat([loopdf.iloc[[3],:], loopdf.drop(3, axis=0)], axis=0)
	loopdf=loopdf.rename(columns = {'mean':name})
	print(loopdf)
	print(loopdf.dtypes)
	line = ax.errorbar(loopdf["dpi"],loopdf[name],loopdf["stdevtn"],capsize=3,capthick=1.5,elinewidth=1.5)

plt.yscale('log')
plt.legend(frameon=False)
plt.xticks(np.arange(5),(1,2,3,4,5))
plt.xlabel('Days Post Transfection',fontsize=15)
plt.ylim((1, 1000000000))
plt.ylabel('PFU/ml',fontsize=15)
plt.tick_params(labelsize=13)
plt.show()
fig.savefig(ofile)
plt.close(fig)


