import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Set to keep track of visited URLs
visited_urls = set()

# Counter to track how many times the word is found
word_count = 0
flag_count = 0
def scrape_website(url, base_url):
    global word_count  # Use the global counter

    # Skip if the URL has already been visited
    if url in visited_urls:
        return
    visited_urls.add(url)

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
        print(f"Content: {page_text[:200]}...")  # Print first 200 characters of content

        # Target word to search for
        target_word = "scraping"


        # Check if the target word is in the page text
        if target_word.lower() in page_text.lower():
            word_count += 1  # Increment the counter
            print(f'Found the word "{target_word}" on {url}. Total occurrences so far: {word_count}')

            # Write to the output file
            with open('output.txt', 'a') as file:  # Use 'a' to append to the file
                file.write(f'Found the word "{target_word}" on {url}.\n')

        # Find all links on the page
        links = soup.find_all('a')
        for link in links:
            # Check if the link has an 'href' attribute
            if 'href' in link.attrs:
                # Construct the absolute URL
                absolute_url = urljoin(base_url, link['href'])

                # Ensure the link is within the same domain
                if absolute_url.startswith(base_url):
                    scrape_website(absolute_url, base_url)  # Recursively scrape the linked page
            else:
                print(f"Skipping link without 'href': {link}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Starting URL and base URL
start_url = 'https://asn.flightsafety.org/'
base_url = 'https://asn.flightsafety.org/'  # Base URL to ensure we stay within the same domain

# Start scraping
scrape_website(start_url, base_url)

target_word = "Sheridan"
# Print the final count
print(f'Total occurrences of the word "{target_word}": {word_count}')
