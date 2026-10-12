PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
.PHONY: demo real test
demo:
	mkdir -p results/simulated
	$(PYTHON) src/simulate_data.py
	PYTHONPATH=src $(PYTHON) src/evaluate.py
	$(PYTHON) src/plot_results.py
	PYTHONPATH=src $(PYTHON) src/lod_experiment.py

real:
	$(PYTHON) src/preflight.py
	bash workflow/01_get_data.sh
	Rscript workflow/02_dada2_its2.R data/real/raw results/real
	bash workflow/03_assign_species.sh data/real/its2_reference.fasta results/real/asvs.fasta results/real
	$(PYTHON) src/asv_to_species.py results/real/asv_counts.csv results/real/blast_hits.tsv results/real/species_table.csv
	$(PYTHON) src/authenticate.py --table results/real/species_table.csv --manifest data/real/manifest.csv --out results/real/verdicts.csv
	$(PYTHON) src/plot_real.py

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v
