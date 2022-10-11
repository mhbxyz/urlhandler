

class URLHandler:

    scheme: str = 'https'
    user_info: dict = None
    host: str = None
    port: int = None
    path: str = None
    query: dict = {}
    query_delimiter: str = '&'
    fragments: str = None

    def __init__(self):
        pass
