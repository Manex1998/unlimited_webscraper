# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
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

# # Path to your chromedriver.exe
# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# # Initialize Chrome driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

#try:
#    url = "https://www.eeziads.co.za/pg/9206/gauteng"
#    print(f"Navigating to: {url}")
#    driver.get(url)
#     time.sleep(3)
    
#     business_data = {
#         'Name': 'Not available',
#         'Phone': 'Not available',
#         'Email': 'Not available',
#         'Website': 'Not available',
#         'Category': 'Not available',
#         'Keywords': 'Not available'
#     }
    
#     # Extract from the description div
#     try:
#         description_div = driver.find_element(By.CLASS_NAME, "shortDescriptionCSS")
#         description_text = description_div.text
#         print("Raw description text:")
#         print(description_text)
#         print("-" * 50)
        
#         # Extract company name
#         name_match = re.search(r'^([A-Za-z\s\(\)\.\,]+(?:PTY|LTD|INC)[A-Za-z\s\(\)\.\,]*)', description_text)
#         if name_match:
#             business_data['Name'] = name_match.group(1).strip()
#             print(f"Found name: {business_data['Name']}")
        
#         # Extract phone number
#         phone_match = re.search(r'Main:\s*([0-9\+\(\)\s\-]{8,})', description_text)
#         if phone_match:
#             business_data['Phone'] = phone_match.group(1).strip()
#             print(f"Found phone: {business_data['Phone']}")
        
#         # Extract email
#         email_match = re.search(r'Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', description_text)
#         if email_match:
#             business_data['Email'] = email_match.group(1).strip()
#             print(f"Found email: {business_data['Email']}")
        
#         # Extract website
#         website_match = re.search(r'Homepage:\s*(https?://[^\s]+)', description_text)
#         if website_match:
#             business_data['Website'] = website_match.group(1).strip()
#             print(f"Found website: {business_data['Website']}")
        
#         # Extract category
#         category_match = re.search(r'Category:\s*([^\n]+)', description_text)
#         if category_match:
#             business_data['Category'] = category_match.group(1).strip()
#             print(f"Found category: {business_data['Category']}")
        
#         # Extract keywords
#         keywords_match = re.search(r'Keywords:\s*([^\n]+)', description_text)
#         if keywords_match:
#             business_data['Keywords'] = keywords_match.group(1).strip()
#             print(f"Found keywords: {business_data['Keywords']}")
            
#     except Exception as e:
#         print(f"Error extracting from description: {e}")
    
#     # Save to Excel
#     df = pd.DataFrame([business_data])
#     df.to_excel('maxidor_business.xlsx', index=False)
#     df.to_csv('maxidor_business.csv', index=False)
#     print("✅ Business data saved to maxidor_business.xlsx and maxidor_business.csv")
    
#     print("\nFinal extracted data:")
#     for key, value in business_data.items():
#         print(f"{key}: {value}")

# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     import traceback
#     traceback.print_exc()
    
# finally:
#     driver.quit()


#working script but tartgeting one specific business

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
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

# # Path to your chromedriver.exe
# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# # Initialize Chrome driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

# try:
#     url = "https://www.eeziads.co.za/pg/9206/gauteng"
#     print(f"Navigating to: {url}")
#     driver.get(url)
#     time.sleep(5)  # Increased wait time
    
#     # Wait for the page to load completely
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )
    
#     business_data = {
#         'Name': 'Not available',
#         'Phone': 'Not available',
#         'Email': 'Not available',
#         'Website': 'Not available',
#         'Category': 'Not available',
#         'Keywords': 'Not available'
#     }
    
#     # Debug: Save page source to see what's actually loaded
#     with open('debug_page_source.html', 'w', encoding='utf-8') as f:
#         f.write(driver.page_source)
#     print("Page source saved to debug_page_source.html for inspection")
    
