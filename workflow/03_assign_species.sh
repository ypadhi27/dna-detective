#!/usr/bin/env bash
# UNTESTED TEMPLATE: assign ASVs to species by BLAST against a curated ITS2 reference.
# Reference FASTA headers must look like: >ACCESSION|Genus_species
# Build the reference from NCBI/BOLD plus authoritative vouchered sequences (see MANUSCRIPT.md, Limitations).
set -euo pipefail
REF=${1:?reference.fasta}; ASV=${2:?results/asvs.fasta}
makeblastdb -in "$REF" -dbtype nucl -out results/its2_ref
blastn -query "$ASV" -db results/its2_ref -max_target_seqs 5 -evalue 1e-10 \
  -outfmt "6 qseqid sseqid pident length qlen bitscore" > results/blast_hits.tsv
