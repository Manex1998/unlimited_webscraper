from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import re

def setup_driver():
    """Set up Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Remove this line if you want to see the browser
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_bestdirectory_selenium():
    base_url = "https://www.bestdirectory.co.za"
    main_url = "https://www.bestdirectory.co.za/business-directory-small-business.html"
    
    driver = setup_driver()
    business_data = []
    
    try:
        print("Loading main directory page...")
        driver.get(main_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "views-row"))
        )
        
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Save the actual HTML for debugging
        with open('selenium_debug.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("Saved page content to selenium_debug.html")
        
        # Find business listings
        business_links = []
        views_rows = soup.find_all('div', class_=re.compile(r'views-row'))
        
        print(f"Found {len(views_rows)} business listings")
        
        for i, row in enumerate(views_rows):
            try:
                # Find the business title link
                title_link = row.find('h3', class_='title').find('a')
                if title_link and title_link.get('href'):
                    href = title_link['href']
                    full_url = base_url + href if href.startswith('/') else base_url + '/' + href
                    
                    if full_url not in business_links:
                        business_links.append(full_url)
                        print(f"{i+1}. {title_link.get_text().strip()}")
            except Exception as e:
                print(f"Error processing row {i+1}: {e}")
                continue
        
        print(f"\nTotal business links found: {len(business_links)}")
        
        # Scrape individual business pages
        for i, link in enumerate(business_links[:5], 1):  # Limit to 5 for testing
            print(f"\nProcessing business {i}/{len(business_links)}: {link}")
            
            try:
                # Navigate to business page
                driver.get(link)
                
                # Wait for page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                time.sleep(2)  # Additional wait for content to load
                
                # Get page source
                biz_page_source = driver.page_source
                biz_soup = BeautifulSoup(biz_page_source, 'html.parser')
                
                # Extract business name
                business_name = "N/A"
                title_elem = biz_soup.find('h1', class_='title')
                if title_elem:
                    business_name = title_elem.get_text().strip()
                
                # Extract phone number
                phone_number = "N/A"
                phone_div = biz_soup.find('div', class_='field_listing_primary_number')
                
                if phone_div:
                    phone_content = phone_div.find('div', class_='field-content')
                    if phone_content:
                        phone_number = phone_content.get_text().strip()
                
                # Extract address
                address = "N/A"
                address_div = biz_soup.find('div', class_='field_listing_street_address')
                if address_div:
                    address_content = address_div.find('div', class_='field-content')
                    if address_content:
                        address = address_content.get_text().strip()
                
                business_data.append({
                    'name': business_name,
                    'phone': phone_number,
                    'address': address,
                    'url': link
                })
                
                print(f"✓ {business_name}")
                print(f"  Phone: {phone_number}")
                print(f"  Address: {address}")
                
            except Exception as e:
                print(f"✗ Error processing {link}: {e}")
                continue
        
        # Save results to CSV
        if business_data:
            with open('business_phones_selenium.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'phone', 'address', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for business in business_data:
                    writer.writerow(business)
            
            print(f"\n✓ Successfully saved {len(business_data)} businesses to business_phones_selenium.csv")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()
    
    return business_data

# Alternative simpler version without headless mode (visible browser)
def scrape_bestdirectory_visible():
    """Version with visible browser for debugging"""
    chrome_options = Options()
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Opening browser...")
        driver.get("https://www.bestdirectory.co.za/business-directory-small-business.html")
        
        print("Page loaded. Check if you can see the business listings in the browser.")
        print("The browser will close automatically in 30 seconds...")
        time.sleep(30)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run full scraper (headless)")
    print("2. Test browser visibility")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        data = scrape_bestdirectory_selenium()
        
        # Print summary
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        print(f"Total businesses processed: {len(data)}")
        phones_found = len([b for b in data if b['phone'] != 'N/A'])
        print(f"Phone numbers found: {phones_found}")
        
    elif choice == "2":
        scrape_bestdirectory_visible()
    else:
        print("Invalid choice")