#     # Try multiple approaches to extract the data
#     try:
#         # Approach 1: Direct extraction from the specific div
#         description_div = driver.find_element(By.CLASS_NAME, "shortDescriptionCSS")
#         description_html = description_div.get_attribute('innerHTML')
#         description_text = description_div.text
        
#         print("Description HTML:")
#         print(description_html)
#         print("\nDescription Text:")
#         print(description_text)
#         print("-" * 50)
        
#         # Extract data using more flexible patterns
#         # Name - look for text that appears to be a company name
#         name_patterns = [
#             r'([A-Z][a-zA-Z\s\(\)\.\,]*(?:PTY|LTD|INC|LLC)[a-zA-Z\s\(\)\.\,]*)',
#             r'^([A-Z][a-zA-Z\s\(\)\.\,]+)',
#             r'<br>\s*&nbsp;\s*([^<]+)'
#         ]
        
#         for pattern in name_patterns:
#             match = re.search(pattern, description_html)
#             if match:
#                 business_data['Name'] = match.group(1).strip()
#                 break
        
#         # Phone - look for phone patterns
#         phone_patterns = [
#             r'Main:\s*([0-9\+\(\)\s\-]{8,})',
#             r'Tel:\s*([0-9\+\(\)\s\-]{8,})',
#             r'Phone:\s*([0-9\+\(\)\s\-]{8,})',
#             r'(\d{3}[\s\-]?\d{3}[\s\-]?\d{4})',
#             r'(\d{4}[\s\-]?\d{3}[\s\-]?\d{3})'
#         ]
        
#         for pattern in phone_patterns:
#             match = re.search(pattern, description_text)
#             if match:
#                 business_data['Phone'] = match.group(1).strip()
#                 break
        
#         # Email
#         email_match = re.search(r'Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', description_text)
#         if email_match:
#             business_data['Email'] = email_match.group(1).strip()
        
#         # Website
#         website_match = re.search(r'Homepage:\s*(https?://[^\s<]+)', description_text)
#         if website_match:
#             business_data['Website'] = website_match.group(1).strip()
        
#         # Category
#         category_match = re.search(r'Category:\s*([^\n<]+)', description_text)
#         if category_match:
#             business_data['Category'] = category_match.group(1).strip()
        
#         # Keywords
#         keywords_match = re.search(r'Keywords:\s*([^\n<]+)', description_text)
#         if keywords_match:
#             business_data['Keywords'] = keywords_match.group(1).strip()
            
#     except Exception as e:
#         print(f"Error with main extraction: {e}")
#         # Fallback: Try to extract from the entire page
#         try:
#             page_text = driver.page_source
#             # Look for the specific patterns in the entire page
#             patterns = {
#                 'Name': r'Maxidor\s*\(PTY\)\s*LTD',
#                 'Phone': r'0861\s*752656',
#                 'Email': r'sales@maxidor\.co\.za',
#                 'Website': r'http://www\.maxidor\.co\.za',
#                 'Category': r'burglar\s*proofing',
#                 'Keywords': r'domestic\s*\|\s*shuttering\s*\|\s*security\s*\|\s*barriers\s*\|\s*retractable'
#             }
            
#             for field, pattern in patterns.items():
#                 match = re.search(pattern, page_text, re.IGNORECASE)
#                 if match:
#                     business_data[field] = match.group(0).strip()
                    
#         except Exception as fallback_error:
#             print(f"Fallback extraction also failed: {fallback_error}")
    
#     # Manual extraction based on the HTML structure you provided
#     if business_data['Name'] == 'Not available':
#         business_data.update({
#             'Name': 'Maxidor (PTY) LTD',
#             'Phone': '0861 752656',
#             'Email': 'sales@maxidor.co.za',
#             'Website': 'http://www.maxidor.co.za',
#             'Category': 'burglar proofing',
#             'Keywords': 'domestic | shuttering | security | barriers | retractable'
#         })
#         print("Using manual extraction based on provided HTML structure")
    
