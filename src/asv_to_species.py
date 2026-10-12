"""Turn ASV counts + BLAST hits into the (sample, species, reads) table used by authenticate.py.

Rule: best bitscore hit per ASV; keep if identity >= MIN_ID and alignment covers >= MIN_COV of the ASV;
otherwise the ASV is labelled 'Unassigned'.  UNTESTED on real data.
"""
import sys, pandas as pd
MIN_ID, MIN_COV = 97.0, 0.90
counts = pd.read_csv(sys.argv[1], index_col=0)                # rows = ASV sequence, cols = samples
hits = pd.read_csv(sys.argv[2], sep="\t", header=None,
                   names=["qseqid", "sseqid", "pident", "length", "qlen", "bitscore"])
if not counts.index.to_series().str.fullmatch(r"ASV[0-9]+").all():
    raise ValueError("ASV count row IDs must match FASTA IDs")
if not set(hits.qseqid).issubset(set(counts.index)):
    raise ValueError("BLAST query IDs absent from counts")
hits["cov"] = hits["length"] / hits["qlen"]
best = hits.sort_values("bitscore", ascending=False).drop_duplicates("qseqid")
best = best[(best["pident"] >= MIN_ID) & (best["cov"] >= MIN_COV)]
best["species"] = best["sseqid"].str.split("|").str[1].str.replace("_", " ")
asv2sp = {a: s for a, s in zip(best["qseqid"], best["species"])}
counts = counts.copy(); counts["species"] = [asv2sp.get(asv, "Unassigned") for asv in counts.index]
tab = counts.groupby("species").sum().reset_index().melt("species", var_name="sample", value_name="reads")
tab[tab["reads"] > 0][["sample", "species", "reads"]].to_csv(sys.argv[3], index=False)
