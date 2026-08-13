# All the commands to scaffold and run the project

# Download data without processing
data-raw:
	@echo "Downloading data and creating data directory structure . . ."
	@./data.py
	@echo "Done!"

# Calculate features from data
