from flask_restx import fields
from scanner_backend.api.restplus import api


scanned_model = api.model(
    "scanned",
    {
        "title": fields.String(required=True, description="Scanned document's title"),
        "expiration": fields.String(
            required=False, description="Scanned document's expiration date"
        ),
        "excerpt": fields.String(
            required=True, description="Scanned document's excerpt"
        ),
        "result": fields.String(required=True, description="Serialized result"),
    },
)
