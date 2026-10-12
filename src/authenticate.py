"""Compare detected species in each sample with its label and issue a verdict.

Input : species table (sample, species, reads) + manifest (sample, product, label_species)
Output: per-sample verdict CSV

Verdicts
  AUTHENTIC    label species >= (1 - adulterant_threshold) of reads after noise filtering
  ADULTERATED  label species present, but other taxa exceed adulterant_threshold
  SUBSTITUTED  label species below substitution_threshold
"""
import argparse, pandas as pd

def authenticate(table, manifest, noise_floor=0.01, adulterant_threshold=0.05, substitution_threshold=0.05):
    for value in (noise_floor, adulterant_threshold, substitution_threshold):
        if not 0 <= value <= 1:
            raise ValueError("Thresholds must be between zero and one")
    if table["reads"].isna().any() or (table["reads"] < 0).any():
        raise ValueError("Read counts must be nonnegative and finite")
    table = table.groupby(["sample", "species"], as_index=False)["reads"].sum()
    out = []
    for _, m in manifest.iterrows():
        t = table[table["sample"] == m["sample"]].copy()
        total = t["reads"].sum()
        t["rel"] = t["reads"] / total
        t = t[t["rel"] >= noise_floor]            # drop taxa below noise floor
        t["rel"] = t["reads"] / t["reads"].sum()  # renormalise
        label_frac = t.loc[t["species"] == m["label_species"], "rel"].sum()
        others = t[t["species"] != m["label_species"]].sort_values("rel", ascending=False)
        if total <= 0 or t.empty or (t["species"] == "Unassigned").any():
            verdict = "INCONCLUSIVE"
        elif label_frac < substitution_threshold:
            verdict = "SUBSTITUTED"
        elif label_frac >= 1 - adulterant_threshold:
            verdict = "AUTHENTIC"
        else:
            verdict = "ADULTERATED"
        out.append({
            "sample": m["sample"], "product": m["product"], "label_species": m["label_species"],
            "label_fraction": round(label_frac, 4), "verdict": verdict,
            "other_species": "; ".join(f"{r.species} ({r.rel:.1%})" for r in others.itertuples()),
            "total_reads": int(total),
        })
    return pd.DataFrame(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True); ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--noise-floor", type=float, default=0.01)
    ap.add_argument("--adulterant-threshold", type=float, default=0.05)
    ap.add_argument("--substitution-threshold", type=float, default=0.05)
    a = ap.parse_args()
    res = authenticate(pd.read_csv(a.table), pd.read_csv(a.manifest),
                       a.noise_floor, a.adulterant_threshold, a.substitution_threshold)
    res.to_csv(a.out, index=False)
    print(res["verdict"].value_counts().to_string())
