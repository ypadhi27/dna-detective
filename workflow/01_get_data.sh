#!/usr/bin/env bash
# UNTESTED TEMPLATE: download public ITS2 metabarcoding runs for spice/herbal products.
# 1) Find BioProjects: NCBI SRA search e.g. "ITS2 spice adulteration", "herbal product metabarcoding".
# 2) Put run accessions (one per line) in data/real/accessions.txt
set -euo pipefail
mkdir -p data/real/raw
while IFS= read -r acc || [[ -n "$acc" ]]; do
  [[ -z "$acc" || "$acc" == \#* ]] && continue
  [[ "$acc" =~ ^[SED]RR[0-9]+$ ]] || { echo "Invalid accession: $acc" >&2; exit 1; }
  prefetch "$acc" -O data/real/raw
  fasterq-dump "data/real/raw/$acc" -O data/real/raw --split-files
done < data/real/accessions.txt
