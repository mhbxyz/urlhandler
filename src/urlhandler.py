from urllib.parse import urlparse


class URLHandler:

    scheme: str = 'https'
    user_info: str = None
    host: str = None
    port: int = None
    path: str = None
    query: dict = None
    query_delimiter: str = '&'
    fragments: list = []

    def __init__(self):
        pass
