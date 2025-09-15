# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time
# import re

# # Set up Chrome options with better error handling
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# # Ignore SSL errors
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--ignore-ssl-errors')
# chrome_options.add_argument('--allow-running-insecure-content')

# # Use WebDriver Manager to automatically handle ChromeDriver
# service = Service(ChromeDriverManager().install())

# # Initialize Chrome driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

# def scrape_phone_numbers():
#     base_url = "https://www.growsa.africa"
#     start_url = "https://www.growsa.africa/sa-directory/all/page1?sort=-link_modified"
    
#     all_business_data = []
#     current_url = start_url
#     max_pages = 50  # Limit to prevent infinite loops
    
#     try:
#         for page_num in range(1, max_pages + 1):
#             print(f"Scraping page {page_num}: {current_url}")
            
#             try:
#                 # Navigate to the page with retry logic
#                 driver.get(current_url)
                
#                 # Wait for the page to load
#                 WebDriverWait(driver, 15).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, "mt-ls-entry"))
#                 )
                
#                 # Find all business listing containers
#                 business_containers = driver.find_elements(By.CLASS_NAME, "mt-ls-entry")
#                 print(f"Found {len(business_containers)} business listings")
                
#                 for container in business_containers:
#                     try:
#                         business_data = extract_business_data(container)
#                         if business_data:  # Only add if we found some data
#                             all_business_data.append(business_data)
                            
#                     except Exception as e:
#                         print(f"Error processing a business container: {e}")
#                         continue
                
#             except Exception as e:
#                 print(f"Error loading page {current_url}: {e}")
#                 # Try to continue to next page anyway
            
#             # Check for next page
#             try:
#                 next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
#                 next_url = next_button.get_attribute("href")
#                 if next_url and next_url != current_url:
#                     current_url = next_url if next_url.startswith("http") else base_url + next_url
#                 else:
#                     print("No more pages or reached the end")
#                     break
#             except:
#                 print("No next page button found")
#                 break
                
#             # Add a delay to be respectful to the server
#             time.sleep(3)
            
#     except Exception as e:
#         print(f"An error occurred during scraping: {e}")
    
#     return all_business_data

# def extract_business_data(container):
#     """Extract business data from a container element"""
#     business_data = {
#         'Name': 'Not available',
#         'Phone': 'Not available',
#         'Email': 'Not available',
#         'Location': 'Not available',
#         'Category': 'Not available',
#         'Website': 'Not available'
#     }
    
#     try:
#         # Extract business name
#         try:
#             name_element = container.find_element(By.TAG_NAME, "h2")
#             business_data['Name'] = name_element.text.strip()
#         except:
#             pass
        
#         # Try to find the misc fields container
#         try:
#             misc_container = container.find_element(By.CLASS_NAME, "mt-ls-fields-misc")
            
#             # Extract phone number
#             try:
#                 phone_elements = misc_container.find_elements(By.XPATH, ".//div[contains(@class, 'mfieldtype_coretelephone')]")
#                 if phone_elements:
#                     phone_output = phone_elements[0].find_element(By.CLASS_NAME, "output")
#                     business_data['Phone'] = phone_output.text.strip()
#             except:
#                 pass
            
#             # Extract email
#             try:
#                 email_elements = misc_container.find_elements(By.XPATH, ".//div[contains(@class, 'mfieldtype_coreemail')]")
#                 if email_elements:
#                     email_anchor = email_elements[0].find_element(By.TAG_NAME, "a")
#                     business_data['Email'] = email_anchor.text.strip()
#             except:
#                 pass
            
#             # Extract location
#             try:
#                 location_elements = misc_container.find_elements(By.XPATH, ".//div[contains(@class, 'mfieldtype_selectlist')]")
#                 if location_elements:
#                     location_output = location_elements[0].find_element(By.CLASS_NAME, "output")
#                     business_data['Location'] = location_output.text.strip()
#             except:
#                 pass
            
