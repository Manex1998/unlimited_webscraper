



# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# import time

# # Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")

# # Path to your chromedriver.exe
# service = Service(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# # Initialize Chrome driver
# driver = webdriver.Chrome(service=service, options=chrome_options)

# try:
#     url = "https://www.eeziads.co.za/pg/9206/gauteng"
#     print(f"Navigating to: {url}")
#     driver.get(url)
#     time.sleep(5)
    
#     # Save the entire page source for manual inspection
#     with open('complete_page_source.html', 'w', encoding='utf-8') as f:
#         f.write(driver.page_source)
#     print("Complete page source saved to complete_page_source.html")
    
#     # Get all text content
#     all_text = driver.find_element(By.TAG_NAME, "body").text
#     with open('page_text_content.txt', 'w', encoding='utf-8') as f:
#         f.write(all_text)
#     print("All text content saved to page_text_content.txt")
    
#     # Let's look at specific elements that might contain business info
#     print("\nLooking for specific elements...")
    
#     # Check for common business listing patterns
#     elements_to_check = [
#         "div", "p", "span", "li", "article", "section"
#     ]
    
#     for tag in elements_to_check:
#         elements = driver.find_elements(By.TAG_NAME, tag)
#         print(f"\n{tag.upper()} elements found: {len(elements)}")
        
#         # Show a few examples
#         for i, element in enumerate(elements[:3]):  # First 3 of each type
#             text = element.text.strip()
#             if text and len(text) > 20:
#                 print(f"  {i+1}. {text[:100]}...")
    
#     print("\nPlease check the saved files to see the actual page structure.")
#     print("This will help us create a more targeted extraction script.")

# except Exception as e:
#     print(f"An error occurred: {str(e)}")
    
# finally:
#     driver.quit()

# from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
# import re
# import pandas as pd
# import os
# import warnings

# # Suppress MarkupResemblesLocatorWarning
# warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# # Path to the HTML file
# html_file = 'complete_page_source.html'

# # Check if the file exists
# if not os.path.exists(html_file):
#     print(f"Error: File '{html_file}' not found in the current directory.")
#     exit(1)

# # Read HTML content from file
# try:
#     with open(html_file, 'r', encoding='utf-8') as file:
#         html_content = file.read()
# except Exception as e:
#     print(f"Error reading HTML file: {e}")
#     exit(1)

# # Check if HTML content is empty
# if not html_content.strip():
#     print("Error: HTML content is empty.")
#     exit(1)

# # Parse HTML with BeautifulSoup
# try:
#     soup = BeautifulSoup(html_content, 'html.parser')
# except Exception as e:
#     print(f"Error parsing HTML: {e}")
#     exit(1)

# # Find all product containers
# product_containers = soup.find_all('div', class_='productContainer1Column boxProductHolder shadowItem')

# # Check if any containers were found
# if not product_containers:
#     print("Warning: No business containers found. Check HTML structure or class name.")
#     print("Expected class: 'productContainer1Column boxProductHolder shadowItem'")
#     exit(1)

# # List to store extracted business information
# businesses = []

# # Regular expressions for extracting data
# phone_pattern = re.compile(r'(TEL|Main|Phone):?\s*([\d\s-]+)', re.IGNORECASE)
# fax_pattern = re.compile(r'(FAX|Fax|Fax-To-Email):?\s*([\d\s-]+)', re.IGNORECASE)
# email_pattern = re.compile(r'(Email):?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', re.IGNORECASE)
# website_pattern = re.compile(r'(Homepage|WEBSITE):?\s*(https?://[^\s]+)', re.IGNORECASE)
# address_pattern = re.compile(r'(ADDRESS|Address):?\s*([^TEL|FAX|EMAIL|WEBSITE|TRADE HEADING|Category|Main|Fax|Email|Homepage|Cellular|Keywords]+)', re.IGNORECASE)
# category_pattern = re.compile(r'(Category|TRADE HEADING):?\s*([^&<]+)', re.IGNORECASE)
# cellular_pattern = re.compile(r'(Cellular):?\s*([\d\s-]+)', re.IGNORECASE)

# for container in product_containers:
#     business = {}
    
#     # Extract business name
#     name_tag = container.find('span', itemprop='name')
#     business['name'] = name_tag.text.strip() if name_tag else 'N/A'
    
#     # Extract description content
#     description = container.find('div', class_='shortDescriptionCSS', itemprop='description')
#     description_text = description.get_text(separator=' ', strip=True) if description else ''
    
#     # Extract address
#     address_match = address_pattern.search(description_text)
#     business['address'] = address_match.group(2).strip() if address_match else 'N/A'
    
#     # Extract phone number
#     phone_match = phone_pattern.search(description_text)
#     business['phone'] = phone_match.group(2).strip() if phone_match else 'N/A'
    
