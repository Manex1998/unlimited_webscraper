from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Path to your chromedriver.exe
service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# Initialize Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Google search URL
    url = "https://www.google.com/search?tbm=lcl&q=law+firms+in+gauteng"
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(5)

    # Scroll to load more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Try multiple selectors for phone numbers
    phone_selectors = [
        "//span[contains(@aria-label, 'Call phone number')]",
        "//span[contains(@aria-label, 'Phone:')]",
        "//div[contains(text(), '+') and string-length(text()) > 8]",
        "//a[contains(@href, 'tel:')]"
    ]

    phone_numbers = []
    
    for selector in phone_selectors:
        try:
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, selector))
            )
            for element in elements:
                if selector == "//a[contains(@href, 'tel:')]":
                    phone_number = element.get_attribute("href").replace("tel:", "")
                else:
                    phone_number = element.text
                
                # Clean up the phone number
                phone_number = ''.join(filter(str.isdigit, phone_number))
                if len(phone_number) >= 9:  # Valid phone number check
                    phone_numbers.append(phone_number)
            break  # Stop if we found elements with this selector
        except:
            continue  # Try next selector if this one fails

    # If no phone numbers found, try a different approach
    if not phone_numbers:
        print("No phone numbers found with direct selectors. Trying alternative approach...")
        
        # Look for business cards and extract information
        business_cards = driver.find_elements(By.CSS_SELECTOR, ".rllt__details")
        for card in business_cards:
            card_text = card.text
            # Look for phone number patterns in the text
            lines = card_text.split('\n')
            for line in lines:
                if any(char.isdigit() for char in line) and ('+' in line or 'phone' in line.lower() or 'tel' in line.lower()):
                    phone_number = ''.join(filter(str.isdigit, line))
                    if len(phone_number) >= 9:
                        phone_numbers.append(phone_number)
                        break

    # Remove duplicates while preserving order
    seen = set()
    unique_phone_numbers = []
    for num in phone_numbers:
        if num not in seen:
            seen.add(num)
            unique_phone_numbers.append(num)

    # Save to Excel
    if unique_phone_numbers:
        df = pd.DataFrame(unique_phone_numbers, columns=['Phone Number'])
        df.to_excel('law_firm_phones.xlsx', index=False)
        print(f"✅ {len(unique_phone_numbers)} phone numbers saved to law_firm_phones.xlsx")
    else:
        print("❌ No phone numbers found. The page structure might have changed.")
        
        # Save page source for debugging
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Page source saved to page_source.html for debugging")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    
finally:
    driver.quit()