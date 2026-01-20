import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Set to keep track of visited URLs
visited_urls = set()

# Counter to track how many times the word is found
word_count = 0
flag_count = 0


def ebayfinder(keywords, priceMax, pages):
    start_url = 'https://www.ebay.com/sch/i.html?_nkw='
    base_url = 'https://www.ebay.com/itm/'
    fileName = 'eBay_'
    counter = 0

    for word in keywords:
        fileName += word
        start_url += word
        counter += 1
        if len(keywords) != counter: # Checks if it hasn't reached the last keyword.
            start_url += '+'
            fileName += '_'
    start_url += "&_sacat=0&_from=R40&_pgn="

    fileName += '_items_under_$' + str(priceMax) + '.txt'
    print(fileName)
    with open(fileName, 'w') as file:
        file.write(fileName[:-4].replace("_", " "))

    for i in range(1, pages+1):
        listings = scrape_website(start_url+str(i), base_url)
        
        with open(fileName, 'a') as file:
            file.write("\nScraped: " + start_url+str(i))   
            for item in listings:
                price = item.find(class_="s-item__price").text
                title = item.find(class_="s-item__title").text
                link = item.find("a", class_="s-item__link").attrs["href"]
                if " to " not in price:
                    if "Shop on eBay" not in title:
                        if (float(price[1:]) < priceMax):
                            file.write("\n" + title)
                            file.write("\n\t" + price)
                            file.write("\n\t" + link)

                
    


def scrape_website(url, base_url):
    global word_count  # Use the global counter

    # Skip if the URL has already been visited
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        # Send a GET request to the URL
        time.sleep(2)
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return
                # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # header
        print(f"Scraped: {url}")
        print(f"Webpage Title: {soup.title.text}...")  

        # Find all items listed on the page
        listings = soup.find_all(class_="s-item__info clearfix")
        return listings

    except Exception as e:
        print(f"Error scraping {url}: {e}")


list = ['shark','vacuum','purple']

ebayfinder(list, 80.00, 1)