#     # Extract fax number
#     fax_match = fax_pattern.search(description_text)
#     business['fax'] = fax_match.group(2).strip() if fax_match else 'N/A'
    
#     # Extract email
#     email_match = email_pattern.search(description_text)
#     business['email'] = email_match.group(2).strip() if email_match else 'N/A'
    
#     # Extract website
#     website_match = website_pattern.search(description_text)
#     business['website'] = website_match.group(2).strip() if website_match else 'N/A'
    
#     # Extract category
#     category_match = category_pattern.search(description_text)
#     business['category'] = category_match.group(2).strip() if category_match else 'N/A'
    
#     # Extract cellular number
#     cellular_match = cellular_pattern.search(description_text)
#     business['cellular'] = cellular_match.group(2).strip() if cellular_match else 'N/A'
    
#     businesses.append(business)

# # Save to Excel
# output_file = 'businesses.xlsx'
# try:
#     # Convert to DataFrame
#     df = pd.DataFrame(businesses, columns=['Name', 'Address', 'Phone', 'Fax', 'Cellular', 'Email', 'Website', 'Category'])
#     # Save to Excel
#     df.to_excel(output_file, index=False, engine='openpyxl')
#     print(f"Extracted {len(businesses)} businesses and saved to '{output_file}'")
# except Exception as e:
#     print(f"Error writing to Excel: {e}")
#     exit(1)

# # Print summary to console
# print(f"Total businesses extracted: {len(businesses)}")
# for idx, business in enumerate(businesses, 1):
#     print(f"Business {idx}:")
#     print(f"Name: {business['name']}")
#     print(f"Address: {business['address']}")
#     print(f"Phone: {business['phone']}")
#     print(f"Fax: {business['fax']}")
#     print(f"Cellular: {business['cellular']}")
#     print(f"Email: {business['email']}")
#     print(f"Website: {business['website']}")
#     print(f"Category: {business['category']}")
#     print("-" * 50)


# from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
# import re
# import pandas as pd
# import os
# import warnings

# # Suppress MarkupResemblesLocatorWarning
# warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# # Path to the HTML file
# html_file = 'complete_page_source.html'

# # Check if the file exists
# if not os.path.exists(html_file):
#     print(f"Error: File '{html_file}' not found in the current directory.")
#     exit(1)

# # Read HTML content from file
# try:
#     with open(html_file, 'r', encoding='utf-8') as file:
#         html_content = file.read()
# except Exception as e:
#     print(f"Error reading HTML file: {e}")
#     exit(1)

# # Check if HTML content is empty
# if not html_content.strip():
#     print("Error: HTML content is empty.")
#     exit(1)

# # Parse HTML with BeautifulSoup
# try:
#     soup = BeautifulSoup(html_content, 'html.parser')
# except Exception as e:
#     print(f"Error parsing HTML: {e}")
#     exit(1)

# # Find all product containers
# product_containers = soup.find_all('div', class_='productContainer1Column boxProductHolder shadowItem')

# # Check if any containers were found
# if not product_containers:
#     print("Warning: No business containers found. Check HTML structure or class name.")
#     print("Expected class: 'productContainer1Column boxProductHolder shadowItem'")
#     exit(1)

# # List to store extracted business information
# businesses = []

# # Regular expressions for extracting data
# phone_pattern = re.compile(r'(TEL|Main|Phone):?\s*([\d\s-]+)', re.IGNORECASE)
# fax_pattern = re.compile(r'(FAX|Fax|Fax-To-Email):?\s*([\d\s-]+)', re.IGNORECASE)
# email_pattern = re.compile(r'(Email):?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', re.IGNORECASE)
# website_pattern = re.compile(r'(Homepage|WEBSITE):?\s*(https?://[^\s]+)', re.IGNORECASE)
# address_pattern = re.compile(r'(ADDRESS|Address):?\s*([^TEL|FAX|EMAIL|WEBSITE|TRADE HEADING|Category|Main|Fax|Email|Homepage|Cellular|Keywords]+)', re.IGNORECASE)
# cellular_pattern = re.compile(r'(Cellular):?\s*([\d\s-]+)', re.IGNORECASE)
# # Updated category pattern to capture main category and subcategories
# category_pattern = re.compile(r'(Category|TRADE HEADING):?\s*([^&<]+?)(?=\s*(?:1\)|$))', re.IGNORECASE)
# subcategory_pattern = re.compile(r'(\d+)\)\s*([^\d][^&<]+?)(?=\s*(?:\d+\)|$))', re.IGNORECASE)

# for idx, container in enumerate(product_containers, 1):
#     business = {}
    
#     # Extract business name
#     name_tag = container.find('span', itemprop='name')
#     business['name'] = name_tag.text.strip() if name_tag else 'N/A'
    
#     # Extract description content
#     description = container.find('div', class_='shortDescriptionCSS', itemprop='description')
#     description_text = description.get_text(separator=' ', strip=True) if description else ''
    
