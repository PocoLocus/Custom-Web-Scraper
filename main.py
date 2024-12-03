import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_data():
    for h3 in soup.find_all("h3", class_="bc-heading"):
        a = h3.find("a")
        if a:
            titles.append(h3.text.strip())

    page_authors = soup.find_all("li", class_="authorLabel")
    page_authors = [author.text for author in page_authors]
    page_authors = [author.replace("By:", "").strip() for author in page_authors]
    authors.extend(page_authors)

    for p in soup.find_all("p", class_="buybox-regular-price"):
        price = p.find("span", string=lambda text: text and "$" in text)
        if price:
            prices.append(price.text.strip())

URL = "https://www.audible.com/search?keywords=book&node=18573211011&pageSize=&ref_pageloadid=wM9MYpaKiZMkcurE&pf_rd_p=1d79b443-2f1d-43a3-b1dc-31a2cd242566&pf_rd_r=DDNT9Q8TT093937AHSX0&plink=hqxNGe35U8ksivMh&pageLoadId=65vRIXRCxfHwkQnk&creativeId=18cc2d83-2aa9-46ca-8a02-1d1cc7052e2a&ref=a_search_c4_pageSize_0"
titles = []
prices = []
authors = []

response = requests.get(url=URL)
html_doc = response.content
soup = BeautifulSoup(html_doc, "html.parser")

driver = webdriver.Chrome()
driver.get(URL)
time.sleep(1)

next_button_disabled = False
while not next_button_disabled:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scrape_data()
    next_button = driver.find_element(By.CLASS_NAME, 'nextButton')
    if "bc-button-disabled" in next_button.get_attribute("class"):
        next_button_disabled = True
    else:
        next_button.click()
        time.sleep(1)

with open("audiobooks.csv", "w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author", "Price"])
    writer.writerows(zip(titles, authors, prices))

driver.quit()
