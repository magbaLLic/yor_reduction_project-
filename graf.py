import pandas as pd, seaborn as sns, matplotlib.pyplot as plt

df = pd.read_csv('saat_sayim.csv', dtype={'saat':int})
df['oran'] = df['yo'] / (df['yo'] + df['yor']).replace({0:None})
df['gece'] = (df['saat'] < 6) | (df['saat'] >= 22)

sns.set_theme()
sns.lineplot(data=df, x='saat', y='oran', marker='o')
plt.title('"yo/yor" Ratio on An Hourly Basis')
plt.xlabel('Hour'); plt.ylabel('"yo" Ratio')
plt.xticks(range(0,24))
plt.tight_layout()
plt.savefig('ratio_plot.png', dpi=200)
plt.show()
