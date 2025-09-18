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

# # Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# # Ignore SSL errors
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--ignore-ssl-errors')

# # Use WebDriver Manager to automatically handle ChromeDriver
# service = Service(ChromeDriverManager().install())

# # Initialize Chrome driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

# def scrape_business_integrator():
#     base_url = "https://sabusinessintegrator.co.za"
#     start_url = "https://sabusinessintegrator.co.za/all-listings/?directory_type=general"
    
#     all_business_data = []
#     current_url = start_url
#     max_pages = 100  # Safety limit to prevent infinite loops
    
#     try:
#         for page_num in range(1, max_pages + 1):
#             print(f"Scraping page {page_num}: {current_url}")
            
#             try:
#                 # Navigate to the page
#                 driver.get(current_url)
                
#                 # Wait for listings to load
#                 WebDriverWait(driver, 15).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, "directorist-listing-single"))
#                 )
                
#                 # Find all business listing containers
#                 business_listings = driver.find_elements(By.CLASS_NAME, "directorist-listing-single")
#                 print(f"Found {len(business_listings)} business listings on this page")
                
#                 for listing in business_listings:
#                     try:
#                         business_data = extract_business_data(listing)
#                         if business_data:  # Only add if we found some data
#                             all_business_data.append(business_data)
                            
#                     except Exception as e:
#                         print(f"Error processing a business listing: {e}")
#                         continue
                
#             except Exception as e:
#                 print(f"Error loading page {current_url}: {e}")
#                 # Try to continue to next page anyway
            
#             # Check for next page
#             try:
#                 next_button = driver.find_element(By.CSS_SELECTOR, "a.next.page-numbers")
#                 next_url = next_button.get_attribute("href")
#                 if next_url and next_url != current_url:
#                     current_url = next_url
#                     print(f"Next page found: {current_url}")
#                 else:
#                     print("No more pages or reached the end")
#                     break
#             except Exception as e:
#                 print("No next page button found or error locating it:", e)
#                 # Try alternative selectors for next page
#                 try:
#                     next_buttons = driver.find_elements(By.CSS_SELECTOR, "a.page-numbers")
#                     for button in next_buttons:
#                         if "next" in button.text.lower() or "»" in button.text:
#                             next_url = button.get_attribute("href")
#                             if next_url and next_url != current_url:
#                                 current_url = next_url
#                                 print(f"Next page found via alternative selector: {current_url}")
#                                 break
#                     else:
#                         print("No more pages available")
#                         break
#                 except:
#                     print("Could not find any next page navigation")
#                     break
                
#             # Add a delay to be respectful to the server
#             time.sleep(2)
            
#     except Exception as e:
#         print(f"An error occurred during scraping: {e}")
    
#     return all_business_data

# def extract_business_data(listing):
#     """Extract business data from a listing element"""
#     business_data = {
#         'Name': 'Not available',
#         'Phone': 'Not available',
#         'Email': 'Not available',
#         'Website': 'Not available',
#         'Category': 'Not available',
#         'Listing_URL': 'Not available',
#         'Date_Posted': 'Not available'
#     }
    
#     try:
#         # Extract business name
#         try:
#             name_element = listing.find_element(By.CSS_SELECTOR, "h2.directorist-listing-title a")
#             business_data['Name'] = name_element.text.strip()
#             business_data['Listing_URL'] = name_element.get_attribute("href")
#         except:
#             pass
        
#         # Extract phone number
#         try:
#             phone_element = listing.find_element(By.CLASS_NAME, "directorist-listing-card-phone")
#             phone_link = phone_element.find_element(By.TAG_NAME, "a")
#             business_data['Phone'] = phone_link.text.strip()
#         except:
#             # Try alternative approach if the first one fails
#             try:
#                 phone_text = listing.find_element(By.CLASS_NAME, "directorist-listing-card-phone").text
#                 # Extract phone number using regex
#                 phone_match = re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', phone_text)
#                 if phone_match:
#                     business_data['Phone'] = phone_match.group(0).strip()
#             except:
#                 pass
        
#         # Extract email (if available in the listing)
#         try:
#             # Look for email patterns in the text
#             listing_text = listing.text
#             email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', listing_text)
#             if email_match:
#                 business_data['Email'] = email_match.group(0).strip()
#         except:
#             pass
        