#     # Debug: Print raw description for problematic entries (e.g., after 1329)
#     if idx >= 1329:
#         print(f"Debug Business {idx} Raw Description: {description_text}")
    
#     # Extract address
#     address_match = address_pattern.search(description_text)
#     business['address'] = address_match.group(2).strip() if address_match else 'N/A'
    
#     # Extract phone number
#     phone_match = phone_pattern.search(description_text)
#     business['phone'] = phone_match.group(2).strip() if phone_match else 'N/A'
    
#     # Extract fax number
#     fax_match = fax_pattern.search(description_text)
#     business['fax'] = fax_match.group(2).strip() if fax_match else 'N/A'
    
#     # Extract email
#     email_match = email_pattern.search(description_text)
#     business['email'] = email_match.group(2).strip() if email_match else 'N/A'
    
#     # Extract website
#     website_match = website_pattern.search(description_text)
#     business['website'] = website_match.group(2).strip() if website_match else 'N/A'
    
#     # Extract cellular number
#     cellular_match = cellular_pattern.search(description_text)
#     business['cellular'] = cellular_match.group(2).strip() if cellular_match else 'N/A'
    
#     # Extract category and subcategories
#     category_match = category_pattern.search(description_text)
#     business['category'] = category_match.group(2).strip() if category_match else 'N/A'
    
#     # Extract subcategories (e.g., 1) Automotive Parts, 2) Car Parts)
#     subcategory_matches = subcategory_pattern.findall(description_text)
#     business['subcategories'] = [match[1].strip() for match in subcategory_matches] if subcategory_matches else []
    
#     businesses.append(business)

# # Save to Excel
# output_file = 'businesses.xlsx'
# try:
#     # Convert to DataFrame
#     df = pd.DataFrame(businesses, columns=['Name', 'Address', 'Phone', 'Fax', 'Cellular', 'Email', 'Website', 'Category', 'Subcategories'])
#     # Save to Excel
#     df.to_excel(output_file, index=False, engine='openpyxl')
#     print(f"Extracted {len(businesses)} businesses and saved to '{output_file}'")
# except Exception as e:
#     print(f"Error writing to Excel: {e}")
#     exit(1)

# # Print summary to console
# print(f"Total businesses extracted: {len(businesses)}")
# for idx, business in enumerate(businesses, 1):
#     print(f"Business {idx}:")
#     print(f"Name: {business['name']}")
#     print(f"Address: {business['address']}")
#     print(f"Phone: {business['phone']}")
#     print(f"Fax: {business['fax']}")
#     print(f"Cellular: {business['cellular']}")
#     print(f"Email: {business['email']}")
#     print(f"Website: {business['website']}")
#     print(f"Category: {business['category']}")
#     print(f"Subcategories: {business['subcategories']}")
#     print("-" * 50)


from bs4 import BeautifulSoup
import re
import pandas as pd

# Load the HTML file
file_path = "complete_page_source.html"  # change to your file path
with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

# Container for business data
business_data = []

# The relevant business info seems to be inside "productContainer1Column" divs
business_containers = soup.find_all("div", class_="productContainer1Column")

for container in business_containers:
    entry = {}

    # Extract business name (inside span[itemprop='name'])
    name_tag = container.find("span", itemprop="name")
    if name_tag:
        entry["Business Name"] = name_tag.get_text(strip=True)
    
    # Extract description block where details are written
    desc_tag = container.find("div", class_="shortDescriptionCSS")
    if desc_tag:
        desc_text = desc_tag.get_text(" ", strip=True)
        
        # Save raw description
        entry["Description"] = desc_text
        
        # Extract phone numbers (Main, Tel, Cell, Fax, etc.)
        tel_match = re.findall(r"(?:Tel|TEL|Main|Cellular|Cell|Fax|FAX)[: ]+([\d\s\+\-]+)", desc_text, re.IGNORECASE)
        if tel_match:
            entry["Phone Numbers"] = ", ".join([t.strip() for t in tel_match])
        
        # Extract email addresses
        email_match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", desc_text)
        if email_match:
            entry["Emails"] = ", ".join(email_match)
        
        # Extract websites (http/https links)
        website_match = re.findall(r"https?://[^\s]+", desc_text)
        if website_match:
            entry["Websites"] = ", ".join(website_match)
        
        # Extract address-like lines (basic heuristic)
        address_match = re.findall(r"[0-9]+\s[\w\s,.-]+", desc_text)
        if address_match:
            entry["Possible Address"] = "; ".join(address_match)
    
    if entry:
        business_data.append(entry)

# Convert to DataFrame for better handling
df = pd.DataFrame(business_data)

# Show the results
print(df)

# Optionally save to Excel/CSV
df.to_csv("business_info.csv", index=False)
df.to_excel("business_info.xlsx", index=False)
