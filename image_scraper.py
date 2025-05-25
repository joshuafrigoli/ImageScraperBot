from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import argparse
import sys
import requests
from pathlib import Path
import time
import platform

# Argparser
parser = argparse.ArgumentParser()
url_advise = "target url"
parser.add_argument("url", type=str, help=url_advise)
selector_advise = "elements css selector"
parser.add_argument("css_selector", type=str, help=selector_advise)
parser.add_argument(
    "--attribute",
    type=str,
    default="src",
    help="elements' attribute to download from, (default src)",
)
parser.add_argument(
    "--driver",
    type=str,
    choices=["chrome", "firefox", "edge", "safari"],
    default="chrome",
    help="driver to use when browsing",
)
parser.add_argument(
    "--folder_path",
    type=str,
    default="images",
    help="downloaded images folder name",
)
parser.add_argument(
    "--incognito",
    action="store_true",
    help="open browser in incognito/private mode, (not available on Safari yet)",
)
parser.add_argument(
    "--saving_format",
    type=str,
    choices=["jpg", "png"],
    default="jpg",
    help="downloaded images saving format",
)
args = parser.parse_args()

# Setup
driver_name = args.driver
incognito = args.incognito
url = args.url
selector = args.css_selector
attribute = args.attribute
saving_format = args.saving_format
folder_path = args.folder_path

if not url:
    sys.exit(f"Error: missing {url_advise}!")
if not selector:
    sys.exit(f"Error: missing {selector_advise}!")

# Browser init
driver = None
# Detect OS
os_name = platform.system().lower()

# Initialize the correct driver
if driver_name == "chrome":
    options = ChromeOptions()
    if incognito:
        options.add_argument("--incognito")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
elif driver_name == "firefox":
    options = FirefoxOptions()
    if incognito:
        options.add_argument("-private")
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()), options=options
    )
elif driver_name == "edge":
    options = EdgeOptions()
    if incognito:
        options.add_argument("-inprivate")
    driver = webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager().install()),
        options=options,
    )
elif driver_name == "safari":
    if os_name != "darwin":
        sys.exit("Error: Safari WebDriver only works on MacOS.")
    driver = webdriver.Safari()
else:
    sys.exit(f"Error: driver {driver_name} non supported on this machine.")

driver.get(url)

# Attesa elementi dinamici
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
)

# Scroll down per caricare immagini lazyload
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Estrazione immagini
elements = driver.find_elements(By.CSS_SELECTOR, selector)
print(f"[INFO] Elements found: {len(elements)}")

folder = Path(folder_path)
folder.mkdir(parents=True, exist_ok=True)

downloaded = 0
for i, element in enumerate(elements):
    try:
        img_url = element.get_attribute(attribute)
        if not img_url or not img_url.startswith("http"):
            continue
        print(f"  Downloading: {img_url}")
        img_data = requests.get(img_url).content
        filename = f"img_{i:03d}.{saving_format}"
        with open(folder / filename, "wb") as f:
            f.write(img_data)
        downloaded += 1
    except Exception as e:
        print(f"  [ERROR] Could not download element {i}: {e}")

driver.quit()
print(f"[END] Downloaded elements: {downloaded}")
