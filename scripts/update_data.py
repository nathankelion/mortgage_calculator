import os
import csv

# Path to the data folder
data_folder = "data"

# Create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Path to the blank CSV file
csv_file_path = os.path.join(data_folder, "blank.csv")

# Create an empty CSV file
with open(csv_file_path, "w", newline="") as csvfile:
    # You can add headers or additional rows here if needed
    pass

print(f"Blank CSV file created at: {csv_file_path}")