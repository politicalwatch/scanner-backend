from datetime import datetime
import ast
import time
import re

from tipi_data.models.topic import Topic
from tipi_data.schemas.topic import TopicSchema, TopicExtendedSchema
from tipi_data.models.scanned import Scanned
from tipi_data.schemas.scanned import ScannedSchema
from tipi_data.utils import generate_id
from .crs_data import CRS_MAPPING


""" TOPICS METHODS """

def get_topics():
    return TopicSchema(many=True).dump(Topic.objects.natsorted())

def get_topic(id):
    return TopicExtendedSchema().dump(Topic.objects.get(id=id))


""" TAGGER METHODS """

def get_tags():
    return Topic.get_tags()


''' SCANNED METHODS '''

def get_scanned(id):
    return ScannedSchema().dump(Scanned.objects.get(id=id))

def save_scanned(payload):
    EXPIRATION_OPTIONS = {
        '1m': 1,
        '3m': 3,
        '1y': 12
    }
    ONE_MONTH_IN_SECONDS = 60 * 60 * 24 * 30

    expiration = time.mktime(datetime.now().timetuple()) + (ONE_MONTH_IN_SECONDS * EXPIRATION_OPTIONS.get(payload.get('expiration', '1m')))

    scanned = Scanned(
        id=generate_id(payload['title'], payload['excerpt'], str(datetime.now())),
        title=payload['title'],
        excerpt=payload['excerpt'],
        result=ast.literal_eval(payload['result']),
        created=datetime.now(),
        expiration=datetime.fromtimestamp(expiration),
        verified=payload['verified']
    )

    saved = scanned.save()
    if not saved:
        raise Exception
    return {
        'id': scanned.id,
        'title': scanned.title,
        'excerpt': scanned.excerpt,
        'expiration': str(scanned.expiration)
    }

def search_verified_scanned(query):
    documents = Scanned.objects.filter(title=re.compile(query, re.IGNORECASE), verified=True)

    return ScannedSchema(many=True).dump(documents)


''' CRS METHODS '''

def get_crs_data(crs):
    if crs in CRS_MAPPING:
        return CRS_MAPPING[crs]
    return ''
