"""Evaluate verdicts against simulated ground truth and sweep thresholds."""
import pandas as pd, numpy as np
from authenticate import authenticate
table = pd.read_csv("data/simulated_species_table.csv")
manifest = pd.read_csv("data/simulated_manifest.csv")
truth = pd.read_csv("data/simulated_truth.csv")
classes = ["AUTHENTIC", "ADULTERATED", "SUBSTITUTED"]

res = authenticate(table, manifest).merge(truth, on="sample")
res.to_csv("results/simulated/verdicts.csv", index=False)
cm = pd.crosstab(res["truth"], res["verdict"]).reindex(index=classes, columns=classes, fill_value=0)
cm.to_csv("results/simulated/confusion_matrix.csv")
acc = (res["truth"] == res["verdict"]).mean()
print("Confusion matrix (rows=truth, cols=prediction)\n", cm, f"\nAccuracy: {acc:.3f}")

is_fraud = res["truth"] != "AUTHENTIC"; pred_fraud = res["verdict"] != "AUTHENTIC"
sens = (is_fraud & pred_fraud).sum() / is_fraud.sum()
spec = (~is_fraud & ~pred_fraud).sum() / (~is_fraud).sum()
print(f"Fraud detection sensitivity: {sens:.3f}  specificity: {spec:.3f}")

rows = []
for nf in [0.0, 0.001, 0.005, 0.01, 0.02, 0.05]:
    for at in [0.01, 0.02, 0.05, 0.10]:
        r = authenticate(table, manifest, nf, at).merge(truth, on="sample")
        f = r["truth"] != "AUTHENTIC"; p = r["verdict"] != "AUTHENTIC"
        rows.append({"noise_floor": nf, "adulterant_threshold": at,
                     "accuracy": (r["truth"] == r["verdict"]).mean(),
                     "sensitivity": (f & p).sum() / f.sum(),
                     "specificity": (~f & ~p).sum() / (~f).sum()})
sweep = pd.DataFrame(rows); sweep.to_csv("results/simulated/threshold_sweep.csv", index=False)
print("\nThreshold sweep:\n", sweep.round(3).to_string(index=False))
