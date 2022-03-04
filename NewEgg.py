from bs4 import BeautifulSoup
import time
import requests
import re
from datetime import date
import csv
import pyshorteners

def main():
    product = input("What product are you looking for on Newegg? ")

    url = f"https://www.newegg.ca/p/pl?d={product}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    page_text = doc.find(class_="list-tool-pagination-text").strong
    pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

    items_found = {}

    page_num = int(input("How many pages do you want to check? "))

    for page in range(1, page_num+1):
        url = f"https://www.newegg.ca/p/pl?d={product}&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        containers = doc.find_all("div", class_="item-cell")
        
        for num, container in enumerate(containers):
            try:
                title = container.find("a", class_= "item-title").string
                price = container.find("li", class_="price-current").find("strong").string + container.find("li", class_="price-current").find("sup").string
                link = container.find("div", class_="item-container").a['href']
                link = pyshorteners.Shortener().tinyurl.short(link)
                rating = container.find("div", class_="item-info").find("a", class_="item-rating")['title'].split("+ ", 1)[1]
                brand = container.find("div", class_="item-info").find("a", class_="item-brand").img['title']
            except AttributeError:
                continue
                
            items_found[num] = {"Title" : title, "Price" : float(price.replace(",","")), "Rating" : rating, "Brand" : brand, "Link" : link}
            
        sorted_items = sorted(items_found.items(), key=lambda x: x[1]["Price"])

    for item in range(len(sorted_items)):
        time.sleep(0.1)
        print("Product:", sorted_items[item][1]['Title'])
        time.sleep(0.1)
        print("Price: $" + str(sorted_items[item][1]['Price']))
        time.sleep(0.1)
        print("Rating:", str(sorted_items[item][1]['Rating']) + "/5 eggs")
        time.sleep(0.1)
        print("Brand", sorted_items[item][1]['Brand'])
        time.sleep(0.1)
        print("Link:", sorted_items[item][1]['Link'].replace(" ","+"))
        time.sleep(0.1)
        print("--------------------------------------")

    print("There were", len(sorted_items),"items on sale under the search of:", product)

    today = date.today().strftime("%m-%d-%y")+".csv"

    with open(today, "w", newline='') as dataFile:
        fieldnames = ["Title", "Price", "Rating", "Brand", "Link"]
        writer = csv.DictWriter(dataFile, fieldnames = fieldnames)
        writer.writeheader()
        for item in range(len(sorted_items)):
            writer.writerow(sorted_items[item][1])
            
if __name__ == "__main__":
    main()