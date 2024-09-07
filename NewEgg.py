import csv
import re
import time
from datetime import date

import pyshorteners
import requests
from bs4 import BeautifulSoup


def main():
    product = input("What product are you looking for on Newegg? ")

    url = f"https://www.newegg.ca/p/pl?d={product}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    page_text = doc.find(class_="list-tool-pagination-text").strong
    pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

    items_found = {}

    page_num = int(input("How many pages do you want to check? "))

    for page in range(1, page_num + 1):
        url = f"https://www.newegg.ca/p/pl?d={product}&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        containers = doc.find_all("div", class_="item-cell")

        for num, container in enumerate(containers):
            title = container.find("a", class_="item-title")
            title = str(title).split("</span>", 1)[1][:-4]
            price = (
                container.find("li", class_="price-current").find("strong").string
                + container.find("li", class_="price-current").find("sup").string
            )
            link = container.find("div", class_="item-container").a["href"]
            link = pyshorteners.Shortener().tinyurl.short(link)
            rating = (
                container.find("div", class_="item-info")
                .find("a", class_="item-rating")["title"]
                .split("+ ", 1)[1]
            )
            try:
                brand = (
                    container.find("div", class_="item-info")
                    .find("a", class_="item-brand")
                    .img["title"]
                )
            except AttributeError:
                brand = "Unknown"

            items_found[num] = {
                "Title": title,
                "Price": float(price.replace(",", "")),
                "Rating": rating,
                "Brand": brand,
                "Link": link,
            }

        sorted_items = sorted(items_found.items(), key=lambda x: x[1]["Price"])

    for item in range(len(sorted_items)):
        print("Product:", sorted_items[item][1]["Title"])
        print("Price: $" + str(sorted_items[item][1]["Price"]))
        print("Rating:", str(sorted_items[item][1]["Rating"]) + "/5 eggs")
        print("Brand:", sorted_items[item][1]["Brand"])
        print("Link:", sorted_items[item][1]["Link"].replace(" ", "+"))
        print("--------------------------------------")

    print(
        "There were", len(sorted_items), "items on sale under the search of:", product
    )

    today = date.today().strftime("%m-%d-%y") + ".csv"

    with open(today, "w", newline="") as dataFile:
        fieldnames = ["Title", "Price", "Rating", "Brand", "Link"]
        writer = csv.DictWriter(dataFile, fieldnames=fieldnames)
        writer.writeheader()
        for item in range(len(sorted_items)):
            writer.writerow(sorted_items[item][1])


if __name__ == "__main__":
    main()
