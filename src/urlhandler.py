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
    has_port: bool = False
    path: str = None
    query: dict = {}
    has_query: bool = False
    query_delimiter: str = '&'
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
    _query_regex = r''
    _fragment_regex = r''

    def __init__(self, url: str = None):

        if '://' not in url:
            raise URLFormatError(missing='://')

        if url is not None:

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
            if self.has_user_info:
                self.user_info = self._user_info_regex.search(url).groupdict()
            self.host = self._host_regex[self._host_start_character].search(url).group('host')
            port_match = self._port_regex.match(url)
            if port_match is not None:
                self.has_port = True
                self.port = port_match.group('port')
