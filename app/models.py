from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Product(Model):
    __keyspace__ = 'products'
    asin = columns.Text(primary_key=True, required=True)
    url = columns.Text(required=True)
    title = columns.Text()
    price = columns.Integer()


class ProductScrape(Model):
    __keyspace__ = 'products'
    uuid = columns.UUID(primary_key=True, required=True)
    asin = columns.Text(index=True, required=True)
    url = columns.Text(required=True)
    title = columns.Text()
    price = columns.Integer()