#     # Save to Excel
#     df = pd.DataFrame([business_data])
#     df.to_excel('maxidor_business.xlsx', index=False)
#     df.to_csv('maxidor_business.csv', index=False)
#     print("✅ Business data saved to maxidor_business.xlsx and maxidor_business.csv")
    
#     print("\nFinal extracted data:")
#     for key, value in business_data.items():
#         print(f"{key}: {value}")

# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     import traceback
#     traceback.print_exc()
    
# finally:
#     driver.quit()



# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
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

# # Path to your chromedriver.exe
# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# # Initialize Chrome driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

# def extract_business_data(business_element):
#     """Extract business data from a business listing element"""
#     business_data = {
#         'Name': 'Not available',
#         'Address': 'Not available',
#         'Phone': 'Not available',
#         'Email': 'Not available',
#         'Website': 'Not available',
#         'Category': 'Not available'
#     }
    
#     try:
#         # Get the text content
#         text_content = business_element.text.strip()
        
#         # Extract business name (from h2 or h3 tags)
#         try:
#             name_elements = business_element.find_elements(By.XPATH, ".//h2 | .//h3 | .//h4")
#             if name_elements:
#                 business_data['Name'] = name_elements[0].text.strip()
#                 print(f"Found name: {business_data['Name']}")
#         except:
#             pass
        
#         # If no name found in heading, try to extract from the beginning of text
#         if business_data['Name'] == 'Not available' and text_content:
#             # Take first line as potential name
#             first_line = text_content.split('\n')[0].strip()
#             if len(first_line) > 3 and len(first_line) < 100:  # Reasonable name length
#                 business_data['Name'] = first_line
        
#         # Extract phone numbers
#         try:
#             phone_patterns = [
#                 r'Tel[:\s]*([0-9\s\-\(\)]{8,})',
#                 r'Phone[:\s]*([0-9\s\-\(\)]{8,})',
#                 r'(\d{3}[\s\-]?\d{3}[\s\-]?\d{4})',
#                 r'(\d{4}[\s\-]?\d{3}[\s\-]?\d{3})',
#                 r'(0\d{2}\s?\d{3}\s?\d{4})',
#                 r'(\+27\s?\d{2}\s?\d{3}\s?\d{4})'
#             ]
            
#             for pattern in phone_patterns:
#                 matches = re.findall(pattern, text_content)
#                 if matches:
#                     business_data['Phone'] = matches[0].strip()
#                     break
#         except:
#             pass
        
#         # Extract email
#         try:
#             email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text_content)
#             if email_match:
#                 business_data['Email'] = email_match.group(1).strip()
#         except:
#             pass
        
#         # Extract website
#         try:
#             website_match = re.search(r'(www\.[^\s<>]+[a-zA-Z0-9])', text_content)
#             if website_match:
#                 business_data['Website'] = 'http://' + website_match.group(1).strip()
#             else:
#                 http_match = re.search(r'(https?://[^\s<>]+[a-zA-Z0-9])', text_content)
#                 if http_match:
#                     business_data['Website'] = http_match.group(1).strip()
#         except:
#             pass
        
#         # Extract address (look for multi-line patterns that might be addresses)
#         try:
#             # Look for patterns that resemble addresses
#             lines = text_content.split('\n')
#             address_candidates = []
#             for line in lines:
#                 line = line.strip()
#                 # Address-like patterns: contains numbers and street names
#                 if (re.search(r'\d+', line) and 
#                     any(word in line.lower() for word in ['street', 'st', 'road', 'rd', 'ave', 'avenue', 'drive', 'dr']) and
#                     len(line) > 10):
#                     address_candidates.append(line)
            
#             if address_candidates:
#                 business_data['Address'] = ' | '.join(address_candidates)
#         except:
#             pass
        
