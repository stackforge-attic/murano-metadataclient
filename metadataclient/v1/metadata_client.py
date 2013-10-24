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


class Controller(object):
    def __init__(self, http_client):
        self.http_client = http_client

    def _get_data(self, endpoint_type, hash_sum=None):
        if hash_sum:
            url = '/v1/client/{0}?hash={1}'.format(endpoint_type, hash_sum)
        else:
            url = '/v1/client/{0}'.format(endpoint_type)
        return self.http_client.raw_request('GET', url)

    def get_ui_data(self, hash_sum=None):
        """
        Download tar.gz with ui metadata. Returns a tuple
        (status, body_iterator) where status can be either 200 or 304. In the
        304 case there is no sense in iterating with body_iterator.

        """
        return self._get_data('ui', hash_sum=hash_sum)

    def get_conductor_data(self, hash_sum=None):
        """
        Download tar.gz with conductor metadata. Returns a tuple
        (status, body_iterator) where status can be either 200 or 304. In the
        304 case there is no sense in iterating with body_iterator.

        """
        return self._get_data('conductor', hash_sum=hash_sum)
