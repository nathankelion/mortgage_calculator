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
import time
import zipfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# URL to the ZIP file
zip_url = 'https://www.bankofengland.co.uk/-/media/boe/files/statistics/yield-curves/latest-yield-curve-data.zip'

# Downloaded zip file path
zip_file_path = 'latest-yield-curve-data.zip'

# Destination folder for extracted file
destination_folder = 'data'

# Temporary download folder
download_folder = '/tmp/chrome_downloads'

# Initialize Chrome options
chrome_options = Options()

# Set the download directory for Chrome in headless mode
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(f'--download-default-directory={download_folder}')

# Initialize ChromeDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the zip file link
driver.get(zip_url)

# Wait for the download to complete (adjust this time as necessary)
time.sleep(10)  # Increased time to ensure file download

# Debugging: List files in the download folder to check if the file was downloaded
print("Contents of download folder:")
for filename in os.listdir(download_folder):
    print(filename)

# Check if the downloaded zip file is in the folder
downloaded_zip_file = os.path.join(download_folder, 'latest-yield-curve-data.zip')
if os.path.exists(downloaded_zip_file):
    print("File found:", downloaded_zip_file)
    # Move the downloaded zip file to the desired location
    shutil.move(downloaded_zip_file, zip_file_path)
else:
    print("Download failed or file not found.")

# Close the browser
driver.quit()

# If file is found, proceed with extraction
if os.path.exists(zip_file_path):
    # Extract the specific Excel file from the zip
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file == 'GLC Nominal daily data current month.xlsx':
                zip_ref.extract(file, destination_folder)
                print(f"Extracted {file} to {destination_folder}")
else:
    print(f"{zip_file_path} not found after download.")

# Clean up: remove the downloaded zip file
if os.path.exists(zip_file_path):
    os.remove(zip_file_path)
