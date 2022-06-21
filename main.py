from BDrate import BD_RATE
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Opening JSON config file
file_cfg = open('configs.json')
configs = json.load(file_cfg)
file_cfg.close()

# Initializing some data structures
df = pd.read_csv('results.csv')
avg_diffs = list()
labels = list()

for v in configs['videos']:
    # Calculating the BD-Rate
    videodf = df[df['v'] == v]
    r1 = videodf['bit_rate'].iloc[:4]
    r2 = videodf['bit_rate'].iloc[4:]
    psnr1 = videodf['psnr'].iloc[:4]
    psnr2 = videodf['psnr'].iloc[4:]
    avg_diffs.append(BD_RATE(r1, psnr1, r2, psnr2))
    
    # Getting the names of the videos, without the resolution
    div_index = v.index("_")
    labels.append(v[:div_index])

#Plotting the graph
plt.figure(figsize=(15,5))
sns.set_style('dark')
sns.lineplot(y=avg_diffs, x=labels, palette=['b']).set(ylabel='Average difference', title='BD-Rate: Average Difference Between VTM and VVenC for Four Sequences', xlabel='Sequences')
plt.show()
