import re


class URLFormatError(Exception):

    def __init__(self, message='The format of you URL is incorrect', **kwargs):
        self.message = message
        if 'missing' in kwargs:
            self.message = f'Your URL is missing {kwargs["missing"]}'
        super().__init__(self.message)


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

    _scheme_regex = re.compile(r'^(?P<scheme>[a-z]+)://')
    _user_info_regex = re.compile(r'://(?P<user>\w+):(?P<password>[\w\W]+)@')
    _host_regex = {'://': re.compile(r'://(?P<host>[\w.]+)[/|$]?'), '@': re.compile(r'@(?P<host>[\w.]+)[/|$]?')}
    _host_start_character = '://'
    _port_regex = r''
    _path_regex = r''
    _query_regex = r''
    _fragment_regex = r''

    def __init__(self, url: str = None):

        url = url.strip()

        if '@' in url:
            self.has_user_info = True
            self.host_start_character = '@'
        if url[-1] == '/':
            self.end_with_slash = True
        if '?' in url:
            self.has_query = True
        if '#' in url:
            self.has_fragment = True

        self.scheme = self._scheme_regex.search(url).group('scheme')
        if self.has_user_info:
            self.user_info = self._user_info_regex.search(url).groupdict()
        self.host = self._host_regex[self._host_start_character].search(url).group('host')
