from BDrate import BD_RATE
import pandas as pd

df = pd.read_csv('results.csv')
r1 = df['bit_rate'].iloc[:16]
r2 = df['bit_rate'].iloc[16:]
psnr1 = df['psnr'].iloc[:16]
psnr2 = df['psnr'].iloc[16:]

avg_diff = BD_RATE(r1, psnr1, r2, psnr2)
print(avg_diff)