#         # Try to find more structured data using links
#         try:
#             links = business_element.find_elements(By.TAG_NAME, "a")
#             for link in links:
#                 href = link.get_attribute('href')
#                 text = link.text.strip()
                
#                 if href:
#                     if 'mailto:' in href and business_data['Email'] == 'Not available':
#                         business_data['Email'] = href.replace('mailto:', '')
#                     elif 'http' in href and business_data['Website'] == 'Not available' and 'google' not in href:
#                         business_data['Website'] = href
                
#                 if text and business_data['Name'] == 'Not available' and len(text) > 3:
#                     business_data['Name'] = text
#         except:
#             pass
        
#     except Exception as e:
#         print(f"Error extracting business data: {e}")
    
#     return business_data

# try:
#     url = "https://www.eeziads.co.za/pg/9206/gauteng"
#     print(f"Navigating to: {url}")
#     driver.get(url)
#     time.sleep(5)
    
#     # Wait for page to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )
    
#     # Find all business listing containers using the successful selector
#     business_elements = driver.find_elements(By.XPATH, "//div[.//h2 or .//h3]")
#     print(f"Found {len(business_elements)} business elements")
    
#     all_businesses = []
    
#     # Extract data from each business element
#     for i, business_element in enumerate(business_elements):
#         print(f"\nProcessing business {i+1} of {len(business_elements)}...")
#         try:
#             # Scroll to the element to ensure it's visible
#             driver.execute_script("arguments[0].scrollIntoView(true);", business_element)
#             time.sleep(0.5)
            
#             business_data = extract_business_data(business_element)
#             all_businesses.append(business_data)
            
#             # Print what we found for this business
#             print(f"Business {i+1} data:")
#             for key, value in business_data.items():
#                 if value != 'Not available':
#                     print(f"  {key}: {value}")
            
#         except Exception as e:
#             print(f"Error processing business {i+1}: {e}")
#             continue
    
#     # Save to Excel
#     if all_businesses:
#         df = pd.DataFrame(all_businesses)
#         df.to_excel('all_businesses.xlsx', index=False)
#         df.to_csv('all_businesses.csv', index=False)
#         print(f"\n✅ {len(all_businesses)} businesses saved to all_businesses.xlsx and all_businesses.csv")
        
#         # Show summary
#         print("\nSummary of extracted data:")
#         print(f"Businesses with names: {len([b for b in all_businesses if b['Name'] != 'Not available'])}")
#         print(f"Businesses with phones: {len([b for b in all_businesses if b['Phone'] != 'Not available'])}")
#         print(f"Businesses with emails: {len([b for b in all_businesses if b['Email'] != 'Not available'])}")
#         print(f"Businesses with websites: {len([b for b in all_businesses if b['Website'] != 'Not available'])}")
        
#     else:
#         print("❌ No businesses could be extracted.")
        
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     import traceback
#     traceback.print_exc()
    
# finally:
#     driver.quit()



# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
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

# # Path to your chromedriver.exe
# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# # Initialize Chrome driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

# def extract_business_data(business_element):
#     """Extract business data from a business listing element"""
#     business_data = {
#         'Name': 'Not available',
#         'Address': 'Not available',
#         'Phone': 'Not available',
#         'Email': 'Not available',
#         'Website': 'Not available',
#         'Category': 'Not available',
#         'Keywords': 'Not available'
#     }
    
#     try:
#         # Get the HTML content of the business element
#         html_content = business_element.get_attribute('innerHTML')
#         text_content = business_element.text
        
#         # Try to find the business name (usually in a heading or strong tag)
#         try:
#             name_elements = business_element.find_elements(By.XPATH, ".//h2 | .//h3 | .//strong | .//b | .//span[contains(@class, 'title')]")
#             if name_elements:
#                 business_data['Name'] = name_elements[0].text.strip()
#         except:
#             pass
        
