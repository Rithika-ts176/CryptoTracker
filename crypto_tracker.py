# crypto_tracker.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import Bypython
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# ✅ Setup Chrome WebDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # uncomment if you don’t want browser window
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ✅ Open CoinMarketCap
url = "https://coinmarketcap.com/"
driver.get(url)

try:
    # Wait for the table to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    # ✅ Scrape top 10 coins
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")[:10]
    data = []

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        coin_name = columns[2].text.split("\n")[0]
        price = columns[3].text
        change_24h = columns[4].text
        market_cap = columns[7].text

        data.append({
            "Coin": coin_name,
            "Price": price,
            "24h Change": change_24h,
            "Market Cap": market_cap,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    # ✅ Save to CSV
    df = pd.DataFrame(data)
    df.to_csv("crypto_prices.csv", index=False)

    print("✅ Data successfully scraped and saved to crypto_prices.csv")

except Exception as e:
    print("⚠️ Error during scraping:", e)

finally:
    driver.quit()

