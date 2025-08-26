from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Path to your chromedriver.exe
service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # adjust path if needed

# Initialize Chrome driver
driver = webdriver.Chrome(service=service)

# Open Google search URL
url = "https://www.google.com/search?tbm=lcl&q=law+firms+in+gauteng"
driver.get(url)

time.sleep(5)  # wait for page to load

# Wait up to 10 seconds for phone numbers to appear
spans = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@aria-label,'Call phone number')]"))
)

phone_numbers = []
for span in spans:
    label = span.get_attribute("aria-label")
    number = label.replace("Call phone number ", "").strip()
    phone_numbers.append(number)

# Save to Excel
df = pd.DataFrame(phone_numbers, columns=['Phone Number'])
df.to_excel('law_firm_phones.xlsx', index=False)
print("✅ Phone numbers saved to law_firm_phones.xlsx")

driver.quit()

