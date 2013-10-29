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
from os.path import dirname, basename

from metadataclient import exc
from urllib import quote, urlencode


class Wrapper(object):
    def __init__(self, entity_id, **kwargs):
        self.id = entity_id
        for key, value in kwargs.items():
            setattr(self, key, value)


class Controller(object):
    def __init__(self, http_client):
        self.http_client = http_client

    def list_services(self):
        resp, body = self.http_client.json_request('GET', '/v1/admin/services')
        services = body.get('services', None)
        if services:
            return [Wrapper(service['full_service_name'], **service)
                    for service in services]
        else:
            raise exc.HTTPInternalServerError()

    def get_service_files(self, data_type, service=None):
        included_files = {}
        if service:
            resp, body = self.http_client.json_request(
                'GET', '/v1/admin/services/{service}'.format(service=service))
            for path in body.get('service_files', {}).get(data_type, []):
                included_files[path] = True

        resp, body = self.http_client.json_request(
            'GET', '/v1/admin/{data_type}'.format(data_type=data_type))
        all_files = body.get(data_type, [])

        return [Wrapper(path, path=dirname(path), filename=basename(path),
                        selected=included_files.get(path, False))
                for path in all_files]

    def download_service(self, service):
        resp, body = self.http_client.raw_request(
            'GET', '/v1/client/services/{service}'.format(service=service))
        return body

    def upload_service(self, data):
        resp, body = self.http_client.raw_request(
            'POST', '/v1/admin/services/', body=data)
        return body

    def delete_service(self, service):
        resp, body = self.http_client.raw_request(
            'DELETE', '/v1/admin/services/{service}'.format(service=service))
        return body

    def toggle_enabled(self, service):
        resp, body = self.http_client.raw_request(
            'POST', '/v1/admin/services/{service}/toggle_enabled'.format(
                service=service))
        return body

    def list_ui(self, path=None):
        if path:
            url = quote('/v1/admin/ui/{path}'.format(path=path))
        else:
            url = '/v1/admin/ui'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_agent(self, path=None):
        if path:
            url = quote('/v1/admin/agent/{path}'.format(path=path))
        else:
            url = '/v1/admin/agent'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_scripts(self, path=None):
        if path:
            url = quote('/v1/admin/scripts/{path}'.format(path=path))
        else:
            url = '/v1/admin/scripts'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_workflows(self, path=None):
        if path:
            url = quote('/v1/admin/workflows/{path}'.format(path=path))
        else:
            url = '/v1/admin/workflows'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_heat(self, path=None):
        if path:
            url = quote('/v1/admin/heat/{path}'.format(path=path))
        else:
            url = '/v1/admin/heat'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_manifests(self, path=None):
        if path:
            url = quote('/v1/admin/manifests/{path}'.format(path=path))
        else:
            url = '/v1/admin/manifests'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def upload_file(self, data_type, file_data, file_name=None):
        if file_name:
            params = urlencode({'filename': file_name})
            url = '/v1/admin/{0}?{1}'.format(data_type, params)
        else:
            url = '/v1/admin/{0}'.format(data_type)
        hdrs = {'Content-Type': 'application/octet-stream'}
        resp, body = self.http_client.raw_request('POST', url,
                                                  headers=hdrs,
                                                  body=file_data)
        return resp

    def upload_file_to_dir(self, data_type, path, file_data):
        url = quote('/v1/admin/{0}/{1}'.format(data_type, path))
        hdrs = {'Content-Type': 'application/octet-stream'}
        self.http_client.raw_request('POST', url,
                                     headers=hdrs,
                                     body=file_data)

    def get_file(self, data_type, file_path):
        url = quote('/v1/admin/{0}/{1}'.format(data_type, file_path))
        resp, body = self.http_client.raw_request('GET', url)
        body_str = ''.join([chunk for chunk in body])
        return StringIO.StringIO(body_str)

    def create_directory(self, data_type, dir_name):
        url = '/v1/admin/{0}/{1}'.format(data_type, dir_name)
        self.http_client.json_request('PUT', url)

    def delete(self, data_type, path):
        # space could be in url paths.
        url = quote('/v1/admin/{0}/{1}'.format(data_type, path))
        self.http_client.raw_request('DELETE', url)
