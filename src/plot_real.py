"""UNTESTED on real sequencing outputs."""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
t=pd.read_csv('results/real/species_table.csv')
p=t.pivot_table(index='sample',columns='species',values='reads',aggfunc='sum',fill_value=0)
p.div(p.sum(axis=1),axis=0).plot.bar(stacked=True,figsize=(10,5))
plt.ylabel('Relative read abundance (not biomass)')
plt.title('Real-data species assignments')
plt.legend(bbox_to_anchor=(1.01,1))
plt.tight_layout()
plt.savefig('results/real/fig1_composition.png',dpi=200)
