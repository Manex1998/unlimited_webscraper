#working code for scraping sabusinessdirectories.com with improved logic to find business names and contact details
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
    url = "https://sabusinessdirectories.com/north-west-province/"
    
    all_business_data = []
    
    try:
        print(f"Scraping page: {url}")
        
        # Navigate to the page
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "elementor-column"))
        )
        
        # Find all business containers - look for columns that contain business information
        business_containers = driver.find_elements(By.CSS_SELECTOR, ".elementor-column")
        print(f"Found {len(business_containers)} column elements")
        
        for container in business_containers:
            try:
                # Check if this column contains business information
                business_data = extract_business_data_from_column(container)
                if business_data and business_data['Name'] != 'Not available':
                    all_business_data.append(business_data)
                    print(f"Extracted: {business_data['Name']} - {business_data.get('Telephone', 'No phone')}")
                    
            except Exception as e:
                print(f"Error processing a business container: {e}")
                continue
                
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    return all_business_data

def extract_business_data_from_column(column):
    """Extract business data from a column element"""
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
        # Look for heading elements that might contain the business name
        headings = column.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6, .elementor-heading-title")
        for heading in headings:
            name = heading.text.strip()
            if name and not any(generic in name.lower() for generic in 
                              ['gauteng', 'directory', 'business', 'welcome', 'home']):
                business_data['Name'] = name
                break
        
        # If no heading found, look for strong text that might be the business name
        if business_data['Name'] == 'Not available':
            strong_elements = column.find_elements(By.TAG_NAME, "strong")
            for strong in strong_elements:
                text = strong.text.strip()
                if (text and not any(keyword in text.lower() for keyword in 
                                   ['telephone', 'fax', 'cell', 'address', 'email', 'website', 'services', 'postal']) and
                    len(text) > 3 and len(text) < 100):  # Reasonable name length
                    business_data['Name'] = text
                    break
        
        # Get all text content from the column
        text_content = column.text.strip()
        
        # Extract telephone numbers
        try:
            # Look for telephone patterns
            tel_patterns = [
                r'Telephone[:\s]*(.+?)(?=\n|$)',
                r'Tel[:\s]*(.+?)(?=\n|$)',
                r'Phone[:\s]*(.+?)(?=\n|$)',
                r'(\+?\d{2,4}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4})'  # General phone pattern
            ]
            
            for pattern in tel_patterns:
                tel_match = re.search(pattern, text_content, re.IGNORECASE)
                if tel_match:
                    business_data['Telephone'] = tel_match.group(1).strip() if ':' in pattern else tel_match.group(0).strip()
                    break
        except:
            pass
        
        # Extract fax numbers
        try:
            fax_match = re.search(r'Fax[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if fax_match:
                business_data['Fax'] = fax_match.group(1).strip()
        except:
            pass
        
        # Extract cell numbers
        try:
            cell_match = re.search(r'Cell[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if cell_match:
                business_data['Cell'] = cell_match.group(1).strip()
        except:
            pass
        
        # Extract physical address
        try:
            addr_match = re.search(r'Address[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if addr_match:
                business_data['Address'] = addr_match.group(1).strip()
        except:
            pass
        
        # Extract postal address
        try:
            postal_match = re.search(r'Postal Address[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if postal_match:
                if business_data['Address'] == 'Not available':
                    business_data['Address'] = postal_match.group(1).strip()
                else:
                    business_data['Address'] += f" | Postal: {postal_match.group(1).strip()}"
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
            website_match = re.search(r'Website[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
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
            services_match = re.search(r'Services[:\s]*(.+?)(?=\n|$)', text_content, re.IGNORECASE)
            if services_match:
                business_data['Services'] = services_match.group(1).strip()
        except:
            pass
        
    except Exception as e:
        print(f"Error extracting business data from column: {e}")
    
    return business_data

# Alternative approach: Look for specific patterns in the entire page
def scrape_alternative_approach():
    """Alternative approach that looks for business information patterns throughout the page"""
    url = "https://sabusinessdirectories.com/gauteng/"
    
    all_business_data = []
    
    try:
        print(f"Scraping page with alternative approach: {url}")
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get all text content
        page_text = driver.find_element(By.TAG_NAME, "body").text
        lines = page_text.split('\n')
        
        current_business = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line might be a business name
            if (len(line) > 3 and len(line) < 100 and 
                not any(keyword in line.lower() for keyword in 
                       ['telephone', 'fax', 'cell', 'address', 'email', 'website', 'services', 'postal', 'gauteng', 'directory']) and
                not re.search(r'[\d\(\)]', line)):  # Less likely to contain numbers/parentheses
                
                # If we have a current business with data, save it
                if current_business and any(current_business.values()):
                    all_business_data.append(current_business)
                    print(f"Extracted: {current_business.get('Name', 'Unknown')}")
                
                # Start a new business
                current_business = {'Name': line}
            
            # Extract contact information
            elif current_business:
                # Telephone
                if re.search(r'Telephone|Tel|Phone', line, re.IGNORECASE):
                    current_business['Telephone'] = re.sub(r'^.*?[:]', '', line).strip()
                
                # Email
                elif '@' in line and ('Email' in line or 'Mail' in line):
                    current_business['Email'] = line
                
                # Address
                elif re.search(r'Address|Location', line, re.IGNORECASE):
                    current_business['Address'] = re.sub(r'^.*?[:]', '', line).strip()
                
                # Website
                elif re.search(r'Website|Web|Site', line, re.IGNORECASE):
                    current_business['Website'] = re.sub(r'^.*?[:]', '', line).strip()
        
        # Add the last business
        if current_business and any(current_business.values()):
            all_business_data.append(current_business)
            
    except Exception as e:
        print(f"Error in alternative approach: {e}")
    
    return all_business_data

# Run the scraping function
print("Starting scraping process for sabusinessdirectories.com...")

# Try the main approach first
business_data = scrape_sabusinessdirectories()

# If main approach didn't find much, try alternative approach
if len(business_data) < 5:
    print("Main approach found few results, trying alternative approach...")
    business_data = scrape_alternative_approach()

# Save to Excel and CSV
if business_data:
    df = pd.DataFrame(business_data)
    
    # Fill NaN values with 'Not available'
    df = df.fillna('Not available')
    
    # Save to Excel
    df.to_excel('sabusinessdirectories_contacts.xlsx', index=False)
    
    # Save to CSV
    df.to_csv('sabusinessdirectories_contacts.csv', index=False)
    
    print(f"Successfully extracted {len(business_data)} business records.")
    
    # Show summary
    telephones_found = len([b for b in business_data if b.get('Telephone') not in ['Not available', None, '']])
    emails_found = len([b for b in business_data if b.get('Email') not in ['Not available', None, '']])
    
    print(f"Businesses with telephone numbers: {telephones_found}")
    print(f"Businesses with emails: {emails_found}")
    print(f"Data saved to sabusinessdirectories_contacts.xlsx and sabusinessdirectories_contacts.csv")
    
else:
    print("No business data was extracted.")

# Close the driver
driver.quit()
print("Scraping completed!")