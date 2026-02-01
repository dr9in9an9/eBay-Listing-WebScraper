from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

# Starting URL and base URL
start_url = 'https://www.scrapethissite.com/pages/simple/'
base_url = 'https://www.scrapethissite.com/'  # Base URL to ensure we stay within the same domain


def scrape_website(url, base_url):
    global word_count  # Use the global counter

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text content from the page
        page_text = soup.get_text()
        print(f"Scraped: {url}")
        print(f"Content: {page_text[:100]}...")  # Print first 200 characters of content


        # Find all countries on the page
        countries = soup.find_all("h3", class_="country-name")
        print('a')
        counter = 0
        for name in countries:
            print(counter)
            print(name.get_text())
            counter = counter + 1
            if "A" in name:
                print(name)
                print("a country")


    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Start scraping
scrape_website(start_url, base_url)
