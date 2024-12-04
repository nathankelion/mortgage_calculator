# from selenium import webdriver
# import time, zipfile, os

# # Zip file link
# zip_url = 'https://www.bankofengland.co.uk/-/media/boe/files/statistics/yield-curves/latest-yield-curve-data.zip'

# # Downloaded zip file path
# zip_file_path = 'latest-yield-curve-data.zip'

# # Destination folder for extracted file
# destination_folder = 'data'

# # Initialize Chrome options
# chrome_options = webdriver.ChromeOptions()

# # Check if running in GitHub Actions
# if 'GITHUB_ACTIONS' in os.environ:
#     # Running in GitHub Actions
#     print("Running in GitHub Actions. Using default download folder.")
#     # Add headless mode
#     chrome_options.add_argument('--headless')
#     # Initialize ChromeDriver with the specified path
#     driver = webdriver.Chrome(options=chrome_options)
# else:
#     # Running locally
#     download_folder = r'C:/Users/natha/OneDrive/Documents/data_science_projects/mortgage_calculator'
#     chrome_options.add_experimental_option('prefs', {
#         'download.default_directory': download_folder,
#         'download.prompt_for_download': False,
#         'download.directory_upgrade': True,
#         'safebrowsing.enabled': True
#     })
#     # Initialize ChromeDriver
#     driver = webdriver.Chrome(options=chrome_options)

# # Navigate to the zip file link
# driver.get(zip_url)

# # Give the zipped folder time to download
# time.sleep(5)

# # Close the browser
# driver.quit()

# # Extract the specific Excel file
# with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     for file in zip_ref.namelist():
#         if file == 'GLC Nominal daily data current month.xlsx':
#             zip_ref.extract(file, destination_folder)

# # Clean up: remove the downloaded zip file
# os.remove(zip_file_path)


import os
import zipfile
import shutil
import requests

# URL to the ZIP file
zip_url = 'https://www.bankofengland.co.uk/-/media/boe/files/statistics/yield-curves/latest-yield-curve-data.zip'

# Downloaded zip file path
zip_file_path = 'latest-yield-curve-data.zip'

# Destination folder for extracted file
destination_folder = 'data'

# Temporary download folder (ensure it exists)
download_folder = '/tmp/chrome_downloads'

# Ensure the download folder exists
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Step 1: Download the ZIP file using requests
print("Downloading the ZIP file...")
response = requests.get(zip_url, stream=True)

# Check if the request was successful
if response.status_code == 200:
    # Write the content to the file
    with open(zip_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print("Download completed.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")

# Step 2: Extract the specific Excel file from the ZIP
if os.path.exists(zip_file_path):
    print("Extracting files from the ZIP...")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file == 'GLC Nominal daily data current month.xlsx':
                zip_ref.extract(file, destination_folder)
                print(f"Extracted {file} to {destination_folder}")
else:
    print(f"{zip_file_path} not found after download.")

# Step 3: Clean up: remove the downloaded zip file
if os.path.exists(zip_file_path):
    os.remove(zip_file_path)
