import pathlib

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection

from . import config

settings = config.get_settings()

ASTRA_DB_CLIENT_ID = settings.db_client_id
ASTRA_DB_CLIENT_SECRET = settings.db_client_secret

BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = str(BASE_DIR / 'ignored' / 'connect.zip')


def get_cluster():
    cloud_config = {'secure_connect_bundle': CLUSTER_BUNDLE}
    auth_provider = PlainTextAuthProvider(
        username=ASTRA_DB_CLIENT_ID,
        password=ASTRA_DB_CLIENT_SECRET
    )
    return Cluster(cloud=cloud_config, auth_provider=auth_provider,  protocol_version=4)


def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session
