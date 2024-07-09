from flask_restx import reqparse


parser_tagger = reqparse.RequestParser()
parser_tagger.add_argument(
    name="text", type=str, location="form", help="Text to be processed (PREFERENCE)"
)
parser_tagger.add_argument(name="file", location="files", help="File to be processed")