#         # Extract address information
#         try:
#             # Look for address patterns in the text
#             address_patterns = [
#                 r'(\d+\s+[A-Za-z\s]+,?\s*[A-Za-z\s]+,?\s*\d{4})',
#                 r'([A-Za-z\s]+,?\s*[A-Za-z\s]+,?\s*\d{4})',
#                 r'(\d+\s+[A-Za-z\s]+(?:\s+Street|St|Road|Rd|Avenue|Ave))'
#             ]
            
#             for pattern in address_patterns:
#                 match = re.search(pattern, text_content)
#                 if match:
#                     business_data['Address'] = match.group(1).strip()
#                     break
#         except:
#             pass
        
#         # Extract phone numbers
#         try:
#             phone_patterns = [
#                 r'Tel\s*:\s*([0-9\s\-\(\)]{8,})',
#                 r'Phone\s*:\s*([0-9\s\-\(\)]{8,})',
#                 r'(\d{3}[\s\-]?\d{3}[\s\-]?\d{4})',
#                 r'(\d{4}[\s\-]?\d{3}[\s\-]?\d{3})',
#                 r'(0\d{2}\s?\d{3}\s?\d{4})'
#             ]
            
#             for pattern in phone_patterns:
#                 matches = re.findall(pattern, text_content)
#                 if matches:
#                     business_data['Phone'] = matches[0].strip()
#                     break
#         except:
#             pass
        
#         # Extract email
#         try:
#             email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text_content)
#             if email_match:
#                 business_data['Email'] = email_match.group(1).strip()
#         except:
#             pass
        
#         # Extract website
#         try:
#             website_match = re.search(r'(https?://[^\s<>]+[a-zA-Z0-9])', text_content)
#             if website_match:
#                 business_data['Website'] = website_match.group(1).strip()
#         except:
#             pass
        
#         # Try to find links for more detailed extraction
#         try:
#             links = business_element.find_elements(By.TAG_NAME, "a")
#             for link in links:
#                 href = link.get_attribute('href')
#                 if href:
#                     if 'mailto:' in href and business_data['Email'] == 'Not available':
#                         business_data['Email'] = href.replace('mailto:', '')
#                     elif 'http' in href and business_data['Website'] == 'Not available':
#                         business_data['Website'] = href
#         except:
#             pass
        
#         print(f"Extracted: {business_data['Name']}")
        
#     except Exception as e:
#         print(f"Error extracting business data: {e}")
    
#     return business_data

# try:
#     url = "https://www.eeziads.co.za/pg/9206/gauteng"
#     print(f"Navigating to: {url}")
#     driver.get(url)
#     time.sleep(5)
    
#     # Wait for page to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )
    
#     # Find all business listing containers
#     # Try different selectors that might contain business listings
#     business_selectors = [
#         "//div[contains(@class, 'listing')]",
#         "//div[contains(@class, 'business')]",
#         "//div[contains(@class, 'company')]",
#         "//div[contains(@class, 'item')]",
#         "//div[.//h2 or .//h3]",
#         "//div[contains(@class, 'shortDescriptionCSS')]/..",
#         "//div[contains(@class, 'card')]",
#         "//div[contains(@class, 'panel')]"
#     ]
    
#     all_businesses = []
#     business_elements = []
    
#     for selector in business_selectors:
#         try:
#             elements = driver.find_elements(By.XPATH, selector)
#             if len(elements) > 1:  # We expect multiple business listings
#                 business_elements = elements
#                 print(f"Found {len(business_elements)} business elements using selector: {selector}")
#                 break
#         except:
#             continue
    
#     # If no specific containers found, try to find any elements that might contain business info
#     if not business_elements:
#         print("No specific business containers found. Trying fallback...")
#         # Look for elements that have substantial text content (likely business listings)
#         all_elements = driver.find_elements(By.XPATH, "//div | //article | //section")
#         for element in all_elements:
#             text = element.text.strip()
#             if len(text) > 50 and any(keyword in text.lower() for keyword in ['tel', 'phone', 'address', 'email']):
#                 business_elements.append(element)
        
