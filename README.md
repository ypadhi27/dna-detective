# 🔍 DNA Detective

**Is that turmeric really turmeric?** An open, reproducible workflow that uses DNA metabarcoding (ITS2) to detect adulteration and substitution in spices and herbal products, with an explicit, tunable decision rule.

> **Status:** Decision logic validated on **simulated** data. Real-data scripts are **untested templates**. See [MANUSCRIPT.md](MANUSCRIPT.md) for the full journal-style write-up, results and limitations.

## What it does
```
raw reads → DADA2 → BLAST vs ITS2 reference → species table → verdict (AUTHENTIC / ADULTERATED / SUBSTITUTED)
```

## Quick start (runs in seconds, no sequencing data needed)
```bash
pip install -r requirements.txt
make demo
```
This simulates 30 spice samples plus a dilution series and regenerates every table and figure in `results/`.

## Key finding (simulation)
The noise floor sets your limit of detection: at ≥95% detection, a 0.1% floor catches 0.2% filler, a 1% floor needs ~2%, and a 2% floor needs ~5%.

![LOD](results/fig3_limit_of_detection.png)

## Repo layout
| Path | Purpose |
|---|---|
| `workflow/` | Real-data steps: SRA download, DADA2, BLAST (templates, untested) |
| `src/asv_to_species.py` | ASV counts + BLAST hits → species table |
| `src/authenticate.py` | Rule-based verdict classifier (CLI + importable) |
| `src/simulate_data.py`, `src/lod_experiment.py` | Simulations |
| `src/evaluate.py`, `src/plot_results.py` | Metrics and figures |
| `results/` | Generated tables and figures |
| `MANUSCRIPT.md` | Full write-up |
| `CODEX_PROMPT.md`, `AGENTS.md` | Prompt and rules for completing the real-data step with Codex |

## Use on your own species table
```bash
python src/authenticate.py --table my_species_table.csv --manifest my_manifest.csv --out verdicts.csv \
  --noise-floor 0.01 --adulterant-threshold 0.05
```
`species_table.csv`: `sample,species,reads` · `manifest.csv`: `sample,product,label_species`

## Roadmap
- [ ] Run on public SRA/BOLD spice and herbal datasets
- [ ] Mock-mixture calibration of read fraction vs true mass fraction
- [ ] Negative-control-based noise estimation
- [ ] Streamlit dashboard
- [ ] Cosmetic botanicals and endangered-species checks

## Citation
If you use this, please cite the repository (see `MANUSCRIPT.md`). Licence: MIT.
