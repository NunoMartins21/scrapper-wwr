from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlsplit

def get_links():
    url = 'https://weworkremotely.com/categories/remote-programming-jobs'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    links = []

    for li in soup.select("#category-2 > article > ul > li"):
        for a in li.select('a'):
            if a['href'].startswith('/remote-jobs/'): links.append(f'https://weworkremotely.com{a["href"]}')

    return links

def get_info():
    links = get_links()
    data = {
        "Position Name": [],
        "Company Name": [],
        "Company Link": [],
        "Company Website": []
    }
    for idx, link in enumerate(links):
        print(f'[{idx+1}] {link}')
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'html.parser')

        position_name = soup.select_one('.listing-header-container > h1').text.strip()
        company_name = soup.select_one('.company-card > h2 > a').text.strip()
        company_link = f'https://weworkremotely.com{soup.select_one(".company-card > h2 > a")["href"]}'
        company_website = soup.select_one('.company-card > h3:nth-child(4) > a')['href'] if soup.select_one('.company-card > h3:nth-child(4) > a') is not None else soup.select_one('.company-card > h3:nth-child(3) > a')['href'] if soup.select_one('.company-card > h3:nth-child(3) > a') is not None else ''

        data["Position Name"].append(position_name)
        data["Company Name"].append(company_name)
        data["Company Link"].append(company_link)
        data["Company Website"].append(urlsplit(company_website).netloc.replace("www.", ""))

    df = pd.DataFrame(data).drop_duplicates(subset=['Company Website'], keep="first")
    return df

get_info().to_excel('scraped.xlsx')