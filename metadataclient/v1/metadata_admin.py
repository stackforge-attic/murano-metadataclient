#    Copyright (c) 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import StringIO


class Controller(object):
    def __init__(self, http_client):
        self.http_client = http_client

    def list_ui(self, path=None):
        if path:
            url = '/v1/admin/ui/{path}'.format(path=path)
        else:
            url = '/v1/admin/ui'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_agent(self, path=None):
        if path:
            url = '/v1/admin/agent/{path}'.format(path=path)
        else:
            url = '/v1/admin/agent'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_scripts(self, path=None):
        if path:
            url = '/v1/admin/scripts/{path}'.format(path=path)
        else:
            url = '/v1/admin/scripts'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_workflows(self, path=None):
        if path:
            url = '/v1/admin/workflows/{path}'.format(path=path)
        else:
            url = '/v1/admin/workflows'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_heat(self, path=None):
        if path:
            url = '/v1/admin/heat/{path}'.format(path=path)
        else:
            url = '/v1/admin/heat'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_manifests(self, path=None):
        if path:
            url = '/v1/admin/manifests/{path}'.format(path=path)
        else:
            url = '/v1/admin/manifests'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def upload_file(self, data_type, file_data):
        url = '/v1/admin/{0}'.format(data_type)
        hdrs = {'Content-Type': 'application/octet-stream'}
        self.http_client.raw_request('POST', url,
                                     headers=hdrs,
                                     body=file_data)

    def upload_file_to_dir(self, data_type, path, file_data):
        url = '/v1/admin/{0}/{1}'.format(data_type, path)
        hdrs = {'Content-Type': 'application/octet-stream'}
        self.http_client.raw_request('POST', url,
                                     headers=hdrs,
                                     body=file_data)

    def get_file(self, data_type, file_path):
        url = '/v1/admin/{0}/{1}'.format(data_type, file_path)
        resp, body = self.http_client.raw_request('GET', url)
        body_str = ''.join([chunk for chunk in body])
        return StringIO.StringIO(body_str)

    def create_directory(self, data_type, dir_name):
        url = '/v1/admin/{0}/{1}'.format(data_type, dir_name)
        self.http_client.json_request('PUT', url)

    def delete_dir(self, data_type, path):
        url = '/v1/admin/{0}/{1}'.format(data_type, path)
        self.http_client.json_request('DELETE', url)