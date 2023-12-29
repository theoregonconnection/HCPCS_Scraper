import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep 


# Define where to export the final dataframe as a CSV. 
output_location = r"C:\codes_data2.csv"

# This is the current location of the data we are scraping. 
# I hardcoded the base_url b/c I am lazy.
scrape_url = 'https://www.hcpcsdata.com/Codes'
base_url = 'https://www.hcpcsdata.com'


# Simulate a browser so the request does not get auto-denied
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Create the dataframe to store the scraped HCPCS description data
df = pd.DataFrame(columns=['HCPCS_CODE', 'HCPCS_DESCRIPTION'])

# Execute get request for scrape_url (this is the page with the category links)
page = requests.get(scrape_url, headers=headers)


# Execute the scrape process 
try:
    if page.status_code == 200:
        print(f"We page succesfully accessed: {scrape_url}")

        # Get the list of category links
        soup = BeautifulSoup(page.text, 'html.parser')
        category_links = [a['href'] for a in soup.find_all('a', href=True) if '/Codes/' in a['href']]

        for category in category_links:
            category_url = base_url + category 
            print(f"Processing Page: {category_url}")

            # Execute get request on category page
            category_page = requests.get(category_url, headers=headers)
            category_soup = BeautifulSoup(category_page.text, 'html.parser') 
            # Wait for a couple of seconds
            sleep(2)

            # Parse codes and descriptions 
            for row in category_soup.find_all('tr', class_='clickable-row'):
                code_tag = row.find('a', class_='identifier')
                description_tag = row.find_all('td')[1]  # The second td element

                if code_tag and description_tag:
                    code = code_tag.get_text(strip=True)
                    description = description_tag.get_text(strip=True)

                    # Data to be added to dataframe
                    new_data = pd.DataFrame([{'HCPCS_CODE': 'A9699', 'HCPCS_DESCRIPTION': 'Radiopharmaceutical, therapeutic, not otherwise classified'}])
                    df = pd.concat([df, new_data], ignore_index=True)
                else:
                    print(f"Skipping data for code: {code} and description: {description}")

    else:
        print(f"Failed to retrieve data from {scrape_url}. Status code: {response.status_code}")

except Exception as e:
    print("An error occurred:", e)

print("Data sucessfully scraped and placed into dataframe df")

# Export to CSV 
try:
    df.to_csv(output_location, index=False) 
    print(f"Data succesfully exported to CSV at: {output_location}")
except Exception as e:
    print("An error occurred when trying to export CSV:", e)