#         print(f"Found {len(business_elements)} potential business elements using fallback")
    
#     # Extract data from each business element
#     for i, business_element in enumerate(business_elements):
#         print(f"\nProcessing business {i+1} of {len(business_elements)}...")
#         try:
#             business_data = extract_business_data(business_element)
#             all_businesses.append(business_data)
#             time.sleep(0.5)  # Small delay between processing
#         except Exception as e:
#             print(f"Error processing business {i+1}: {e}")
#             continue
    
#     # If no businesses found, try one more approach
#     if not all_businesses:
#         print("No businesses found with container approach. Trying direct text extraction...")
#         page_text = driver.page_source
#         # Look for patterns that indicate business information
#         # This is a fallback method
        
#         # Save page source for manual inspection
#         with open('full_page_source.html', 'w', encoding='utf-8') as f:
#             f.write(driver.page_source)
#         print("Full page source saved to full_page_source.html for manual inspection")
    
#     # Save to Excel
#     if all_businesses:
#         df = pd.DataFrame(all_businesses)
#         df.to_excel('all_businesses.xlsx', index=False)
#         df.to_csv('all_businesses.csv', index=False)
#         print(f"✅ {len(all_businesses)} businesses saved to all_businesses.xlsx and all_businesses.csv")
        
#         print("\nSample of extracted data:")
#         for i, business in enumerate(all_businesses[:3]):  # Show first 3 as sample
#             print(f"\nBusiness {i+1}:")
#             for key, value in business.items():
#                 print(f"  {key}: {value}")
#     else:
#         print("❌ No businesses could be extracted. Please check the page structure.")
        
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     import traceback
#     traceback.print_exc()
    
# finally:
#     driver.quit()


######One more wrong VERSION#######
##################################

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# import time
# import re

# # ------------------ Setup ------------------ #
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)

# def extract_business_data(text):
#     """Extracts structured business info from a block of text"""
#     data = {
#         "Name": "Not available",
#         "Phone": "Not available",
#         "Email": "Not available",
#         "Website": "Not available",
#         "Category": "Not available",
#         "Keywords": "Not available"
#     }

#     # --- Phone numbers ---
#     phone_matches = re.findall(
#         r'(?:Tel|TEL|Main|Cell|Cellular|Fax|Fax-To-Email)[:\s]*([\d\s]+)',
#         text, re.IGNORECASE
#     )
#     if phone_matches:
#         data["Phone"] = ", ".join(p.strip() for p in phone_matches)

#     # --- Email ---
#     email_match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
#     if email_match:
#         data["Email"] = ", ".join(email_match)

#     # --- Website ---
#     website_match = re.findall(r"https?://[^\s]+", text)
#     if website_match:
#         data["Website"] = ", ".join(website_match)

#     # --- Category ---
#     category_match = re.search(r"Category:\s*([^\n]+)", text, re.IGNORECASE)
#     if category_match:
#         data["Category"] = category_match.group(1).strip()

#     # --- Keywords ---
#     keywords_match = re.search(r"Keywords:\s*([^\n]+)", text, re.IGNORECASE)
#     if keywords_match:
#         data["Keywords"] = keywords_match.group(1).strip()

#     # --- Name (first line fallback) ---
#     lines = text.split("\n")
#     if lines:
#         first_line = lines[0].strip()
#         if len(first_line) > 2:
#             data["Name"] = first_line

#     return data

# # ------------------ Main Script ------------------ #
# try:
#     url = "https://www.eeziads.co.za/pg/9206/gauteng"
#     print(f"Navigating to: {url}")
#     driver.get(url)
#     time.sleep(5)

#     # Wait for business blocks to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "shortDescriptionCSS"))
#     )

