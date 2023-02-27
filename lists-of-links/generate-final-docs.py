import csv
import requests
from bs4 import BeautifulSoup
import os
import time
import random

def generate_user_agent():
    """Generate a random user agent."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    ]
    return random.choice(user_agents)

def scrape_text_from_url(url):
    """Scrape the text from a webpage and return it as a string."""

    # Add a random delay before making the request
    delay = random.uniform(0.2, 0.5)
    time.sleep(delay)

    # Generate a random user agent and set headers
    user_agent = generate_user_agent()
    headers = {'User-Agent': user_agent}

    # Send a GET request to the URL and get the HTML content
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("ERROR: COULD NOT SCRAPE TEXT FROM", url, ":", str(e).upper())
        

    html_content = response.content

    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tags to exclude from the extracted text and remove them from the parsed HTML
    for tag in soup.find_all(['script', 'style', 'header', 'footer', 'nav', 'form', 'img', 'audio', 'video']):
        tag.decompose()

    # Extract all the text from the webpage
    text = soup.get_text(separator='\n')

    # Return the extracted text
    return text


# Prompt the user for a filename
filename = input("Enter the filename: ")

# Create the final-docs folder if it does not exist
if not os.path.exists('final-docs'):
    os.makedirs('final-docs')

# Scrape the text from each link and save it to a file
with open(os.path.join('final-docs', f'{filename}'), 'w', encoding='utf-8') as f:
    # Open the CSV file and read the list of links
    with open(f'{filename}', 'r', encoding='utf-8') as f_links:
        links = [row[0] for row in csv.reader(f_links)]

    for i, link in enumerate(links):
        # Scrape the text from the current link
        text = scrape_text_from_url(link)

        # Check if the text was scraped successfully
        if text is None:
            break

        # Write the text to the output file, prepended with the page number
        f.write(f'---PAGE {i+1}---\n{text}\n\n')

        # Print the current page number
        print(f'Page {i+1} scraped')


