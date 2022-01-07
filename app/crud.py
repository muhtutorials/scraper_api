import uuid

from .models import Product, ProductScrape


def create_product(data):
    return Product.create(**data)


def scrape_product(data):
    data['uuid'] = uuid.uuid1()
    return ProductScrape.create(**data)


def create_product_and_scrape(data):
    product = create_product(data)
    scrape = scrape_product(data)
    return product, scrape
