import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
table = pd.read_csv("data/simulated_species_table.csv")
res = pd.read_csv("results/verdicts.csv")
cm = pd.read_csv("results/confusion_matrix.csv", index_col=0)

piv = table.pivot_table(index="sample", columns="species", values="reads", aggfunc="sum", fill_value=0)
piv = piv.div(piv.sum(axis=1), axis=0).loc[res["sample"]]
fig, ax = plt.subplots(figsize=(12, 4.5))
piv.plot(kind="bar", stacked=True, ax=ax, colormap="tab20", width=0.85)
ax.set_ylabel("Relative read abundance"); ax.set_xlabel("Sample (turmeric S01-S10, saffron S11-S20, black pepper S21-S30)")
ax.set_title("Fig. 1  Species composition of simulated spice samples (tick colour = verdict)")
colors = {"AUTHENTIC": "green", "ADULTERATED": "darkorange", "SUBSTITUTED": "red"}
for tick, v in zip(ax.get_xticklabels(), res["verdict"]): tick.set_color(colors[v])
ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8, title="Species")
plt.tight_layout(); plt.savefig("results/fig1_composition.png", dpi=200); plt.close()

fig, ax = plt.subplots(figsize=(4.8, 4))
ax.imshow(cm.values, cmap="Blues")
ax.set_xticks(range(3)); ax.set_xticklabels(cm.columns, rotation=30, ha="right")
ax.set_yticks(range(3)); ax.set_yticklabels(cm.index)
for i in range(3):
    for j in range(3): ax.text(j, i, cm.values[i, j], ha="center", va="center")
ax.set_xlabel("Predicted"); ax.set_ylabel("Truth"); ax.set_title("Fig. 2  Verdict vs ground truth")
plt.tight_layout(); plt.savefig("results/fig2_confusion.png", dpi=200); plt.close()
print("figures saved")
