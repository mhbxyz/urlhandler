import re


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

    _SCHEME_REGEX = re.compile(r'^(?P<scheme>[a-z]+)://')
    _USER_INFO_REGEX = re.compile(r'://(?P<user>\w+):(?P<password>[\w\W]+)@')
    _HOST_REGEX = r'{start_character}(?P<host>[\w.]+)[/|$]?'
    _HOST_START_CHARACTER = '://'
    _PORT_REGEX = r''
    _PATH_REGEX = r''
    _QUERY_REGEX = r''
    _FRAGMENT_REGEX = r''

    def __init__(self, url: str = None):

        url = url.strip()

        if '@' in url:
            self.has_user_info = True
            self._HOST_START_CHARACTER = '@'
        if url[-1] == '/':
            self.end_with_slash = True
        if '?' in url:
            self.has_query = True
        if '#' in url:
            self.has_fragment = True

        self.scheme = self._SCHEME_REGEX.search(url).group('scheme')
        if self.has_user_info:
            self.user_info = self._USER_INFO_REGEX.search(url).groupdict()
        self.host = re.search(self._HOST_REGEX.format(start_character=self._HOST_START_CHARACTER), url).group('host')
