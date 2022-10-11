

class URLHandler:

    scheme: str = 'https'
    user_info: dict = None
    has_user_info: bool = False
    host: str = None
    port: int = None
    path: str = None
    end_with_slash: bool = False
    query: dict = {}
    has_query: bool = False
    query_delimiter: str = '&'
    fragment: str = None
    has_fragment: bool = False

    _SCHEME_REGEX = r'^(?P<scheme>[a-z]+)://'
    _USER_INFO_REGEX = r'://(?P<user>\w+):(?P<password>[\w\W]+)@'
    _HOST_REGEX = r''
    _PORT_REGEX = r''
    _PATH_REGEX = r''
    _QUERY_REGEX = r''
    _FRAGMENT_REGEX = r''

    def __init__(self, url: str = None):

        url = url.strip()

        if '@' in url:
            self.has_user_info = True
        if url[-1] == '/':
            self.end_with_slash = True
        if '?' in url:
            self.has_query = True
        if '#' in url:
            self.has_fragment = True