#             # Extract category/keywords
#             try:
#                 category_elements = misc_container.find_elements(By.XPATH, ".//div[contains(@class, 'mfieldtype_mtags')]")
#                 if category_elements:
#                     category_output = category_elements[0].find_element(By.CLASS_NAME, "output")
#                     business_data['Category'] = category_output.text.strip()
#             except:
#                 pass
            
#         except:
#             pass
        
#         # Extract website if available
#         try:
#             links = container.find_elements(By.TAG_NAME, "a")
#             for link in links:
#                 href = link.get_attribute("href")
#                 if href and "http" in href and "growsa.africa" not in href:
#                     business_data['Website'] = href
#                     break
#         except:
#             pass
        
#         # Print success for debugging
#         if business_data['Name'] != 'Not available' or business_data['Phone'] != 'Not available':
#             print(f"Extracted: {business_data['Name']} - {business_data['Phone']}")
        
#     except Exception as e:
#         print(f"Error extracting business data: {e}")
    
#     return business_data

# # Run the scraping function
# print("Starting scraping process...")
# business_data = scrape_phone_numbers()

# # Save to Excel and CSV
# if business_data:
#     df = pd.DataFrame(business_data)
#     df.to_excel('business_phone_numbers.xlsx', index=False)
#     df.to_csv('business_phone_numbers.csv', index=False)
#     print(f"Successfully extracted {len(business_data)} business records.")
    
#     # Show summary
#     phones_found = len([b for b in business_data if b['Phone'] != 'Not available'])
#     print(f"Businesses with phone numbers: {phones_found}")
#     print(f"Businesses with emails: {len([b for b in business_data if b['Email'] != 'Not available'])}")
    
# else:
#     print("No business data was extracted.")

# # Close the driver
# driver.quit()
# print("Scraping completed!")


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# import random
# import re

# # ✅ Rotate user agents
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
#     "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/118.0",
# ]

# BASE_URL = "https://www.growsa.africa"
# START_URL = f"{BASE_URL}/sa-directory/all/page1?sort=-link_modified"

# def fetch_page(url):
#     """Fetch a page safely with retries"""
#     for attempt in range(3):
#         try:
#             headers = {"User-Agent": random.choice(USER_AGENTS)}
#             resp = requests.get(url, headers=headers, timeout=15, verify=False)  # ignore SSL issues
#             if resp.status_code == 200:
#                 return resp.text
#         except Exception as e:
#             print(f"⚠️ Error fetching {url} (attempt {attempt+1}): {e}")
#             time.sleep(3)
#     return None

# def extract_business_data(container):
#     """Extract details from a single business entry"""
#     business = {
#         'Name': 'Not available',
#         'Phone': 'Not available',
#         'Email': 'Not available',
#         'Location': 'Not available',
#         'Category': 'Not available',
#         'Website': 'Not available'
#     }

#     # Business Name
#     name_tag = container.find("h2")
#     if name_tag:
#         business["Name"] = name_tag.get_text(strip=True)

#     # Misc fields (phone, email, etc.)
#     misc = container.find("div", class_="mt-ls-fields-misc")
#     if misc:
#         # Phone
#         phone = misc.find("div", class_=re.compile("mfieldtype_coretelephone"))
#         if phone:
#             out = phone.find("div", class_="output")
#             if out:
#                 business["Phone"] = out.get_text(strip=True)

#         # Email
#         email = misc.find("div", class_=re.compile("mfieldtype_coreemail"))
#         if email:
#             a = email.find("a")
#             if a:
#                 business["Email"] = a.get_text(strip=True)

#         # Location
#         loc = misc.find("div", class_=re.compile("mfieldtype_selectlist"))
#         if loc:
#             out = loc.find("div", class_="output")
#             if out:
#                 business["Location"] = out.get_text(strip=True)

#         # Category
#         cat = misc.find("div", class_=re.compile("mfieldtype_mtags"))
#         if cat:
#             out = cat.find("div", class_="output")
#             if out:
#                 business["Category"] = out.get_text(strip=True)

