import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

df = pd.read_csv("/home/arthurscarpatto/VC/video-coding/results.csv") 
fig, axes = plt.subplots(2, 1, figsize=(15,5))
sb.barplot(data=df, x='v', y='psnr', hue='qsize', ax=axes[0]).set(title='VTM Test Run: Correlation Between Quantization Parameters and PSNR/BitRate', xlabel='')
sb.barplot(data=df, x='v', y='bit_rate', hue='qsize', ax=axes[1]).set(xlabel='Videos')
plt.show()