import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. URL of Google search results (replace with your URL)
url = "https://www.google.com/search?sca_esv=00d2b9dd415bfb1f&tbm=lcl&sxsrf=AE3TifMY8tVjyInYqrgE0-wCvaY6131yIA:1756206197242&q=law+firms+in+gauteng&rflfq=1&num=10&sa=X&sqi=2&ved=2ahUKEwj42Kf0qaiPAxWz9LsIHai7JC4QjGp6BAgnEAE&biw=1366&bih=607&dpr=1#rlfi=hd:;si:5501188608969405651,a;mv:[[-26.0173804,28.0638009],[-26.149722699999998,27.964295600000003]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:14"  # e.g., the URL you used for law firms in Gauteng

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/139.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 2. Find all <span> tags with 'aria-label' containing 'Call phone number'
phone_spans = soup.find_all('span', attrs={'aria-label': True})
phone_numbers = []

for span in phone_spans:
    label = span['aria-label']
    if 'Call phone number' in label:
        # Extract the actual number
        number = label.replace('Call phone number ', '').strip()
        phone_numbers.append(number)

# 3. Save to Excel
df = pd.DataFrame(phone_numbers, columns=['Phone Number'])
df.to_excel('law_firm_phones.xlsx', index=False)

print("✅ Phone numbers saved to law_firm_phones.xlsx")
