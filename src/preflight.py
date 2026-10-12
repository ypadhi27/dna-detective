"""Fail closed before real-data downloads. Executed locally; sequencing remains UNTESTED."""
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
    print('Real-data workflow BLOCKED:\n'+'\n'.join(errors),file=sys.stderr)
    sys.exit(1)
