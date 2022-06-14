import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

with open("/home/arthurscarpatto/VC/BD-Rate/results.csv", 'r') as csv_file:
    df = pd.DataFrame(csv_file.read())
    csv_file.close()

sb.barplot(data=df, x='v', y='bdrate', hue='qp')
plt.show()