#         # Extract category
#         try:
#             category_element = listing.find_element(By.CSS_SELECTOR, ".directorist-listing-category a")
#             business_data['Category'] = category_element.text.strip()
#         except:
#             pass
        
#         # Extract date posted
#         try:
#             date_element = listing.find_element(By.CLASS_NAME, "directorist-listing-card-posted-on")
#             date_span = date_element.find_element(By.TAG_NAME, "span")
#             business_data['Date_Posted'] = date_span.text.strip()
#         except:
#             pass
        
#         # Extract website (from the main link if it's external)
#         try:
#             if business_data['Listing_URL'] != 'Not available':
#                 listing_url = business_data['Listing_URL']
#                 if "sabusinessintegrator.co.za" not in listing_url:
#                     business_data['Website'] = listing_url
#         except:
#             pass
        
#         # Print success for debugging
#         if business_data['Name'] != 'Not available':
#             print(f"Extracted: {business_data['Name']} - {business_data['Phone']}")
        
#     except Exception as e:
#         print(f"Error extracting business data: {e}")
    
#     return business_data

# # Run the scraping function
# print("Starting scraping process for sabusinessintegrator.co.za...")
# business_data = scrape_business_integrator()

# # Save to Excel and CSV
# if business_data:
#     df = pd.DataFrame(business_data)
    
#     # Save to Excel
#     df.to_excel('sabusinessintegrator_contacts.xlsx', index=False)
    
#     # Save to CSV
#     df.to_csv('sabusinessintegrator_contacts.csv', index=False)
    
#     print(f"Successfully extracted {len(business_data)} business records.")
    
#     # Show summary
#     phones_found = len([b for b in business_data if b['Phone'] != 'Not available'])
#     emails_found = len([b for b in business_data if b['Email'] != 'Not available'])
    
#     print(f"Businesses with phone numbers: {phones_found}")
#     print(f"Businesses with emails: {emails_found}")
#     print(f"Data saved to sabusinessintegrator_contacts.xlsx and sabusinessintegrator_contacts.csv")
    
# else:
#     print("No business data was extracted.")

# # Close the driver
# driver.quit()
# print("Scraping completed!")



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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

# Ignore SSL errors
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

# Use WebDriver Manager to automatically handle ChromeDriver
service = Service(ChromeDriverManager().install())

# Initialize Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_sabusinessdirectories():
    url = "https://sabusinessdirectories.com/limpopo/"
    
    all_business_data = []
    
    try:
        print(f"Scraping page: {url}")
        
        # Navigate to the page
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "elementor-widget-container"))
        )
        
        # Find all text editor widgets that contain business information
        text_widgets = driver.find_elements(By.CLASS_NAME, "elementor-widget-text-editor")
        print(f"Found {len(text_widgets)} text editor widgets")
        
        # Find all heading elements that might contain business names
        headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6, .elementor-heading-title")
        
        # Create a mapping of elements to their potential business names
        business_elements = []
        
        for widget in text_widgets:
            try:
                text_content = widget.text.strip()
                # Check if this looks like a business contact block
                if any(keyword in text_content for keyword in 
                      ['Telephone', 'Fax', 'Cell', 'Address', 'Email', 'Website', 'Services']):
                    
                    # Find the closest heading above this widget that might be the business name
                    business_name = find_business_name(widget, headings)
                    
                    business_elements.append({
                        'element': widget,
                        'name': business_name
                    })
            except:
                continue
        
        print(f"Found {len(business_elements)} business contact blocks")
        
        for business_info in business_elements:
            try:
                business_data = extract_business_data(business_info['element'])
                business_data['Name'] = business_info['name']
                
                if business_data['Name'] != 'Not available' or any(
                    business_data[key] != 'Not available' for key in 
                    ['Telephone', 'Fax', 'Cell', 'Email']
                ):
                    all_business_data.append(business_data)
                    print(f"Extracted: {business_data['Name']} - {business_data['Telephone']}")
                    
            except Exception as e:
                print(f"Error processing a business container: {e}")
                continue
                
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    return all_business_data

