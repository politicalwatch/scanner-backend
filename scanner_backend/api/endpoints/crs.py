import codecs
import logging

from flask_restplus import Namespace, Resource

from scanner_backend.api.business import get_crs_data
from scanner_backend.api.endpoints import cache


log = logging.getLogger(__name__)

ns = Namespace('crs', description='Mapping between CRS to SDGs.')


@ns.route('/<id>')
class CrsItem(Resource):

    @cache.cached()
    def get(self, id):
        """Returns SDG and Target for a specific CRS"""
        return get_crs_data(id)