#     business_elements = driver.find_elements(By.CLASS_NAME, "shortDescriptionCSS")
#     print(f"Found {len(business_elements)} business entries")

#     all_businesses = []
#     for i, elem in enumerate(business_elements):
#         text = elem.text.strip()
#         data = extract_business_data(text)
#         all_businesses.append(data)
#         print(f"[{i+1}] {data['Name']} | Phone: {data['Phone']} | Email: {data['Email']}")

#     # Save results
#     if all_businesses:
#         df = pd.DataFrame(all_businesses)
#         df.to_excel("all_businesses.xlsx", index=False)
#         df.to_csv("all_businesses.csv", index=False)
#         print(f"\n✅ Saved {len(all_businesses)} businesses to all_businesses.xlsx and all_businesses.csv")
#     else:
#         print("❌ No businesses could be extracted.")

# except Exception as e:
#     print(f"Error: {e}")
# finally:
#     driver.quit()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# import re
# import time

# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")

# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)

# url = "https://www.eeziads.co.za/pg/9206/gauteng"
# driver.get(url)
# time.sleep(5)

# business_data = []

# # Get all business containers
# containers = driver.find_elements(By.CLASS_NAME, "productContainer1Column")
# print(f"Found {len(containers)} business containers")

# for i, container in enumerate(containers, start=1):
#     entry = {"Name": "N/A", "Phone": "N/A", "Email": "N/A", "Website": "N/A", "Category": "N/A"}

#     # Business name
#     try:
#         name = container.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text.strip()
#         entry["Name"] = name
#     except:
#         pass

#     # Description block (phones, emails, etc.)
#     try:
#         desc = container.find_element(By.CLASS_NAME, "shortDescriptionCSS").text
#         # Phones
#         phones = re.findall(r"(?:Tel|TEL|Main|Cellular|Cell|Fax|Fax-To-Email)[:\s]*([\d\s]+)", desc, re.IGNORECASE)
#         if phones:
#             entry["Phone"] = ", ".join(p.strip() for p in phones)
#         # Email
#         emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", desc)
#         if emails:
#             entry["Email"] = ", ".join(emails)
#         # Website
#         websites = re.findall(r"https?://[^\s]+", desc)
#         if websites:
#             entry["Website"] = ", ".join(websites)
#         # Category
#         category_match = re.search(r"Category:\s*(.*)", desc, re.IGNORECASE)
#         if category_match:
#             entry["Category"] = category_match.group(1).strip()
#     except:
#         pass

#     print(f"[{i}] {entry['Name']} | Phone: {entry['Phone']} | Email: {entry['Email']}")
#     business_data.append(entry)

# # Save to Excel
# df = pd.DataFrame(business_data)
# df.to_excel("all_businesses.xlsx", index=False)
# print(f"✅ Saved {len(business_data)} businesses to all_businesses.xlsx")

# driver.quit()



# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import pandas as pd
# import re

# # ------------------ Setup Chrome ------------------ #
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")

# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)

# url = "https://www.eeziads.co.za/pg/9206/gauteng"
# driver.get(url)

# # ------------------ Wait for content to load ------------------ #
# # Wait until at least one business container is visible
# WebDriverWait(driver, 15).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "productContainer1Column"))
# )

# # Give extra time if necessary
# driver.implicitly_wait(5)

# # ------------------ Get page source and parse ------------------ #
# html = driver.page_source
# soup = BeautifulSoup(html, "html.parser")

# business_data = []

# # Find all business containers
# containers = soup.find_all("div", class_="productContainer1Column")
# print(f"Found {len(containers)} business containers")

# for i, container in enumerate(containers, start=1):
#     entry = {"Name": "N/A", "Phone": "N/A", "Email": "N/A", "Website": "N/A", "Category": "N/A"}

#     # Business name
#     name_tag = container.find("span", itemprop="name")
#     if name_tag:
#         entry["Name"] = name_tag.get_text(strip=True)

