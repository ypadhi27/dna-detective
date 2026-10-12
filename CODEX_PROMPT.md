# Prompt to paste into Codex

Open this repo in Codex (CLI, IDE or cloud) and paste everything inside the box.

```
You are working in the repo "dna-detective": an ITS2 metabarcoding workflow that detects
adulteration and substitution in spices/herbal products. Read README.md, MANUSCRIPT.md and
AGENTS.md first and follow AGENTS.md strictly.

CURRENT STATE
- Decision logic (src/authenticate.py) is validated on SIMULATED data only (`make demo`).
- workflow/01_get_data.sh, workflow/02_dada2_its2.R, workflow/03_assign_species.sh and
  src/asv_to_species.py are UNTESTED templates.

GOAL
Run the pipeline on REAL public data, report honestly what happens, and update the manuscript.

TASKS
1. Environment: create the conda env from environment.yml (or document what is missing).
   Run `make demo` and confirm it passes.
2. Find data: search NCBI SRA / ENA (use `esearch`/`efetch`, the ENA portal API, or the web)
   for 3 to 10 public paired-end ITS2 (or other plant barcode) metabarcoding runs from
   spices, herbal products, honey or botanical supplements. Prefer studies that state the
   product label. Record BioProject, run accessions, label, and source paper in
   data/real/manifest_sources.csv. Do not guess accessions; verify each one exists.
3. Reference database: build data/real/its2_reference.fasta from NCBI nucleotide ITS2 records
   for the declared label species and their known adulterants (headers "ACCESSION|Genus_species").
   Document how it was built (query, date, filters) in docs/REFERENCE.md.
4. Run workflow/01..03 and src/asv_to_species.py on the real runs. Fix bugs in the templates as
   needed (for example primer trimming, ASV ID matching, file naming). Keep fixes minimal and
   commit each one with a clear message.
5. Run src/authenticate.py on the real species table. Save outputs in results/real/
   (verdicts.csv, species_table.csv, a composition figure like Fig. 1).
6. Move current simulated outputs to results/simulated/ and update paths in src/ and Makefile
   so `make demo` still works.
7. Update MANUSCRIPT.md: add a "Real-data case study" section with the actual results, revise
   the Abstract, Limitations and Future Work to match, and remove the "simulated only" claims
   that are no longer true. If the real run failed or the data were unsuitable, say so plainly
   rather than softening it.
8. Write docs/RUNLOG.md listing every command run, versions of tools, and any errors.
9. Commit in small logical commits. If `gh` is authenticated, create a public GitHub repo
   "dna-detective" and push; otherwise leave the repo ready and print the exact commands I
   should run.

ACCEPTANCE CRITERIA
- Every number and figure in MANUSCRIPT.md is reproducible from code and files in the repo.
- `make demo` passes. A new `make real` target reproduces the real-data results from
  data/real/accessions.txt.
- No invented data, accessions or citations. Unverified items carry "TODO: verify".
- Final message: summarise what worked, what failed, and what is still untested.
```

## Tips
- Cloud Codex often has no internet for SRA downloads. Use the CLI or IDE on your machine, or enable network access in the task settings.
- If it cannot find suitable paired-end data, ask it to report that instead of lowering the standard. Single-end data would need small changes to `02_dada2_its2.R`.
- Review the diff of `MANUSCRIPT.md` yourself before you push.
