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
	python python/09_mellon_template.py --embedding data/mock/cell_embedding.csv --metadata data/mock/scrna_metadata.csv --output /tmp/nm_mellon_manifest.json
	python python/10_miso_manifest.py --omics data/mock/scrna_counts.csv data/mock/cell_scores.csv --image-features data/mock/cell_embedding.csv --spot-metadata data/mock/scrna_metadata.csv --output /tmp/nm_miso_manifest.json
	python python/11_scmmib_manifest.py --dataset-manifest data/mock/multimodal_dataset_manifest.csv --task paired --output /tmp/nm_scmmib_manifest.json
	python python/12_scmultibench_manifest.py --dataset-manifest data/mock/multimodal_dataset_manifest.csv --tasks dimension_reduction clustering --output /tmp/nm_scmultibench_manifest.json
	python python/13_narmbench_manifest.py --reads data/mock/narmbench_reads.fastq --reference data/mock/narmbench_reference.fa --output /tmp/nm_narmbench_manifest.json
	python python/14_pinnacle_manifest.py --expression data/mock/scrna_counts.csv --ppi-network data/mock/protein_network.tsv --context-metadata data/mock/context_metadata.csv --output /tmp/nm_pinnacle_manifest.json
	python python/15_phlower_manifest.py --modalities data/mock/scrna_counts.csv data/mock/cell_scores.csv --cell-metadata data/mock/scrna_metadata.csv --root-label control --task both --output /tmp/nm_phlower_manifest.json
	python python/16_spatialdata_manifest.py --datasets data/mock/spatialdata_table.csv --elements table points --coordinate-system tissue --platform synthetic --output /tmp/nm_spatialdata_manifest.json
	python python/17_scikit_bio_manifest.py --inputs data/mock/narmbench_reference.fa --operation sequence --format FASTA --output /tmp/nm_scikit_bio_manifest.json

compile-python:
	python -m compileall -q python
