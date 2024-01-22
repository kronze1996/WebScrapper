# Web Scraper
## Web Scraping and Contact Information Extraction Process

### Overview
This Python script performs web scraping on a list of websites to extract contact information, including phone numbers, email addresses, and physical addresses. The code utilizes the BeautifulSoup library for HTML parsing and regular expressions for pattern matching.

### Features
- **Multithreading:**
  The script employs concurrent.futures.ThreadPoolExecutor to concurrently process multiple websites, improving efficiency.
- **Robust URL Handling:**
  The code accommodates different URL structures by attempting to find a '/contact-us' or '/kontakt' page. If not found, it defaults to the provided URL.
- **Error Handling:**
  The script gracefully handles exceptions, marking information as 'N/A' if a website is not accessible or does not provide contact details.

### Usage
1. Install the required dependencies:
    ```bash
    pip install requests beautifulsoup4
    ```

2. Run the script:
    ```bash
    python script_name.py
    ```

3. The extracted contact details are saved in a CSV file named 'contact_details_optimized.csv'.

### Configuration
Modify the `websites` list to include the URLs of the websites you want to scrape.

### Output
The CSV file contains the following columns:
- `Website`: The URL of the website.
- `Phone Numbers`: Extracted phone numbers (if available).
- `Email Addresses`: Extracted email addresses (if available).
- `Address`: Extracted physical address (if available).

### Notes
- The script may need adjustments based on the specific structure of the websites you are scraping.
- Ensure compliance with the terms of service of the websites being scraped.
- For large-scale or continuous scraping, consider implementing delays to avoid being blocked by websites.
