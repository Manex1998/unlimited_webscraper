from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re

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
    url = "https://www.google.com/search?tbm=lcl&q=construction+firms+in+gauteng"
    print("Navigating to Google search...")
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(5)
    
    # Check if we need to accept cookies
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[contains(., 'Accept all') or contains(., 'I agree')]")
        cookie_button.click()
        print("Accepted cookies")
        time.sleep(2)
    except:
        print("No cookie consent button found")
    
    # Scroll to load more results
    print("Scrolling to load more results...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    
    while scroll_attempts < 5:  # Limit to 5 scroll attempts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_attempts += 1

    # Find all business listings
    print("Looking for business listings...")
    
    # Try different selectors for business cards
    business_selectors = [
        "//div[contains(@class, 'rllt__details')]",
        "//div[contains(@class, 'VkpGBb')]",
        "//div[@class='rllt__details']",
        "//div[@class='VkpGBb']",
        "//div[contains(@class, 'section-result')]"
    ]
    
    businesses = []
    
    for selector in business_selectors:
        try:
            businesses = driver.find_elements(By.XPATH, selector)
            if businesses:
                print(f"Found {len(businesses)} businesses using selector: {selector}")
                break
        except:
            continue
    
    if not businesses:
        print("No business listings found with standard selectors. Trying fallback...")
        # Try to find any div that might contain business info
        businesses = driver.find_elements(By.XPATH, "//div[.//h3]")
        print(f"Found {len(businesses)} potential business elements")
    
    construction_firms = []
    
    for i, business in enumerate(businesses):
        try:
            # Extract business name
            name = "Unknown"
            try:
                name_elements = business.find_elements(By.XPATH, ".//h3 | .//div[contains(@class, 'title')] | .//span[contains(@class, 'title')]")
                if name_elements:
                    name = name_elements[0].text.strip()
            except:
                pass
            
            # Extract address
            address = "Not available"
            try:
                address_elements = business.find_elements(By.XPATH, ".//span[contains(@class, 'address')] | .//div[contains(@class, 'address')] | .//span[contains(text(), 'South Africa')]")
                if address_elements:
                    address = address_elements[0].text.strip()
            except:
                pass
            
            # Extract phone number using multiple strategies
            phone = "Not available"
            try:
                # Look for phone numbers in the text
                full_text = business.text
                phone_patterns = [
                    r'(\+27\s?\d{2}\s?\d{3}\s?\d{4})',  # South Africa format +27
                    r'(\(\d{3}\)\s?\d{3}-\d{4})',       # US format (123) 456-7890
                    r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4})',  # Standard phone
                    r'(\d{3}\s\d{3}\s\d{4})',           # 123 456 7890
                ]
                
                for pattern in phone_patterns:
                    matches = re.findall(pattern, full_text)
                    if matches:
                        phone = matches[0]
                        break
            except:
                pass
            
            # Extract rating if available
            rating = "Not rated"
            try:
                rating_elements = business.find_elements(By.XPATH, ".//span[contains(@class, 'rating')] | .//div[contains(@class, 'rating')]")
                if rating_elements:
                    rating = rating_elements[0].text.strip()
            except:
                pass
            
            # Extract website if available
            website = "Not available"
            try:
                website_elements = business.find_elements(By.XPATH, ".//a[contains(@href, 'http')]")
                if website_elements:
                    for element in website_elements:
                        href = element.get_attribute('href')
                        if href and ('google.com' not in href and 'maps.google.com' not in href):
                            website = href
                            break
            except:
                pass
            
            construction_firms.append({
                'Name': name,
                'Address': address,
                'Phone': phone,
                'Rating': rating,
                'Website': website
            })
            
            print(f"Processed business {i+1}: {name}")
            
        except Exception as e:
            print(f"Error processing business {i+1}: {str(e)}")
            continue

    # Save to Excel
    if construction_firms:
        df = pd.DataFrame(construction_firms)
        df.to_excel('construction_firms_gauteng.xlsx', index=False)
        print(f"✅ {len(construction_firms)} construction saved to construction_firms_gauteng.xlsx")
        
        # Also save as CSV for easier viewing
        df.to_csv('construction_firms_gauteng.csv', index=False)
        print(f"✅ CSV version saved as construction_firms_gauteng.csv")
    else:
        print("❌ No construction firms found. The page structure might have changed significantly.")
        
        # Save page source for debugging
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Page source saved to page_source.html for debugging")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()