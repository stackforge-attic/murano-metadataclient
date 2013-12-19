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
        resp, body = self.http_client.json_request('GET', '/admin/services')
        services = body.get('services', None)
        if services is not None:
            return [Wrapper(service['full_service_name'], **service)
                    for service in services]
        else:
            raise exc.HTTPInternalServerError()

    def get_service_files(self, data_type=None, service=None):
        all_files = []

        def get_files(_data_type):
            included_files = {}
            if service:
                resp, body = self.http_client.json_request(
                    'GET',
                    '/admin/services/{service}'.format(service=service))
                for path in body.get(_data_type, []):
                    included_files[path] = True

            resp, body = self.http_client.json_request(
                'GET', '/admin/{data_type}'.format(data_type=_data_type))
            files = body.get(_data_type, [])

            return [Wrapper('{0}##{1}'.format(_data_type, path),
                            path=dirname(path), filename=basename(path),
                            selected=included_files.get(path, False),
                            data_type=_data_type)
                    for path in files]

        if data_type:
            all_files.extend(get_files(data_type))
        else:
            # FixME: need to get list of data types directly from server
            for data_type in ('ui', 'workflows', 'heat', 'agent', 'scripts'):
                all_files.extend(get_files(data_type))

        return all_files

    def get_service_info(self, service):
        resp, body = self.http_client.json_request(
            'GET', '/admin/services/{service}/info'.format(service=service))
        return body

    def download_service(self, service):
        resp, body = self.http_client.raw_request(
            'GET', '/client/services/{service}'.format(service=service))
        return body

    def upload_service(self, data):
        resp, body = self.http_client.raw_request(
            'POST', '/admin/services/', body=data)
        return body

    def delete_service(self, service):
        resp, body = self.http_client.raw_request(
            'DELETE', '/admin/services/{service}'.format(service=service))
        return body

    def toggle_enabled(self, service):
        resp, body = self.http_client.raw_request(
            'POST', '/admin/services/{service}/toggle_enabled'.format(
                service=service))
        return body

    def list_ui(self, path=None):
        if path:
            url = quote('/admin/ui/{path}'.format(path=path))
        else:
            url = '/admin/ui'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_agent(self, path=None):
        if path:
            url = quote('/admin/agent/{path}'.format(path=path))
        else:
            url = '/admin/agent'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_scripts(self, path=None):
        if path:
            url = quote('/admin/scripts/{path}'.format(path=path))
        else:
            url = '/admin/scripts'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_workflows(self, path=None):
        if path:
            url = quote('/admin/workflows/{path}'.format(path=path))
        else:
            url = '/admin/workflows'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_heat(self, path=None):
        if path:
            url = quote('/admin/heat/{path}'.format(path=path))
        else:
            url = '/admin/heat'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def list_manifests(self, path=None):
        if path:
            url = quote('/admin/manifests/{path}'.format(path=path))
        else:
            url = '/admin/manifests'
        resp, body = self.http_client.json_request('GET', url)
        return body

    def upload_file(self, data_type, file_data, file_name=None):
        if file_name:
            params = urlencode({'filename': file_name})
            url = '/admin/{0}?{1}'.format(data_type, params)
        else:
            url = '/admin/{0}'.format(data_type)
        hdrs = {'Content-Type': 'application/octet-stream'}
        resp, body = self.http_client.raw_request('POST', url,
                                                  headers=hdrs,
                                                  body=file_data)
        return resp

    def _update_service(self, service_files, service_id, service_info):
        service_info.update(service_files)
        url = quote('/admin/services/{service}'.format(service=service_id))
        resp, body = self.http_client.json_request('PUT', url,
                                                   body=service_info)
        return resp, body

    def upload_file_to_service(self, data_type, file_data,
                               file_name, service_id):
        self.upload_file(data_type, file_data, file_name)
        service_info = self.get_service_info(service_id)
        resp, service_files = self.http_client.json_request(
            'GET', '/admin/services/{service}'.format(service=service_id))
        existing_files = service_files.get(data_type)
        if existing_files:
            service_files[data_type].append(file_name)
        else:
            service_files[data_type] = [file_name]
        resp, body = self._update_service(service_files,
                                          service_id,
                                          service_info)
        return body

    def upload_file_to_dir(self, data_type, path, file_data):
        url = quote('/admin/{0}/{1}'.format(data_type, path))
        hdrs = {'Content-Type': 'application/octet-stream'}
        self.http_client.raw_request('POST', url,
                                     headers=hdrs,
                                     body=file_data)

    def get_file(self, data_type, file_path):
        url = quote('/admin/{0}/{1}'.format(data_type, file_path))
        resp, body = self.http_client.raw_request('GET', url)
        body_str = ''.join([chunk for chunk in body])
        return StringIO.StringIO(body_str)

    def create_directory(self, data_type, dir_name):
        url = '/admin/{0}/{1}'.format(data_type, dir_name)
        self.http_client.json_request('PUT', url)

    def delete(self, data_type, path):
        url = quote('/admin/{0}/{1}'.format(data_type, path))
        self.http_client.raw_request('DELETE', url)

    def delete_from_service(self, data_type, filename, service_id):
        service_info = self.get_service_info(service_id)
        resp, service_files = self.http_client.json_request(
            'GET', '/admin/services/{service}'.format(service=service_id))
        files = service_files.get(data_type)
        if filename in files:
            service_files[data_type].remove(filename)
        resp, body = self._update_service(service_files,
                                          service_id,
                                          service_info)
        if resp.status == 200:
            url = quote('/admin/{0}/{1}'.format(data_type, filename))
            self.http_client.raw_request('DELETE', url)
        return body

    def create_or_update_service(self, service, json_data):
        # Increment version in case of modification
        json_data['service_version'] += 1

        json_data['version'] = u'0.1'  # Version of metadata
        url = quote('/admin/services/{service}'.format(service=service))
        resp, body = self.http_client.json_request('PUT', url, body=json_data)
        return body
