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

    _scheme_regex = re.compile(r'^(?P<scheme>[a-z]+)://')
    _user_info_regex = re.compile(r'://(?P<user>\w+):(?P<password>[\w\W]+)@')
    _host_regex = r'{start_character}(?P<host>[\w.]+)[/|$]?'
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
        self.host = re.search(self._host_regex.format(start_character=self._host_start_character), url).group('host')