def find_business_name(widget, headings):
    """Find the business name by looking for the closest heading element"""
    try:
        # Get the location of the current widget
        widget_location = widget.location['y']
        
        # Find the closest heading above this widget
        closest_heading = None
        min_distance = float('inf')
        
        for heading in headings:
            try:
                heading_location = heading.location['y']
                if heading_location < widget_location:  # Heading is above the widget
                    distance = widget_location - heading_location
                    if distance < min_distance:
                        min_distance = distance
                        closest_heading = heading
            except:
                continue
        
        if closest_heading:
            name = closest_heading.text.strip()
            # Filter out generic headings
            if name and not any(generic in name.lower() for generic in 
                              ['gauteng', 'directory', 'business', 'welcome', 'home']):
                return name
        
        # Alternative approach: look for strong text in the widget itself
        try:
            strong_elements = widget.find_elements(By.TAG_NAME, "strong")
            for strong in strong_elements:
                text = strong.text.strip()
                if (text and not any(keyword in text.lower() for keyword in 
                                   ['telephone', 'fax', 'cell', 'address', 'email', 'website', 'services']) and
                    len(text) > 3 and len(text) < 50):  # Reasonable name length
                    return text
        except:
            pass
            
    except Exception as e:
        print(f"Error finding business name: {e}")
    
    return "Not available"

def extract_business_data(container):
    """Extract business data from a container element"""
    business_data = {
        'Name': 'Not available',
        'Telephone': 'Not available',
        'Fax': 'Not available',
        'Cell': 'Not available',
        'Address': 'Not available',
        'Email': 'Not available',
        'Website': 'Not available',
        'Services': 'Not available'
    }
    
    try:
        # Get the text content
        text_content = container.text.strip()
        
        # Skip empty containers
        if not text_content or len(text_content) < 20:
            return business_data
        
        # Extract telephone number
        try:
            tel_match = re.search(r'Telephone Number[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if tel_match:
                business_data['Telephone'] = tel_match.group(1).strip()
        except:
            pass
        
        # Extract fax number
        try:
            fax_match = re.search(r'Fax Number[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if fax_match:
                business_data['Fax'] = fax_match.group(1).strip()
        except:
            pass
        
        # Extract cell number
        try:
            cell_match = re.search(r'Cell Number[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if cell_match:
                business_data['Cell'] = cell_match.group(1).strip()
        except:
            pass
        
        # Extract physical address
        try:
            addr_match = re.search(r'Physical Address[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if addr_match:
                business_data['Address'] = addr_match.group(1).strip()
        except:
            pass
        
        # Extract email addresses
        try:
            email_match = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_content)
            if email_match:
                business_data['Email'] = ', '.join(email_match)
        except:
            pass
        
        # Extract website
        try:
            website_match = re.search(r'Website Address[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if website_match:
                business_data['Website'] = website_match.group(1).strip()
            else:
                # Try to find website URLs directly
                url_match = re.search(r'www\.[^\s]+|\bhttps?://[^\s]+', text_content)
                if url_match:
                    business_data['Website'] = url_match.group(0).strip()
        except:
            pass
        
        # Extract services provided
        try:
            services_match = re.search(r'Services Provided[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if services_match:
                business_data['Services'] = services_match.group(1).strip()
        except:
            pass
        
    except Exception as e:
        print(f"Error extracting business data: {e}")
    
    return business_data

# Run the scraping function
print("Starting scraping process for sabusinessdirectories.com...")
business_data = scrape_sabusinessdirectories()

# Save to Excel and CSV
if business_data:
    df = pd.DataFrame(business_data)
    
    # Save to Excel
    df.to_excel('sabusinessdirectories_contacts.xlsx', index=False)
    
    # Save to CSV
    df.to_csv('sabusinessdirectories_contacts.csv', index=False)
    
    print(f"Successfully extracted {len(business_data)} business records.")
    
    # Show summary
    telephones_found = len([b for b in business_data if b['Telephone'] != 'Not available'])
    cells_found = len([b for b in business_data if b['Cell'] != 'Not available'])
    emails_found = len([b for b in business_data if b['Email'] != 'Not available'])
    
    print(f"Businesses with telephone numbers: {telephones_found}")
    print(f"Businesses with cell numbers: {cells_found}")
    print(f"Businesses with emails: {emails_found}")
    print(f"Data saved to sabusinessdirectories_contacts.xlsx and sabusinessdirectories_contacts.csv")
    
else:
    print("No business data was extracted.")

# Close the driver
driver.quit()
print("Scraping completed!")