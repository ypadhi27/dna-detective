#!/usr/bin/env bash
# UNTESTED TEMPLATE: download public ITS2 metabarcoding runs for spice/herbal products.
# 1) Find BioProjects: NCBI SRA search e.g. "ITS2 spice adulteration", "herbal product metabarcoding".
# 2) Put run accessions (one per line) in data/accessions.txt
set -euo pipefail
mkdir -p data/raw
while read -r acc; do
  prefetch "$acc" -O data/raw
  fasterq-dump "data/raw/$acc" -O data/raw --split-files
done < data/accessions.txt
