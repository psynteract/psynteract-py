# Copyright 2015- Felix Henninger
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division

import requests
import pycouchdb
import json
import random

class Connection(object):
    def __init__(self, server_uri, db_name,
        client_name=None, design='stranger',
        group_size=2, groupings_needed=1, roles=None, ghosts=False,
        group='default', initial_data={}, offline=False):
        # Set offline mode
        self.offline = offline

        if not self.offline:
            self.server = pycouchdb.Server(server_uri)
            self.db = self.server.database(db_name)
            self.session = self.latest_session
            # TODO: Fail if db does not contain psynteract
            # design documents
        else:
            self.session = 'offline'

        # Populate the client document
        self.doc = {
            'data': initial_data,
            'session': self.session,
            'group': group,
            'type': 'client',
            'design': {
                'type': design,
                'group_size': group_size,
                'groupings_needed': groupings_needed,
                'roles': roles,
                'ghosts': ghosts,
                }
            }

        if offline:
            self.doc['_id'] = 'offline'

        self.design = design
        self.group_size = group_size
        self.groupings = groupings_needed
        self.roles = roles

        # Show warning if roles are used in offline mode
        if offline and roles:
            print('Warning: You are using roles in offline mode. '
                'This is tricky and may lead to complications. '
                'To be on the safe side, we recommend simulating. '
                'a complete lab environment or using dummies (if '
                'you are using code to build the experiment).')

        # Start with the first grouping
        self.current_grouping = 0

        # Set a client name/description if one is provided
        if client_name:
            self.doc['name'] = client_name

        # Push all data to the server
        self.push()

    @property
    def latest_session(self):
        # Query database to find open sessions,
        # be sure to reverse the order so that the most recent
        # ones appear on top
        sessions = self.db.query('psynteract/open_sessions', descending='true')

        # Select the most recent session and return its id
        try:
            return list(sessions)[0]['id']
        except IndexError:
            raise KeyError('There is no open session available')

    def push(self):
        if not self.offline:
            self.doc = self.db.save(self.doc)
        else:
            pass

    def refresh(self):
        if not self.offline:
            self.doc = self.db.get(self._id)
        else:
            pass

    @property
    def data(self):
        return self.doc['data']

    @property
    def _id(self):
        try:
            return self.doc['_id']
        except KeyError:
            return None

    @property
    def _rev(self):
        try:
            return self.doc['_rev']
        except KeyError:
            return None

    def get(self, doc, offline_dummy=[]):
        if not self.offline:
            return self.db.get(doc)
        else:
            import collections
            if isinstance(offline_dummy, dict):
                return offline_dummy
            elif isinstance(offline_dummy, collections.Iterable) and len(offline_dummy) is not 0:
                return random.choice(offline_dummy)
            else:
                return self.doc

    def await(self, condition=lambda doc: True,
        check='clients', check_function=all,
        timeout=None, heartbeat=1000):

        check_type = 'client' if check == 'clients' else check

        if self.offline:
            # Do not wait in offline mode, but return
            # directly instead.
            return
        else:
            # TODO: Check only a couple of documents,
            # e.g. not the client's own, allies/session
            # only
            last_seq = self.db.resource.get()[1]['update_seq']

            # Prepopulate a dictionary of the relevant
            # documents' ids onto whether the specified
            # condition is met.
            # This process works slightly differently
            # depending on which documents are checked,
            # but the end result is always the same.
            if check is 'session':
                condition_met = {self.session: condition(self.db.get(self.session))}
            elif check is 'partners':
                # FIXME: Test this!
                condition_met = {doc['id']: condition(doc['doc'])
                    for doc in self.db.query('psynteract/session_clients', \
                        key=self.session, type='client', include_docs='true')
                        if doc['id'] in self.current_partners}
            else:
                condition_met = {doc['id']: condition(doc['doc'])
                    for doc in self.db.query('psynteract/session_clients', \
                        key=self.session, type='client', include_docs='true')}

            if check_function(condition_met.values()):
                # If all relevant documents test positive
                # at this point, stop waiting.
                return
            else:
                # Otherwise keep going, listening for changes
                # to the database and updating the dictionary
                # accordingly.
                while True:
                    r = self.db.resource.get(
                        '_changes',
                        params={
                            'feed': 'continuous',
                            'filter': 'psynteract/clients',
                            # 'key': '"' + self.session + '"',
                            'session': self.session,
                            'type': check_type,
                            'since': last_seq,
                            'include_docs': 'true',
                            'heartbeat': heartbeat,
                            'timeout': timeout
                        },
                        stream=True,
                        timeout=timeout/1000 if not timeout is None else None
                    )

                    for line in r[0].iter_lines(chunk_size=1):
                        if line: # filter out keep-alive new lines
                            change = json.loads(line.decode("utf-8"))
                            if not 'last_seq' in change.keys():
                                last_seq = change['seq']
                                condition_met[change['id']] = \
                                    condition(change['doc'])
                                if check_function(condition_met.values()):
                                    return
                            else:
                                last_seq = change['last_seq']

    def heartbeat(self):
        pass

    @property
    def current_partners(self):
        if self.offline:
            return [self._id] * (self.group_size - 1)
        else:
            # Using the current grouping state, extract the
            # other clients assigned to the current connection
            return self.get(self.session)['groupings']\
                [self.current_grouping]\
                [self._id]

    def get_role(self, player=None):
        # If no player is specified,
        # look up the client's own role
        if player == None:
            player = self._id

        # If no roles have been specified,
        # return 'None' in any case.
        if self.roles == None:
            return None
        elif self.offline:
            return self.roles[1]
        else:
            return self.get(self.session)['roles']\
                [self.current_grouping]\
                [player]

    @property
    def current_role(self):
        return self.get_role()

    @property
    def current_partner_roles(self):
        if self.offline:
            # In the offline mode, the client is partnered
            # with itself, so the following will return a
            # dictionary containing the client's own id,
            # followed by the first role specified.
            return dict(zip(
                self.current_partners,
                self.roles[1,]
            ))
        else:
            # In the online mode, with full access to other clients,
            # return a dictionary of ids mapping to roles
            # for each of the current partners.
            return {
                partner: get_role(partner)
                for partner in self.current_partners
            }

    def reassign_grouping(self, allow_rollover=False):
        # Switch to the next grouping available, and
        # return the currently assigned partners.
        if self.offline:
            # Mappings never switch in offline mode
            return self.current_partners
        else:
            self.current_grouping += 1

            # If rollovers are permitted, start from the
            # first grouping if the available groupings have
            # already been exceeded.
            if allow_rollover:
                self.current_grouping = self.current_grouping % self.groupings

            return self.current_partners

def install(db_uri, create_db=True):
    import os
    print('Locating backend blob')
    backend_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'backend.json'
        )

    print('Uploading backend')
    requests.put(
        db_uri + '/_design/psynteract',
        data=open(backend_path).read()
        )
    return db_uri + '/_design/psynteract/index.html'
