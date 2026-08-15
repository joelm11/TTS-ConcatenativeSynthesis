# All the commands to scaffold and run the project using uv

.PHONY: install data-raw features clean

# Install the package and dependencies in a virtual environment
install:
	uv sync

# Download data without processing
data-raw:
	uv run python -m concatenative_synthesis.data

# Calculate features from data
features:
	uv run python -m concatenative_synthesis.features.extract

# Clean up generated files and venv
clean:
	rm -rf data/features/
	rm -rf *.egg-info/