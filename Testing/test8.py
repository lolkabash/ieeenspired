import requests
from bs4 import BeautifulSoup
import re

search = "HP General Specification for Environment (GSE) Substances and Materials Requirements"
results = 5  # valid options 10, 20, 30, 40, 50, and 100


def get_link(search, results):
    page = requests.get(f"https://www.google.com/search?q={search}&num={results}")
    soup = BeautifulSoup(page.content, "html5lib")
    links = soup.findAll("a")

    extracted_links = []
    for link in links:
        link_href = link.get("href")
        if "url?q=" in link_href and not "webcache" in link_href:
            temp_link = link.get("href").split("?q=")[1].split("&sa=U")[0]
            extracted_links.append(temp_link)
    return extracted_links
