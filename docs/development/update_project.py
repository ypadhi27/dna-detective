from pathlib import Path
import csv
p=Path('.')
# Portable interpreter selection.
f=p/'Makefile'
f.write_text('PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)\n.PHONY: demo real test\ndemo:\n\tmkdir -p results/simulated\n\t$(PYTHON) src/simulate_data.py\n\tPYTHONPATH=src $(PYTHON) src/evaluate.py\n\t$(PYTHON) src/plot_results.py\n\tPYTHONPATH=src $(PYTHON) src/lod_experiment.py\n\nreal:\n\t$(PYTHON) src/preflight.py\n\tbash workflow/01_get_data.sh\n\tRscript workflow/02_dada2_its2.R data/real/raw results/real\n\tbash workflow/03_assign_species.sh data/real/its2_reference.fasta results/real/asvs.fasta results/real\n\t$(PYTHON) src/asv_to_species.py results/real/asv_counts.csv results/real/blast_hits.tsv results/real/species_table.csv\n\t$(PYTHON) src/authenticate.py --table results/real/species_table.csv --manifest data/real/manifest.csv --out results/real/verdicts.csv\n\t$(PYTHON) src/plot_real.py\n\ntest:\n\tPYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v\n')
rows=list(csv.DictReader(open('data/real/ena_study.tsv'),delimiter='\t'))
chosen=[r for r in rows if r['library_layout']=='PAIRED'][:3]
with open('data/real/manifest_sources.csv','w') as o:
 w=csv.DictWriter(o,fieldnames=['bioproject','run_accession','sample_title','label_species','source_paper','status','metadata_url']); w.writeheader()
 for r in chosen:w.writerow(dict(bioproject=r['study_accession'],run_accession=r['run_accession'],sample_title=r['sample_title'],label_species='TODO: verify',source_paper='TODO: verify',status='Run and paired amplicon layout verified; marker and product label unresolved',metadata_url='https://www.ebi.ac.uk/ena/browser/view/'+r['run_accession']))
Path('data/real/accessions.txt').write_text('# No approved runs. Candidates are in manifest_sources.csv.\n# Verify ITS2-only reads, primers, labels and source paper before adding accessions.\n')
Path('data/real/manifest.csv').write_text('sample,product,label_species\n')
Path('src/preflight.py').write_text('''"""Fail closed before real-data downloads. Executed locally; sequencing remains UNTESTED."""
from pathlib import Path
import csv, re, shutil, sys
errors=[]
for tool in ['prefetch','fasterq-dump','Rscript','makeblastdb','blastn']:
    if not shutil.which(tool): errors.append(f'Missing executable: {tool}')
accessions=[s.strip() for s in Path('data/real/accessions.txt').read_text().splitlines() if s.strip() and not s.startswith('#')]
if not accessions: errors.append('No approved runs in data/real/accessions.txt')
if any(not re.fullmatch(r'[SED]RR[0-9]+', s) for s in accessions): errors.append('Invalid run accession')
manifest=list(csv.DictReader(open('data/real/manifest.csv')))
if set(accessions)!={r['sample'] for r in manifest}: errors.append('Manifest samples must exactly match accessions')
if any(not r['label_species'].strip() or 'TODO' in r['label_species'] for r in manifest): errors.append('Unverified label species')
ref=Path('data/real/its2_reference.fasta')
if not ref.exists() or not ref.stat().st_size: errors.append('Missing curated data/real/its2_reference.fasta')
if not Path('data/real/PRIMERS_VERIFIED.md').exists(): errors.append('Missing PRIMERS_VERIFIED.md: document primer removal or verified primer-free input')
if errors:
    print('Real-data workflow BLOCKED:\\n'+'\\n'.join(errors),file=sys.stderr)
    sys.exit(1)
''')
f=Path('workflow/01_get_data.sh');s=f.read_text().replace('data/accessions.txt','data/real/accessions.txt').replace('data/raw','data/real/raw').replace('while read -r acc; do','while IFS= read -r acc || [[ -n "$acc" ]]; do\n  [[ -z "$acc" || "$acc" == \\#* ]] && continue\n  [[ "$acc" =~ ^[SED]RR[0-9]+$ ]] || { echo "Invalid accession: $acc" >&2; exit 1; }');f.write_text(s)
f=Path('workflow/03_assign_species.sh');s=f.read_text().replace('makeblastdb -in', 'OUT=${3:-results/real}\nmkdir -p "$OUT"\nmakeblastdb -in').replace('results/its2_ref','"$OUT/its2_ref"').replace('results/blast_hits.tsv','"$OUT/blast_hits.tsv"');f.write_text(s)
f=Path('workflow/02_dada2_its2.R');s=f.read_text().replace('dir.create(out_dir, showWarnings = FALSE)','dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)\ndir.create(file.path(out_dir, "filtered"), showWarnings = FALSE)');s=s.replace('samples <- sub', 'if (!length(fnF) || length(fnF) != length(fnR)) stop("Missing or unpaired FASTQ files")\nif (!identical(sub("_1.fastq.*", "", basename(fnF)), sub("_2.fastq.*", "", basename(fnR)))) stop("FASTQ sample names differ")\nsamples <- sub');s=s.replace('uniquesToFasta(seqtab, file.path(out_dir, "asvs.fasta"))\nwrite.csv(t(seqtab), file.path(out_dir, "asv_counts.csv"))   # rows = ASV sequence','if (!ncol(seqtab)) stop("No ASVs survived filtering")\nids <- paste0("ASV", seq_len(ncol(seqtab)))\nwriteLines(as.vector(rbind(paste0(">", ids), colnames(seqtab))), file.path(out_dir, "asvs.fasta"))\ncounts <- t(seqtab)\nrownames(counts) <- ids\nwrite.csv(counts, file.path(out_dir, "asv_counts.csv"))');f.write_text(s)
f=Path('src/asv_to_species.py');s=f.read_text();s=s.replace('fasta_ids = {f"ASV{i+1}": s for i, s in enumerate(counts.index)}   # matches uniquesToFasta order','if not counts.index.to_series().str.fullmatch(r"ASV[0-9]+").all():\n    raise ValueError("ASV count row IDs must match FASTA IDs")\nif not set(hits.qseqid).issubset(set(counts.index)):\n    raise ValueError("BLAST query IDs absent from counts")');s=s.replace('asv2sp.get(f"ASV{i+1}", "Unassigned") for i in range(len(counts))','asv2sp.get(asv, "Unassigned") for asv in counts.index');f.write_text(s)
f=Path('src/authenticate.py');s=f.read_text().replace('    out = []','    for value in (noise_floor, adulterant_threshold, substitution_threshold):\n        if not 0 <= value <= 1:\n            raise ValueError("Thresholds must be between zero and one")\n    if table["reads"].isna().any() or (table["reads"] < 0).any():\n        raise ValueError("Read counts must be nonnegative and finite")\n    table = table.groupby(["sample", "species"], as_index=False)["reads"].sum()\n    out = []').replace('        if label_frac < substitution_threshold:', '        if total <= 0 or t.empty or (t["species"] == "Unassigned").any():\n            verdict = "INCONCLUSIVE"\n        elif label_frac < substitution_threshold:');f.write_text(s)
Path('src/plot_real.py').write_text('''"""UNTESTED on real sequencing outputs."""
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
''')
