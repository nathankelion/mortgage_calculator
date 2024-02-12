from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time, zipfile, os

# Zip file link
zip_url = 'https://www.bankofengland.co.uk/-/media/boe/files/statistics/yield-curves/latest-yield-curve-data.zip'

# Downloaded zip file path
zip_file_path = 'latest-yield-curve-data.zip'

# Destination folder for extracted file
destination_folder = 'data'

# Initialize Chrome options
chrome_options = Options()

# Check if running in GitHub Actions
if 'GITHUB_ACTIONS' in os.environ:
    # Running in GitHub Actions
    print("Running in GitHub Actions. Using default download folder.")
    chrome_service = Service(os.environ['CHROMEWEBDRIVER'])
    for option in ['--headless','--disable-gpu','--window-size=1920,1200','--ignore-certificate-errors','--disable-extensions','--no-sandbox','--disable-dev-shm-usage']:
        chrome_options.add_argument(option)
    # Initialize ChromeDriver with the specified path
    driver = webdriver.Chrome(service = chrome_service,options = chrome_options)
else:
    # Running locally
    download_folder = r'C:\Users\natha\OneDrive\Documents\data_science_projects\mortgage_calculator'
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': download_folder,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    # Initialize ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

# Navigate to the zip file link
driver.get(zip_url)

# Give the zipped folder time to download
time.sleep(5)

# Close the browser
driver.quit()

# Extract the specific Excel file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    for file in zip_ref.namelist():
        if file == 'GLC Nominal daily data current month.xlsx':
            zip_ref.extract(file, destination_folder)

# Clean up: remove the downloaded zip file
os.remove(zip_file_path)
