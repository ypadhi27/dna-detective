"""Simulate ITS2 metabarcoding species tables for spice authentication.

SYNTHETIC DATA, for pipeline validation only. Ground truth is written to a
separate file so the authentication step never sees it.
"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)

PRODUCTS = {
    "turmeric":     ("Curcuma longa",  ["Curcuma zedoaria", "Zea mays", "Manihot esculenta", "Triticum aestivum"]),
    "saffron":      ("Crocus sativus", ["Carthamus tinctorius", "Zea mays", "Curcuma longa"]),
    "black_pepper": ("Piper nigrum",   ["Carica papaya", "Zea mays"]),
}
BACKGROUND = ["Oryza sativa", "Glycine max", "Capsicum annuum", "Allium sativum", "Solanum lycopersicum"]
N_AUTH, N_ADULT, N_SUBST = 5, 3, 2

rows, manifest, truth = [], [], []
sid = 0
for product, (label, adulterants) in PRODUCTS.items():
    classes = ["AUTHENTIC"]*N_AUTH + ["ADULTERATED"]*N_ADULT + ["SUBSTITUTED"]*N_SUBST
    for cls in classes:
        sid += 1
        sample = f"S{sid:02d}"
        depth = int(rng.lognormal(mean=np.log(20000), sigma=0.3))
        props = {}
        if cls == "AUTHENTIC":
            props[label] = 1.0
        elif cls == "ADULTERATED":
            filler = rng.uniform(0.10, 0.40)
            chosen = rng.choice(adulterants, size=rng.integers(1, 3), replace=False)
            w = rng.dirichlet(np.ones(len(chosen)))
            props[label] = 1 - filler
            for sp, wi in zip(chosen, w):
                props[sp] = filler * wi
        else:  # SUBSTITUTED: label species nearly absent
            chosen = rng.choice(adulterants, size=rng.integers(1, 3), replace=False)
            w = rng.dirichlet(np.ones(len(chosen)))
            tiny = rng.uniform(0.0, 0.02)
            props[label] = tiny
            for sp, wi in zip(chosen, w):
                props[sp] = (1 - tiny) * wi
        # low-level background / index-hopping noise (0.05-0.8% total)
        noise = rng.uniform(0.0005, 0.008)
        bg = rng.choice(BACKGROUND, size=2, replace=False)
        for sp in bg:
            props[sp] = props.get(sp, 0) + noise / 2
        sp_list = list(props); p = np.array([props[s] for s in sp_list]); p /= p.sum()
        counts = rng.multinomial(depth, p)
        for sp, c in zip(sp_list, counts):
            if c > 0:
                rows.append((sample, sp, int(c)))
        manifest.append((sample, product, label))
        truth.append((sample, cls))

pd.DataFrame(rows, columns=["sample", "species", "reads"]).to_csv("data/simulated_species_table.csv", index=False)
pd.DataFrame(manifest, columns=["sample", "product", "label_species"]).to_csv("data/simulated_manifest.csv", index=False)
pd.DataFrame(truth, columns=["sample", "truth"]).to_csv("data/simulated_truth.csv", index=False)
print(f"Simulated {sid} samples, {len(rows)} sample-species rows")
