"""Limit-of-detection experiment on SIMULATED data.

Spike a filler (Zea mays) into authentic turmeric at known fractions, with
realistic background noise, and measure how often the pipeline flags it.
Also measures the false-positive rate at 0% spike.
"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from authenticate import authenticate

rng = np.random.default_rng(7)
LABEL, FILLER = "Curcuma longa", "Zea mays"
BG = ["Oryza sativa", "Glycine max", "Capsicum annuum", "Allium sativum", "Solanum lycopersicum"]
SPIKES = [0, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20]
REPS = 100

def make(spike, rep):
    depth = int(rng.lognormal(np.log(20000), 0.3))
    noise = rng.uniform(0.0005, 0.02)          # up to 2% background / cross-talk
    bg = rng.choice(BG, 2, replace=False)
    props = {LABEL: 1 - spike - noise, FILLER: spike}
    for s in bg: props[s] = noise / 2
    sp = list(props); p = np.array([max(props[s], 0) for s in sp]); p /= p.sum()
    c = rng.multinomial(depth, p)
    return [(f"sp{spike}_r{rep}", s, int(x)) for s, x in zip(sp, c) if x > 0]

rows = [r for sp in SPIKES for rep in range(REPS) for r in make(sp, rep)]
table = pd.DataFrame(rows, columns=["sample", "species", "reads"])
manifest = pd.DataFrame({"sample": table["sample"].unique()})
manifest["product"] = "turmeric"; manifest["label_species"] = LABEL
manifest["spike"] = manifest["sample"].str.extract(r"sp([0-9.]+)_")[0].astype(float)

out = []
for nf in [0.001, 0.005, 0.01, 0.02]:
    res = authenticate(table, manifest[["sample", "product", "label_species"]],
                       noise_floor=nf, adulterant_threshold=0.0001).merge(manifest[["sample", "spike"]], on="sample")
    # flag only if the FILLER specifically is reported (not just any background taxon)
    res["filler_called"] = res["other_species"].str.contains(FILLER)
    g = res.groupby("spike")["filler_called"].mean().rename(nf)
    out.append(g)
lod = pd.concat(out, axis=1); lod.index.name = "spike_fraction"
lod.columns = [f"noise_floor={c}" for c in lod.columns]
lod.to_csv("results/lod_detection_rate.csv"); print(lod.round(2).to_string())

fig, ax = plt.subplots(figsize=(6.5, 4))
x = [s * 100 if s > 0 else 0.1 for s in lod.index]
for c in lod.columns: ax.plot(x, lod[c], marker="o", label=c)
ax.set_xscale("log"); ax.set_xlabel("Filler spiked in (% of reads; 0% plotted at 0.1)")
ax.set_ylabel("Fraction of replicates where filler is called")
ax.axhline(0.95, ls="--", c="grey", lw=0.8); ax.legend(fontsize=8)
ax.set_title("Fig. 3  Detection rate vs adulteration level (n=100 per level)")
plt.tight_layout(); plt.savefig("results/fig3_limit_of_detection.png", dpi=200)
