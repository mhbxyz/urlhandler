import re


class URLHandler:

    scheme: str = 'https'
    user_info: dict = None
    host: str = None
    port: int = None
    path: str = None
    query: dict = {}
    query_delimiter: str = '&'
    fragment: str = None

    _SCHEME_REGEX = r'^(?P<scheme>[a-z]+)://'
    _USER_INFO_REGEX = r'://(?P<user>\w+):(?P<password>[\w\W]+)@'
    _HOST_REGEX = r''
    _PORT_REGEX = r''
    _PATH_REGEX = r''
    _QUERY_REGEX = r''
    _FRAGMENT_REGEX = r''

    def __init__(self, url: str = None):
        pass
