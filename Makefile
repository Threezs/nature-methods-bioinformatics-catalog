.PHONY: help validate smoke-python smoke-method-manifests compile-python smoke-summary

help:
	@echo "make validate        validate catalog, utility templates and function index"
	@echo "make smoke-python    run dependency-light input and sample-level tests"
	@echo "make smoke-method-manifests  validate recent-method manifest entrypoints"
	@echo "make compile-python  compile all Python templates"

validate:
	python python/validate_manifest.py

smoke-python:
	python python/00_input_audit.py --input data/mock/scrna_counts.csv --output /tmp/nm_input_audit.json
	python python/08_sample_level_summary.py --scores data/mock/cell_scores.csv --metadata data/mock/scrna_metadata.csv --output /tmp/nm_sample_level_summary.csv

smoke-method-manifests:
	python python/09_mellon_template.py --embedding data/mock/cell_scores.csv --metadata data/mock/scrna_metadata.csv --output /tmp/nm_mellon_manifest.json
	python python/10_miso_manifest.py --omics data/mock/scrna_counts.csv --image-features data/mock/cell_scores.csv --spot-metadata data/mock/scrna_metadata.csv --output /tmp/nm_miso_manifest.json
	python python/11_scmmib_manifest.py --dataset-manifest data/mock/scrna_metadata.csv --task paired --output /tmp/nm_scmmib_manifest.json

compile-python:
	python -m compileall -q python
