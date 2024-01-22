import requests
import re
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import time
import html

start_time = time.time()

def fetch_details(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    contact_elements = soup.find_all(['a', 'p'])

    phone_numbers = re.findall(r'\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', ' '.join([element.get_text() for element in contact_elements]))
    valid_phone_numbers = [re.match(r'\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', number).group() for number in phone_numbers if len(number) >= 7 and '.' not in number]

    # Extract email
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' '.join([element.get_text() for element in contact_elements]))
    valid_email_addresses = list(set(email_addresses))

    # Extracting address
    address_elements = soup.find_all('p')
    addresses = next((element.get_text().strip() for element in address_elements if re.search(r'\d{4,5}\s\w+', element.get_text())), 'N/A')

    return list(set(valid_phone_numbers)), valid_email_addresses, html.unescape(addresses)

def get_contact_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return fetch_details(response)
    except Exception as e:
        return ['Website not working'], ['Website not working'], 'Website not working'

def process_website(website):
    try:
        print('Website: ', website)
        details = get_contact_info(website)
        if details[2] is None:
            details = (details[0], details[1], details[2])
        elif not details:
            details = (details[0], details[1], details[2])
        else:
            details = (details[0], details[1], [details[2]])
        print('WEBSITE: ', website, ' CONTACT INFO: ', details)
        return {website: [details]}
    except Exception as e:
        print(f"Error processing website {website}: {e}")
        return None

# Website testing
websites = ['https://' + website for website in ['jansem.ch', 'radicalinclusion.ch', 'tornadoseltzer.ch', 'versalex.ch', 'repairdesign.ch', 'realfakephotos.com', 'goldengrowconsulting.com', 'noyo-mobility.com', 're-cae.com', 'annesigridfuchs.ch', 'oriotx.com', 'diamasfinance.com', 'hoi-kommunikation.ch', 'smart-recruiting.ch', 'smfinance.ch', 'arthconsultancy.com', 'engitec.ch', 'sihltop.ch', 'ixio.ch', 'fitcogroup.ch', 'prophima.ch', 'linkedin.com/in/angel-garcia-duran', 'lacavernedejouvence.ch', 'point-f.ch', 'dascoli-pharma.ch', 'daro-branddesign.ch', 'pinus-soap.ch', 'starke-dms.ch', 'mangolddigitaldesign.com', 'ebike360.ch']]

contact_details = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(process_website, websites))

for result in results:
    if result is not None:
        contact_details.append(result)

# Save to CSV
csv_filename = 'contact_details_optimized.csv'

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Website', 'Phone Numbers', 'Email Addresses', 'Address']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in contact_details:
        for website, details in entry.items():
            writer.writerow({
                'Website': website,
                'Phone Numbers': ', '.join(details[0][0]) if details[0][0] else 'N/A',
                'Email Addresses': ', '.join(details[0][1]) if details[0][1] else 'N/A',
                'Address': ', '.join(details[0][2]) if details[0][2] else 'N/A'
            })

print(f'Data saved to {csv_filename}')

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time} seconds")
