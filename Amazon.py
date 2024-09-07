import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv("USER_AGENT")


def get_title(product):
    try:
        title = product.find("span", attrs={"id": "productTitle"}).text.strip()
        return title
    except AttributeError:
        return "N/A"


def get_price(product):
    try:
        price = (
            product.find("span", attrs={"class": "a-price aok-align-center"})
            .find("span", attrs={"class": "a-offscreen"})
            .text
        )
        return price
    except AttributeError:
        return "N/A"


def get_rating(product):
    try:
        rating = (
            product.find(
                "a",
                attrs={"class": "a-popover-trigger a-declarative"},
            )
            .find("span", attrs={"class": "a-size-base a-color-base"})
            .text
        )
        return rating.strip() + " out of 5 stars"
    except AttributeError:
        return "N/A"


def get_availability(product):
    try:
        availability = (
            product.find("div", attrs={"id": "availability"}).find("span").text.strip()
        )
        return availability
    except AttributeError:
        return "N/A"


def get_reviews(product):
    try:
        reviews = (
            product.find("a", attrs={"id": "acrCustomerReviewLink"})
            .find("span", attrs={"id": "acrCustomerReviewText"})
            .text
        )
        return reviews
    except AttributeError:
        return "N/A"


def main():
    product = "gaming+laptop"
    url = f"https://www.amazon.ca/s?k={product}"
    HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US en;q=0.5",
    }
    search_page = requests.get(url, headers=HEADERS).text
    search_soup = BeautifulSoup(search_page, "html.parser")

    links = search_soup.find_all(
        "a",
        attrs={
            "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
        },
    )

    product_data = {
        "title": [],
        "price": [],
        "rating": [],
        "availability": [],
        "reviews": [],
        "links": [],
    }

    link_list = []

    for links in links:
        link_list.append("https://amazon.ca" + links.get("href"))

    for i in range(10):
        page = requests.get(link_list[i], headers=HEADERS).text
        product = BeautifulSoup(page, "html.parser")

        product_data["title"].append(get_title(product))
        product_data["price"].append(get_price(product))
        product_data["rating"].append(get_rating(product))
        product_data["availability"].append(get_availability(product))
        product_data["reviews"].append(get_reviews(product))
        product_data["links"].append(link_list[i])

    df = pd.DataFrame(product_data)
    df.to_csv("test.csv")
    print(df)


if __name__ == "__main__":
    main()
