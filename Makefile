.PHONY: help validate smoke-python compile-python smoke-summary

help:
	@echo "make validate        validate catalog, utility templates and function index"
	@echo "make smoke-python    run dependency-light input and sample-level tests"
	@echo "make compile-python  compile all Python templates"

validate:
	python python/validate_manifest.py

smoke-python:
	python python/00_input_audit.py --input data/mock/scrna_counts.csv --output /tmp/nm_input_audit.json
	python python/08_sample_level_summary.py --scores data/mock/cell_scores.csv --metadata data/mock/scrna_metadata.csv --output /tmp/nm_sample_level_summary.csv

compile-python:
	python -m compileall -q python
