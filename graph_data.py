import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import json

file_cfg = open('configs.json')
configs = json.load(file_cfg)

df = pd.read_csv("/home/arthurscarpatto/VC/video-coding/results.csv") 
vtmdf = df.iloc[:16, :]
vvencdf = df.iloc[16:, :]
fig, axes = plt.subplots(2, 1, figsize=(15,5))

if configs['encoder'] == 'VTM':
    sb.barplot(data=vtmdf, x='v', y='psnr', hue='qsize', ax=axes[0]).set(title='VTM Test Run: Correlation Between Quantization Parameters and PSNR/BitRate', xlabel='')
    sb.barplot(data=vtmdf, x='v', y='bit_rate', hue='qsize', ax=axes[1]).set(xlabel='Videos')
elif configs['encoder'] == "vvenc":
    sb.barplot(data=vvencdf, x='v', y='psnr', hue='qsize', ax=axes[0]).set(title='VVenC Test Run: Correlation Between Quantization Parameters and PSNR/BitRate', xlabel='')
    sb.barplot(data=vvencdf, x='v', y='bit_rate', hue='qsize', ax=axes[1]).set(xlabel='Videos')

plt.show()