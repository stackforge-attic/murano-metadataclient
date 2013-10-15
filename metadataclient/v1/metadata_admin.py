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


class MetadataAdmin(base.Resource):
    def __repr__(self):
        return "<Metadata Client %s>" % self._info


class MetadataAdminManager(base.Manager):
    resource_class = MetadataAdmin

    def list_ui(self, path=None):
        if path:
            return self._list('/v1/admin/ui/{path}'.format(path=path))
        else:
            return self._list('/v1/admin/ui')

    def list_agent(self, path=None):
        if path:
            return self._list('/v1/admin/agent/{path}'.format(path=path))
        else:
            return self._list('/v1/admin/agent')

    def list_heat(self, path=None):
        if path:
            return self._list('/v1/admin/heat/{path}'.format(path=path))
        else:
            return self._list('/v1/admin/heat')

    def list_workflows(self, path=None):
        if path:
            return self._list('/v1/admin/workflows/{path}'.format(path=path))
        else:
            return self._list('/v1/admin/workflows')

    def list_scripts(self, path=None):
        if path:
            return self._list('/v1/admin/scripts/{path}'.format(path=path))
        else:
            return self._list('/v1/admin/scripts')

    def get_file(self):
    #application/octet
        pass
