demo:
	python3 src/simulate_data.py
	PYTHONPATH=src python3 src/evaluate.py
	python3 src/plot_results.py
	PYTHONPATH=src python3 src/lod_experiment.py