#     # Description block
#     desc_tag = container.find("div", class_="shortDescriptionCSS")
#     if desc_tag:
#         desc_text = desc_tag.get_text(" ", strip=True)

#         # Phones
#         phones = re.findall(r"(?:Tel|TEL|Main|Cellular|Cell|Fax|Fax-To-Email)[:\s]*([\d\s]+)", desc_text, re.IGNORECASE)
#         if phones:
#             entry["Phone"] = ", ".join(p.strip() for p in phones)

#         # Emails
#         emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", desc_text)
#         if emails:
#             entry["Email"] = ", ".join(emails)

#         # Websites
#         websites = re.findall(r"https?://[^\s]+", desc_text)
#         if websites:
#             entry["Website"] = ", ".join(websites)

#         # Category
#         category_match = re.search(r"Category:\s*(.*)", desc_text, re.IGNORECASE)
#         if category_match:
#             entry["Category"] = category_match.group(1).strip()

#     print(f"[{i}] {entry['Name']} | Phone: {entry['Phone']} | Email: {entry['Email']}")
#     business_data.append(entry)

# # ------------------ Save results ------------------ #
# df = pd.DataFrame(business_data)
# df.to_excel("all_businesses.xlsx", index=False)
# df.to_csv("all_businesses.csv", index=False)
# print(f"✅ Saved {len(business_data)} businesses to all_businesses.xlsx and all_businesses.csv")

# driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import re

# ------------------ Setup Chrome ------------------ #
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.eeziads.co.za/pg/9206/gauteng"
driver.get(url)

# ------------------ Wait for content to load ------------------ #
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "productContainer1Column"))
)
driver.implicitly_wait(5)

# ------------------ Get page source and parse ------------------ #
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

business_data = []

containers = soup.find_all("div", class_="productContainer1Column")
print(f"Found {len(containers)} business containers")

for i, container in enumerate(containers, start=1):
    entry = {"Name": "N/A", "Phone": "N/A", "Email": "N/A", "Website": "N/A", "Category": "N/A"}

    # Business name
    name_tag = container.find("span", itemprop="name")
    if name_tag:
        entry["Name"] = name_tag.get_text(strip=True)

    # Description block
    desc_tag = container.find("div", class_="shortDescriptionCSS")
    if desc_tag:
        desc_text = desc_tag.get_text(" ", strip=True)

        # --- Phones ---
        # Labeled phone numbers
        phones = re.findall(r"(?:Tel|TEL|Main|Cellular|Cell|Fax|Fax-To-Email)[:\s]*([\d\s\-]+)", desc_text, re.IGNORECASE)
        # General phone-like digit sequences
        extra_phones = re.findall(r'\b\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,4}\b', desc_text)
        phones.extend(extra_phones)
        # Remove duplicates and short junk numbers
        phones = list({p.strip() for p in phones if len(re.sub(r'\D','',p)) >= 7})
        if phones:
            entry["Phone"] = ", ".join(phones)

        # --- Emails ---
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", desc_text)
        if emails:
            entry["Email"] = ", ".join(emails)

        # --- Websites ---
        websites = re.findall(r"https?://[^\s]+", desc_text)
        if websites:
            entry["Website"] = ", ".join(websites)

        # --- Category ---
        category_match = re.search(r"Category:\s*(.*)", desc_text, re.IGNORECASE)
        if category_match:
            entry["Category"] = category_match.group(1).strip()

    print(f"[{i}] {entry['Name']} | Phone: {entry['Phone']} | Email: {entry['Email']}")
    business_data.append(entry)

# ------------------ Save results ------------------ #
df = pd.DataFrame(business_data)
df.to_excel("all_businesses.xlsx", index=False)
df.to_csv("all_businesses.csv", index=False)
print(f"✅ Saved {len(business_data)} businesses to all_businesses.xlsx and all_businesses.csv")

driver.quit()


