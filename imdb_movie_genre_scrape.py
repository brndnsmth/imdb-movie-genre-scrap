import requests
from bs4 import BeautifulSoup
import json

# Function to scrape a single page
def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    items = []

    # Find and extract data from each item on the page
    for item in soup.find_all(class_='lister-item'):
        title = item.find(class_='lister-item-header').find('a').text
        year = item.find(class_='lister-item-year').text.strip('()')

        # Check if the ratings element exists before extracting text
        ratings_element = item.find(class_='ratings-imdb-rating')
        rating = ratings_element.text.strip() if ratings_element else 'N/A'

        items.append({
            'title': title,
            'year': year,
            'rating': rating
        })

    return items

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    items = []

    # Find and extract data from each item on the page
    for item in soup.find_all(class_='lister-item'):
        title = item.find(class_='lister-item-header').find('a').text
        year = item.find(class_='lister-item-year').text.strip('()')
        rating = item.find(class_='ratings-imdb-rating').text.strip()
        items.append({
            'title': title,
            'year': year,
            'rating': rating
        })

    return items


# Genre you want to scrape (default is 'horror')
# Reference other genres  here: https://www.imdb.com/feature/genre/
genre_to_scrape = 'horror'

# Number of pages to scrape (adjust as needed)
num_pages_to_scrape = 5

# Function to scrape multiple pages
def scrape_imdb_pages(genre_to_scrape, num_pages_to_scrape):
    base_url = f'https://www.imdb.com/search/title/?genres={genre_to_scrape}&sort=release_date,asc&explore=title_type,genres'
    all_items = []
    for page in range(1, num_pages_to_scrape + 1):
        page_url = f"{base_url}&page={page}"
        items = scrape_page(page_url)
        all_items.extend(items)

    return all_items

# Scrape the data from IMDb
result = scrape_imdb_pages(genre_to_scrape, num_pages_to_scrape)

# Write the data to a JSON file
output_filename = f'imdb_{genre_to_scrape}_movies.json'
with open(output_filename, 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)

print(f'Scraped {len(result)} {genre_to_scrape} items and saved to {output_filename}')
