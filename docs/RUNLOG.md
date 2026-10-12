# Run log — 2026-10-12

## Outcome
Simulation executed successfully. Real sequencing stopped at preflight under the supplied AGENTS.md instruction: “If a step fails (download blocked, no network, tool missing), stop that step, record the exact error …”. No environment installation via Conda was attempted because `conda`, `mamba`, and `micromamba` were absent. Rscript, BLAST and SRA executables were also absent. No real-data performance claims are made.

## Commands and operations
Commands below were run from the project unless absolute paths are shown; inspection reads are grouped. The two development scripts used to modify files are archived in `docs/development/`.

1. `cat /Users/yajnaseneepadhi/Downloads/CODEX_PROMPT.md`; `unzip -l /Users/yajnaseneepadhi/Downloads/dna-detective.zip`.
2. From the workspace: `mkdir -p outputs work`; `unzip -q /Users/yajnaseneepadhi/Downloads/dna-detective.zip -d outputs`. Read `AGENTS.md`, `README.md`, `environment.yml`, `Makefile`, `MANUSCRIPT.md`, `src/*.py`, `workflow/*`, `.gitignore`.
3. `command -v conda micromamba mamba Rscript blastn fasterq-dump gh python3`; `python3 -V`. Python 3.11.9 and gh present; sequencing tools absent.
4. `mkdir -p docs data/real results/real`; Python dependency import failed with `ModuleNotFoundError: No module named 'matplotlib'`. Initial chained demo therefore did not run.
5. `python3 -m venv .venv`; `.venv/bin/pip install -r requirements.txt > docs/python-install.log 2>&1` — succeeded.
6. Web searches: `ITS2 herbal products metabarcoding paired end SRA BioProject`, `"DNA-Based Herbal Teas" "PRJ"`, `"37255553" "PRJNA"`. PMC page https://pmc.ncbi.nlm.nih.gov/articles/PMC8539046/ returned reCAPTCHA. Opening https://www.ncbi.nlm.nih.gov/sra/SRX29255992 timed out. A speculative Frontiers URL was inaccessible and is not used as evidence.
7. `curl -fL --max-time 40` fetched the ENA filereport endpoint with `accession=SRX29255992`, `result=read_run`, `format=tsv`, fields `run_accession,study_accession,secondary_study_accession,sample_accession,library_layout,library_strategy,fastq_ftp`; saved as `data/real/ena_candidate.tsv`.
8. Same ENA endpoint (`https://www.ebi.ac.uk/ena/portal/api/filereport`) queried with `accession=PRJNA1279389` and fields `run_accession,study_accession,sample_accession,library_layout,library_strategy,sample_title,experiment_title,fastq_ftp`; saved as `data/real/ena_study.tsv`. Both downloads succeeded. Candidate run existence/layout verified; labels, source paper and suitability unresolved.
9. `git init`; `git add .`; initial import commit. Accidentally staged virtual environment removed with `git rm -r --cached -q .venv`, `.gitignore` updated, and own unpublished import commit amended.
10. Moved supplied results into `results/simulated/` and replaced simulation output references in Python and Markdown. `PATH="$PWD/.venv/bin:$PATH" make demo > docs/demo.log 2>&1` succeeded.
11. `.venv/bin/python ../../work/update_project.py` applied workflow changes. `make real > docs/real-preflight.log 2>&1` exited 2 (Make), with Python preflight exit 1. Exact errors in that log.
12. `.venv/bin/pip freeze > requirements-lock.txt`; added regression tests. `make test > docs/tests.log 2>&1`; `make demo > docs/demo.log 2>&1`.
13. `.venv/bin/python ../../work/document_project.py` updated documentation. Final shell syntax, Python compilation, tests, demo and Git checks recorded alongside this log.

## Validation scope
Executed: Python simulation, classifier, synthetic ASV conversion tests and real preflight failure path. UNTESTED on real data: download, DADA2, BLAST, ASV conversion and real plot. Primer trimming is not implemented; study-specific verification is required. No reference build, raw-read download or GitHub publication occurred. The requested real-data acceptance criteria are not met.

Python dependency versions are pinned in `requirements-lock.txt`; simulation stdout is `demo.log`; tests are in `tests.log`.
