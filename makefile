# All the commands to scaffold and run the project

.PHONY: install data-raw features clean

# Install the package in editable mode
install:
	pip install -e .

# Download data without processing
data-raw:
	python -m concatenative_synthesis.data

# Calculate features from data
features:
	python -m concatenative_synthesis.features.extract

# Clean up generated files
clean:
	rm -rf data/features/
	rm -rf *.egg-info/