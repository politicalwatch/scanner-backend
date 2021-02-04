from datetime import datetime
import json
import ast
import logging
import time
import re
import pygsheets


from tipi_data.models.topic import Topic
from tipi_data.schemas.topic import TopicSchema, TopicExtendedSchema
from tipi_data.models.scanned import Scanned
from tipi_data.schemas.scanned import ScannedSchema
from tipi_data.utils import generate_id



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


''' LINES OF ACTION '''

class GoogleCredentials:
    def __init__(self):
        self.google_credentials = pygsheets.authorize(
            service_account_file='credentials.json'
        )

class LinesOfAction(GoogleCredentials):
    targets_blacklist = [
        '2.3',
        '3.8',
        '4.7',
        '5.5',
        '15.1',
        '16.1',
        '16.3',
        '16.6'
    ]

    def extract(results):
        extractor = LinesOfAction()
        return extractor.get(results)

    def get(self, results):
        kb_lines = self.get_kb_lines()
        sheet = self.google_credentials.open('Linea de accion-TAG')
        wks = sheet.worksheet('index', 0)
        data = wks.get_values(grange=pygsheets.GridRange(worksheet=wks, start=None, end=None))
        lines_by_tag = dict()
        for d in data[1:]:
            lines_by_tag[d[1]] = d[0]

        result = results['result']
        tags = result['tags']
        courses_of_action = []
        if len(tags) != 0:
            for tag in tags:
                subtopic = self.extract_subtopic_number(tag['subtopic'])
                if not self.is_target_in_blackist_for_lines(subtopic):
                    try:
                        tag['course_of_action'] = kb_lines[subtopic]
                        courses_of_action.append(kb_lines[subtopic])
                    except KeyError:
                        pass
                else:
                    try:
                        tag['course_of_action'] = lines_by_tag[tag['tag']]
                        courses_of_action.append(lines_by_tag[tag['tag']])
                    except KeyError:
                        pass
        result['courses_of_action'] = list(set(courses_of_action))

    def extract_subtopic_number(self, subtopic):
        splitted = subtopic.split(' ', 1)
        return splitted[0]

    def get_kb_lines(self):
        wks = self.google_credentials.open('Matriz linea de accion').worksheet('index', 0)
        data = wks.get_values(grange=pygsheets.GridRange(worksheet=wks, start=None, end=None))
        kb = dict()
        for row in data[1:]:
            if row[0] not in self.targets_blacklist:
                kb[row[0]] = row[1]
        return kb

    def is_target_in_blackist_for_lines(self, target):
        return target in self.targets_blacklist
