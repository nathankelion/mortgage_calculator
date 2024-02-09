import requests
import zipfile
import os

# URL of the Bank of England zip file
zip_file_url = "https://www.bankofengland.co.uk/-/media/boe/files/statistics/yield-curves/latest-yield-curve-data.zip"

# Path to your data folder
data_folder = "data"

try:
    # Download the zip file
    r = requests.get(zip_file_url, stream=True)
    with open("latest_data.zip", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract the desired Excel file
    excel_file_name = "GLC Nominal daily data current month.xlsx"
    with zipfile.ZipFile("latest_data.zip", "r") as zip_ref:
        zip_ref.extract(excel_file_name, data_folder)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up: remove the downloaded zip file
    try:
        os.remove("latest_data.zip")
    except OSError:
        pass  # Ignore the error if the file doesn't exist