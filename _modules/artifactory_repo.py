# -*- coding: utf-8 -*-
'''
Module for fetching artifacts from Artifactory
'''

# Import python libs
from __future__ import absolute_import
import os
import base64
import logging

# Import Salt libs
import salt.utils
import salt.ext.six.moves.http_client  # pylint: disable=import-error,redefined-builtin,no-name-in-module
from salt.ext.six.moves import urllib  # pylint: disable=no-name-in-module
from salt.ext.six.moves.urllib.error import HTTPError, URLError  # pylint: disable=no-name-in-module

import json
import requests

log = logging.getLogger(__name__)

__virtualname__ = 'artifactory_repo'


def __virtual__():

    return True


repo_config = {
    "key": "local-repo1",
    "rclass" : "local",
    "packageType": "generic",
    "description": "The local repository public description",
}

#    "repoLayoutRef" : "maven-2-default",

class ArtifactoryClient:

    def __init__(self, config={}):

        self.files = []

        client_config = {
            'artifactory_url': 'http://your-instance/artifactory/api',
            'search_prop': 'search/prop',
            'search_name': 'search/artifact',
            'search_repos': 'repositories',
            'username': 'your-user',
            'password': 'password',
            'headers': {'Content-type': 'application/json'},
            'ssl_verify': True
        }

        client_config.update(config)

        # Set instance variables for every value in party_config
        for k, v in client_config.items():
            setattr(self, '%s' % (k,), v)

    def create_repository(self, name, config, **connection_args):
        repositories = []

        query = "%s/%s/%s" % (self.artifactory_url, self.search_repos, name)
        auth = (self.username, self.password)

        r = requests.put(query, auth=auth, json=config, verify=self.ssl_verify)
        print(r.content)

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return []
        response = json.loads(raw_response.text)
        for line in response:
            for item in line:
                repositories.append(line)

        if repositories:
            return repositories

        return []


    def get_repositories(self, repo_type=None, **connection_args):
        repositories = []

        if repo_type is None:
            query = "%s/%s" % (self.artifactory_url, self.search_repos)
        else:
            query = "%s/%s?type=%s" % (self.artifactory_url,
                                       self.search_repos, repo_type)

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return []
        response = json.loads(raw_response.text)
        for line in response:
            for item in line:
                repositories.append(line)

        if repositories:
            return repositories

        return []


    def query_artifactory(self, query, query_type='get'):
        """
        Send request to Artifactory API endpoint.
        @param: query - Required. The URL (including endpoint) to send to the Artifactory API
        @param: query_type - Optional. CRUD method. Defaults to 'get'.
        """

        auth = (self.username, self.password)
        query_type = query_type.lower()

        if query_type == "get":
            response = requests.get(query, auth=auth, headers=self.headers, verify=self.ssl_verify)
        elif query_type == "put":
            response = requests.put(query, data=query.split('?', 1)[1], auth=auth, headers=self.headers, verify=self.ssl_verify)
        if query_type == "post":
            pass

        if not response.ok:
            return None

        return response

    def query_file_info(self, filename):
        """
        Send request to Artifactory API endpoint for file details.
        @param: filename - Required. The shortname of the artifact
        """
        query = "%s/storage/%s" % (self.artifactory_url, filename)

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)

        return response

    def find_by_properties(self, properties):
        """
        Look up an artifact, or artifacts, in Artifactory by using artifact properties.
        @param: properties - List of properties to use as search criteria.
        """
        query = "%s/%s?%s" % (self.artifactory_url,
                              self.search_prop, urlencode(properties))
        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response

        response = json.loads(raw_response.text)

        for item in response['results']:
            for k, v in item.items():
                setattr(self, '%s' % (k,), v)

        if not response['results']:
            return None

        artifact_list = []
        for u in response['results']:
            artifact_list.append(os.path.basename(u['uri']))

        self.files = artifact_list
        setattr(self, 'count', len(artifact_list))

        return "OK"

    def find(self, filename):
        """
        Look up an artifact, or artifacts, in Artifactory by
        its filename.
        @param: filename - Filename of the artifact to search.
        """
        query = "%s/%s?name=%s" % (self.artifactory_url,
                                   self.search_name, filename)
        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)
        if len(response['results']) < 1:
            return None

        setattr(self, 'name', filename)
        setattr(self, 'url', json.dumps(response))

        return "OK"

    def get_properties(self, filename, properties=None):
        """
        Get an artifact's properties, as defined in the Properties tab in
        Artifactory.
        @param: filename - Filename of artifact of which to get properties.
        @param: properties - Optional. List of properties to help filter results.
        """
        if properties:
            query = "%s?properties=%s" % (filename, ",".join(properties))
        else:
            query = "%s?properties" % filename

        raw_response = self.query_artifactory(query)
        if raw_response is None:
            return raw_response
        response = json.loads(raw_response.text)
        for key, value in response.items():
            setattr(self, '%s' % (key,), value)

        return "OK"


def _client(**connection_args):
    '''
    Set up artifactory credentials

    '''

    prefix = "artifactory"

    # look in connection_args first, then default to config file
    def get(key, default=None):
        return connection_args.get('connection_' + key,
            __salt__['config.get'](prefix, {})).get(key, default)

    client_config = {
      'artifactory_url': '%s://%s:%s/artifactory/api' % (get('proto', 'http'), get('host', 'localhost'), get('port', '8080')),
      'ssl_verify': get('ssl_verify', True)
    }

    user = get('user', False)
    password = get('password', False)
    if user and password:
      client_config['username'] = user
      client_config['password'] = password

    artifactory_client = ArtifactoryClient(client_config)

    return artifactory_client


def repo_list(repo_type=None, **connection_args):
    '''
    Return a list of available repositories

    CLI Example:

    .. code-block:: bash

        salt '*' artifactory_repo.repo_list
        salt '*' artifactory_repo.repo_list REMOTE
        salt '*' artifactory_repo.repo_list LOCAL
    '''
    ret = {}

    artifactory = _client(**connection_args)
    repos = artifactory.get_repositories(repo_type)

    for repo in repos:
        if 'key' in repo:
            ret[repo.get('key')] = repo
    return ret


def repo_get(name, **connection_args):
    '''
    Return a list of available repositories

    CLI Example:

    .. code-block:: bash

        salt '*' artifactory_repo.repo_get reponame
    '''

    ret = {}

    repos = repo_list(None, **connection_args)
    if not name in repos:
        return {'Error': "Error retrieving repository {0}".format(name)}
    ret[name] = repos[name]
    return ret


def repo_create(name, repo_type="local", package="generic", url=None, **connection_args):
    '''
    Create a artifactory repository

    :param name: new repo name
    :param repo_type: new repo type
    :param package: new repo package type
        "gradle" | "ivy" | "sbt" | "nuget" | "gems" | "npm" | "bower" |
        "debian" | "pypi" | "docker" | "vagrant" | "gitlfs" | "yum" |
        "generic"


    CLI Examples:

    .. code-block:: bash

        salt '*' artifactory_repo.repo_create projectname remote generic

    '''
    ret = {}

    if url in connection_args and url == None:
        url = connection_args['url']

    repo = repo_get(name, **connection_args)

    if repo and not "Error" in repo:
        log.debug("Repository {0} exists".format(name))
        return repo

    repo_config = {
        "key": name,
        "rclass" : repo_type,
        "packageType": package,
        "description": "The local repository public description",
    }

    if repo_type == "remote":
        repo_config['url'] = url

    artifactory = _client(**connection_args)
    artifactory.create_repository(name, repo_config)
    return repo_get(name, **connection_args)
