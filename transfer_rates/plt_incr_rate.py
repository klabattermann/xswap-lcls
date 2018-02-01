#!/usr/bin/env python3
#
# plot some stats from the file transfer statistics
#

import sys
import pandas as pd
import matplotlib.pyplot as plt


fn = sys.argv[1]

d = pd.read_csv(fn)
d.info()

d.frate /= pow(2,20)
d.fsize /= pow(2,30)

cut_ana = (d.fsize < 200) & (d.ffbtrans == 0)
cut_ffb = (d.fsize < 200) & (d.ffbtrans == 1)


fig = plt.figure(figsize=(10,10))

for n,cut in enumerate((cut_ana, cut_ffb)):    
    ax = fig.add_subplot(2,2,2*n+1)
    
    d.loc[ cut ].frate.hist(bins=200)
    plt.xlabel("rate [MiB/s]")
    plt.ylabel("counts")
    ax.set_yscale("log")
    if n == 0:
        ax.set_title("ffb -> ana transfers", loc='left')
    else:
        ax.set_title("dss -> ffb transfers", loc='left')
                
    ax = fig.add_subplot(2,2,2*n+2)
    d.loc[ cut ].fsize.hist(bins=200)
    plt.xlabel("file size [GiB]")
    ax.set_yscale("log")

plt.tight_layout()
plt.suptitle("Incremenatal transfer rates", y=1)
plt.show()
