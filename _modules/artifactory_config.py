# -*- coding: utf-8 -*-
'''
Module for configuring Artifactory.
change admin password
add license key
confingure ldap
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

__virtualname__ = 'artifactory_config'


def __virtual__():

    return True



#    "repoLayoutRef" : "maven-2-default",

class Artifactoryconfig:

    def __init__(self, config={}):

        self.files = []
        self.def_password = 'password'
        self.def_user= 'admin'


        client_config = {
            'artifactory_url': 'http://your-instance/artifactory/api',
            'username': 'your-user',
            'password': 'password',
            'license_key' :'key',
            'artifactory_ldap_url': 'http://localhost',
#            'headers': {'Content-type': 'application/json'},
            'ssl_verify': True
        }

        client_config.update(config)

        # Set instance variables for every value in party_config
        for k, v in client_config.items():
            setattr(self, '%s' % (k,), v)

    def change_admin_password(self,  **connection_args):
        """
        Usage: POST /api/security/users/authorization/changePassword  -H "Content-type: application/json" -d ' { "userName" : "{user}", "oldPassword" : "{old password}", "newPassword1" : "{new password}", "newPassword2" : "{verify new password}" }
        :param connection_args:
        :return: 0 if ok
        """

        url = self.artifactory_url + '/security/users/authorization/changePassword'
        log.error(str(url))
        data_pass={ "userName": self.def_user, "oldPassword": self.def_password, "newPassword2": self.password,"newPassword1": self.password}
        auth = (self.username, self.def_password)

        r = requests.post(url, auth=auth, json=data_pass)
        log.error(str(r.text))
        return r

    def add_license_key(self, **connection_args):
        """
        Usage: POST /api/system/license
        :param connection_args:
        :return: 0 if ok
        """
        url = self.artifactory_url +'/system/license'
        log.error(str(url))
        auth = (self.username, self.password)
        key = {"licenseKey": self.license_key}
        log.error(str(key))
        r = requests.post(url, auth=auth, json=key)
        log.error(str(r.text))
        return r

    def configure_ldap(self, **connection_args):
        url = self.artifactory_url + '/system/configuration'
        auth = (self.username, self.password)
        # r = requests.post(url,auth=auth,json=data)

        r = requests.get(url, auth=auth)
        # print json.dumps(r.text)
        #log.error(str(r.text))

        ldap_url = self.artifactory_ldap_url
        searchFilter = "uid={0}"
        xmlTemplate = """
                    <ldapSetting>
                        <key>ldap</key>
                        <enabled>true</enabled>
                        <ldapUrl>%(url)s</ldapUrl>
                        <search>
                            <searchFilter>%(sf)s</searchFilter>
                            <searchSubTree>true</searchSubTree>
                        </search>
                        <autoCreateUser>true</autoCreateUser>
                        <emailAttribute>mail</emailAttribute>
                        <ldapPoisoningProtection>true</ldapPoisoningProtection>
                    </ldapSetting>
                    """
        xml_date = {'url': ldap_url, 'sf': searchFilter}
        a = xmlTemplate % xml_date
#        log.error(str( r.text))
        z = str(r.text).split('<ldapSettings/>')
        out = str(z[0] + '<ldapSettings>' + a + '</ldapSettings>' + z[1])

        # out=str(r.text).split('<ldapSettings/>')[0]+'<ldapSettings/>'+str(r.text).split('<ldapSettings/>')[1]
        headers = {'Content-Type': 'application/xml'}

        r = requests.post(url, auth=auth, data=out, headers=headers)
        log.error(str(r.text))
        return r

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
      'ssl_verify': get('ssl_verify', True),'license_key':get('license_key','key'),'artifactory_ldap_url':get('ldap_server','url'),
      'ldap_searchFilter':get('ldap_searchFilter','uid={0}'),'ldap_account_base':get('ldap_account_base','accaunt')
    }

    user = get('user', False)
    password = get('password', False)
    if user and password:
      client_config['username'] = user
      client_config['password'] = password

    artifactory_config = Artifactoryconfig(client_config)

    return artifactory_config



def artifactory_init(**connection_args):

    artifactory = _client(**connection_args)
    artifactory.change_admin_password()
    artifactory.add_license_key()
    artifactory.configure_ldap()

