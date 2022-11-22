import logging.config
import os
from os import environ as env

import sentry_sdk
from flask import Flask, Blueprint
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

from scanner_backend.settings import Config
from scanner_backend.api.endpoints import cache, limiter
from scanner_backend.api.endpoints.topics import ns as topics_namespace
from scanner_backend.api.endpoints.tagger import ns as tagger_namespace
from scanner_backend.api.endpoints.scanned import ns as scanned_namespace
from scanner_backend.api.endpoints.tagger_crs import ns as crs_tagger_namespace
from scanner_backend.api.endpoints.crs import ns as crs_namespace
from scanner_backend.api.restplus import api


def add_sentry():
    SENTRY_DSN = env.get('SENTRY_DSN', None)
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[FlaskIntegration()]
        )


def create_app(config=Config):
    add_sentry()
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(config)
    initialize_app(app)

    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
    logging.config.fileConfig(logging_conf_path)
    log = logging.getLogger(__name__)
    log.info('>>>>> Starting development server at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
    return app


def add_namespaces(app):
    namespaces = [topics_namespace,
                  tagger_namespace,
                  scanned_namespace,
                  crs_tagger_namespace,
                  crs_namespace
    ]
    for ns in namespaces:
        if ns.name in env.get('EXCLUDE_NAMESPACES', []):
            continue
        api.add_namespace(ns)


def initialize_app(app):
    cache.init_app(app, config=Config.CACHE)
    limiter.init_app(app)
    blueprint = Blueprint('api', __name__)
    CORS(blueprint)
    api.init_app(blueprint)
    add_namespaces(app)
    app.register_blueprint(blueprint)


def main():
    app = create_app(Config)
    app.run(
        host=app.config['IP'],
        port=app.config['PORT'],
        debug=app.config['FLASK_DEBUG']
    )


if __name__ == "__main__":
    main()
