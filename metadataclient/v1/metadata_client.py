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

from muranoclient.common import base


# class MetadataClient(base.Resource):
#     def __repr__(self):
#         return "<Metadata Client %s>" % self._info
#
#
# class MetadataClientManager(base.Manager):
#     resource_class = MetadataClient
#
#     def get_ui_archive(self):
#         return self._get('/v1/client/ui')
#
#     def conductor(self):
#         return self._get('/v1/client/conductor')

class Controller(object):
    def __init__(self, http_client):
        self.http_client = http_client

    def get_ui_data(self):
        """
        Download tar.gz with

        """
        url = '/v1/client/ui'
        resp, body = self.http_client.archive_request('GET', url)
        return body

    def get_conductor_data(self):
        """
        Download tar.gz with

        """
        url = '/v1/client/conductor'
        resp, body = self.http_client.archive_request('GET', url)
        return body