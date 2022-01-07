from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from celery import Celery
from celery.schedules import crontab
from celery.signals import beat_init, worker_process_init

from .db import get_session
from .config import get_settings
from .crud import create_product_and_scrape
from .models import Product, ProductScrape
from .schemas import ProductSchema
from .scraper import Scraper


celery_app = Celery(__name__)
settings = get_settings()
celery_app.conf.broker_url = settings.redis_url
celery_app.conf.result_backend = settings.redis_url


def celery_on_startup(*args, **kwargs):
    if connection.cluster is not None:
        connection.cluster.shutdown()

    if connection.session is not None:
        connection.session.shutdown()

    get_session()
    sync_table(Product)
    sync_table(ProductScrape)


worker_process_init.connect(celery_on_startup)
beat_init.connect(celery_on_startup)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    sender.add_periodic_task(crontab(minute='*/3'), scrape_product_list.s())


@celery_app.task
def scrape_product(url):
    scraper = Scraper(url)
    data = scraper.scrape_data()

    try:
        validated_data = ProductSchema(**data)
    except:
        validated_data = None
    if validated_data is not None:
        product, _ = create_product_and_scrape(validated_data.dict())
        return product.title
    return None


@celery_app.task
def scrape_product_list():
    products = list(Product.objects.all().values_list('url', flat=True))
    for url in products:
        scrape_product.delay(url)
