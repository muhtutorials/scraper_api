from typing import List

from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI

from . import db, config
from .models import Product, ProductScrape
from .schemas import ProductCreateSchema, ProductSchema, ProductScrapeSchema
from .worker import scrape_product


settings = config.get_settings()

app = FastAPI()

session = None


@app.on_event('startup')
async def startup_event():
    global session
    session = db.get_session()
    # Inspects the model and creates / updates the corresponding table and columns
    sync_table(Product)
    sync_table(ProductScrape)


@app.post('/products')
async def create_product(data: ProductCreateSchema):
    url = data.dict()['url']
    scrape_product.delay(url)
    return {'message': 'success'}


@app.get('/products', response_model=List[ProductSchema])
async def product_list():
    return list(ProductScrape.objects.all())


@app.get('/products/{asin}')
async def product_detail(asin: str):
    data = dict(Product.objects.get(asin=asin))
    scrapes = list(ProductScrape.objects.filter(asin=asin))
    data['scrapes'] = [ProductScrapeSchema(**scrape) for scrape in scrapes]
    return data
