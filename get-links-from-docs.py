import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# prompt user for url
url = input("Enter a URL: ")

# parse the domain of the input url
domain = urlparse(url).netloc

# make HTTP request
response = requests.get(url)

# parse HTML
soup = BeautifulSoup(response.content, "html.parser")

# find all links on the page
links = set()
for link in soup.find_all("a"):
    href = link.get("href")
    print(href)
    if href and href.startswith("/"):
        
        # convert internal link to absolute link
        link_url = url + href
        links.add(link_url)
    elif href and href.startswith("http"):
        # check if link is within the same domain
        link_domain = urlparse(href).netloc
        print(link_domain)
        if link_domain == domain:
            links.add(href)

# visit each link and add any unique links found
for link in list(links):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    for sub_link in soup.find_all("a"):
        href = sub_link.get("href")
        if href and href.startswith("/"):
            # convert internal link to absolute link
            link_url = link + href
            links.add(link_url)
        elif href and href.startswith("http"):
            # check if link is within the same domain
            link_domain = urlparse(href).netloc
            if link_domain == domain:
                links.add(href)

# write links to a csv
with open("links.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for link in links:
        writer.writerow([link])
