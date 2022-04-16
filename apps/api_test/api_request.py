import json
import re
from urllib import parse

import requests


def _replace_argument(target_str, arguments=None):
    if not arguments:
        return target_str

    while 1:
        search_result = re.search(r'{{(.+?)}}', target_str)
        if not search_result:
            break

        argument_name = search_result.group(1)
        if argument_name in arguments:
            target_str = re.sub('{{'+argument_name+'}}', arguments[argument_name], target_str)
        else:
            target_str = re.sub('{{'+argument_name+'}}', argument_name, target_str)

    return target_str


def request(api, arguments=None):
    host = api.host.host
    method = api.http_method
    path = api.path

    url = parse.urljoin(host, path)
    url = _replace_argument(url, arguments)

    data = {}
    if api.data:
        data_list = json.loads(api.data, encoding='utf8')
        for data_dict in data_list:
            data[data_dict['name']] = _replace_argument(data_dict['value'], arguments)

    headers = {}
    if api.headers:
        header_list = json.loads(api.headers, encoding='utf8')
        for header_dict in header_list:
            headers[header_dict['name']] = _replace_argument(header_dict['value'], arguments)

    resp = requests.request(method, url, headers=headers, data=data)
    return resp