#     # External website
#     links = container.find_all("a", href=True)
#     for link in links:
#         href = link["href"]
#         if href.startswith("http") and "growsa.africa" not in href:
#             business["Website"] = href
#             break

#     return business

# def scrape_directory(max_pages=50):
#     """Scrape the business directory"""
#     results = []
#     current_url = START_URL

#     for page_num in range(1, max_pages + 1):
#         print(f"\n📄 Scraping page {page_num}: {current_url}")
#         html = fetch_page(current_url)
#         if not html:
#             print("❌ Could not load page, stopping...")
#             break

#         soup = BeautifulSoup(html, "html.parser")
#         business_containers = soup.find_all("div", class_="mt-ls-entry")
#         print(f"✅ Found {len(business_containers)} businesses")

#         for container in business_containers:
#             data = extract_business_data(container)
#             results.append(data)

#         # Find next page
#         next_btn = soup.select_one("a.next")
#         if next_btn and next_btn.get("href"):
#             next_url = next_btn["href"]
#             current_url = next_url if next_url.startswith("http") else BASE_URL + next_url
#         else:
#             print("🚪 No more pages.")
#             break

#         time.sleep(random.uniform(2, 5))  # polite delay

#     return results

# # --- Run scraper ---
# print("🚀 Starting scraping...")
# data = scrape_directory(max_pages=50)

# # Save results
# if data:
#     df = pd.DataFrame(data)
#     df.to_excel("business_phone_numbers.xlsx", index=False)
#     df.to_csv("business_phone_numbers.csv", index=False)
#     print(f"\n✅ Saved {len(data)} businesses")
#     print(f"☎️ With phone numbers: {len([d for d in data if d['Phone'] != 'Not available'])}")
#     print(f"📧 With emails: {len([d for d in data if d['Email'] != 'Not available'])}")
# else:
#     print("⚠️ No data scraped.")


# import requests

# url = "https://www.growsa.africa/sa-directory/all/page1?sort=-link_modified"
# html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
# print(html[:2000])  # print first 2000 chars



# import requests
# from bs4 import BeautifulSoup

# url = "https://www.growsa.africa/sa-directory/all/page1?sort=-link_modified"
# headers = {"User-Agent": "Mozilla/5.0"}
# resp = requests.get(url, headers=headers, verify=False)
# soup = BeautifulSoup(resp.text, "html.parser")

# # Debug: find any business containers
# for div in soup.find_all("div", class_=True)[:20]:
#     print(div.get("class"))



import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# Headers to avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

# CSV setup
OUTPUT_FILE = "growsa_businesses.csv"
fields = ["Name", "Category", "Phone", "Email", "Description"]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    # Loop through first 100 pages
    for page in range(1, 101):
        url = f"https://www.growsa.africa/sa-directory/all/page{page}?sort=-link_modified"
        print(f"📄 Scraping page {page}: {url}")

        try:
            resp = requests.get(url, headers=HEADERS, verify=False, timeout=20)
            if resp.status_code != 200:
                print(f"⚠️ Failed to fetch page {page} (status {resp.status_code})")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            businesses = soup.select("div.listing-summary")

            print(f"✅ Found {len(businesses)} businesses")

            for biz in businesses:
                name = biz.select_one("h3 a span[itemprop='name']")
                category = biz.select_one("div.mt-ls-field.category span.output a")
                phone = biz.select_one("div.mfieldtype_coretelephone span.output")
                email = biz.select_one("div.mfieldtype_coreemail span.output a")
                desc = biz.select_one("p.mfieldtype_coredesc")

                writer.writerow({
                    "Name": name.get_text(strip=True) if name else "",
                    "Category": category.get_text(strip=True) if category else "",
                    "Phone": phone.get_text(strip=True) if phone else "",
                    "Email": email.get_text(strip=True) if email else "",
                    "Description": desc.get_text(strip=True) if desc else ""
                })

            # Random sleep to avoid blocking
            time.sleep(random.uniform(2, 5))

        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            continue

print(f"\n🎉 Scraping complete! Data saved to {OUTPUT_FILE}")



