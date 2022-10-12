import re
import json
from typing import List


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
    _path: list = None
    _query: dict = {}
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
    _query_end_character = ''
    _fragment_regex = re.compile(r'#(?P<fragment>\w.+)$')

    @staticmethod
    def _is_a_number(string: str) -> int or float or None:

        number_is_negative: bool = False
        number_is_integer: bool = True
        number_str: str
        number: int or float

        if string.startswith('-'):
            number_is_negative = True

        if '.' in string:
            number_is_integer = False

        number_str = string[1:] if number_is_negative else string
        try:
            number = int(number_str) if number_is_integer else float(number_str)
        except ValueError:
            return None

        return -number if number_is_negative else number

    def _scan_query(self, query: str) -> dict:

        params: List[str]
        result: dict = {}

        params = query.split(self.query_param_separator)
        for param in params:

            name: str
            value: str or dict

            name, value = param.split('=', maxsplit=1)
            if value.startswith('{') and value.endswith('}'):
                value = json.loads(value)
            else:
                number = self._is_a_number(value)
                if number is not None:
                    value = number
                else:
                    if value == 'null':
                        value = None
                    elif value == 'true':
                        value = True
                    elif value == 'false':
                        value = False

            result.update({name: value})

        return result

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
                self._host_start_character = '@'
            if '?' in url:
                self.has_query = True
                self._path_end_character = '?'
            if '#' in url:
                self.has_fragment = True
                self._query_end_character = '#'
                if not self.has_query:
                    self._path_end_character = '#'

            self.scheme = self._scheme_regex.search(url).group('scheme')
            self.host = self._host_regex[self._host_start_character].search(url).group('host')
            path_match = self._path_regex[self._path_end_character].search(url)
            if path_match is not None:
                self._path = path_match.group('path').split('/')

            if self.has_user_info:
                self.user_info = self._user_info_regex.search(url).groupdict()

            port_match = self._port_regex.match(url)
            if port_match is not None:
                self.has_port = True
                self.port = port_match.group('port')

            if self.has_query:
                self._query = self._scan_query(self._query_regex[self._query_end_character].search(url).group('query'))

            if self.has_fragment:
                self.fragment = self._fragment_regex.search(url).group('fragment')

    def _get_query_string(self) -> str or None:

        params: list = []

        if self._query is not None:
            for key, value in self._query.items():
                if type(value) is dict:
                    value = json.dumps(value).replace(' ', '')
                else:
                    if type(value) is int or type(value) is float:
                        value = str(value)
                    else:
                        if value is None:
                            value = 'null'
                        elif value is True:
                            value = 'true'
                        elif value is False:
                            value = 'false'
                params.append(f'{key}={value}')

            return '&'.join(params)
        return None

    def get_url(self):

        url: str

        url = f'{self.scheme}://'
        url += f'{self.user_info["user"]}:{self.user_info["password"]}@' if self.user_info is not None else ''
        url += self.host if self.host is not None else ''
        url += f':{self.port}' if self.port is not None else ''
        url += f'/{"/".join(self._path)}' if self._path is not None else ''
        url += f'?{self._get_query_string()}' if self._query is not None else ''
        url += f'#{self.fragment}' if self.fragment is not None else ''

        return url

    def __str__(self):
        return self.get_url()

    def add_query_param(self, name, value):
        self._query.update({name: value})

    def remove_query_param(self, name):
        self._query.pop(name, None)

    @property
    def query(self) -> str:
        return self._get_query_string()

    @property
    def path(self) -> str:
        return "/".join(self._path)
