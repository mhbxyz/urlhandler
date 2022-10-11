import re


class URLFormatError(Exception):

    def __init__(self, message='The format of you URL is incorrect', **kwargs):
        self.message = message
        if 'missing' in kwargs:
            self.message = f'Your URL is missing {kwargs["missing"]}'
        super().__init__(self.message)


class InvalidQueryParamSeparatorError(Exception):
    def __init__(self, query_param_separator: str):
        self.message = f'{query_param_separator} is not a valid query parameter separator'
        super().__init__(self.message)


class URLHandler:

    scheme: str = 'https'
    user_info: dict = None
    has_user_info: bool = False
    host: str = None
    port: int = None
    has_port: bool = False
    path: str = None
    query: dict = {}
    has_query: bool = False
    query_param_separator: str = '&'
    fragment: str = None
    has_fragment: bool = False

    _scheme_regex = re.compile(r'^(?P<scheme>[a-z]+)://')
    _user_info_regex = re.compile(r'://(?P<user>\w+):(?P<password>[\w\W]+)@')
    _host_regex = {'://': re.compile(r'://(?P<host>[\w.]+)[/|$]?'), '@': re.compile(r'@(?P<host>[\w.]+)[/|$]?')}
    _host_start_character = '://'
    _port_regex = re.compile(r':(?P<port>\d+)[/|$]?')
    _path_regex = {
        '': re.compile(r'[^/]/(?P<path>\w.+)$'),
        '?': re.compile(r'[^/]/(?P<path>\w.+)\?'),
        '#': re.compile(r'[^/]/(?P<path>\w.+)#')
    }
    _path_end_character = ''
    _query_regex = {'': re.compile(r'\?(?P<query>\w.+)$'), '#': re.compile(r'\?(?P<query>\w.+)#')}
    _fragment_regex = re.compile(r'#(?P<fragment>\w.+)$')

    def __init__(self, url: str = None, query_param_separator: str = None):

        if url is not None:

            if query_param_separator is not None:
                if query_param_separator not in ['&', ';']:
                    raise InvalidQueryParamSeparatorError(query_param_separator)
                self.query_param_separator = query_param_separator

            if '://' not in url:
                raise URLFormatError(missing='://')

            url = url.strip('/ ')

            if '@' in url:
                self.has_user_info = True
                self.host_start_character = '@'
            if '?' in url:
                self.has_query = True
                self._path_end_character = '?'
            if '#' in url:
                self.has_fragment = True
                if not self.has_query:
                    self._path_end_character = '#'

            self.scheme = self._scheme_regex.search(url).group('scheme')
            self.host = self._host_regex[self._host_start_character].search(url).group('host')
            self.path = self._path_regex[self._path_end_character].search(url).group('path')

            if self.has_user_info:
                self.user_info = self._user_info_regex.search(url).groupdict()

            port_match = self._port_regex.match(url)
            if port_match is not None:
                self.has_port = True
                self.port = port_match.group('port')

            if self.has_fragment:
                self.fragment = self._fragment_regex.search(url).group('fragment')
