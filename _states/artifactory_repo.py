# -*- coding: utf-8 -*-
'''
Management of artifactory repositories
======================================

:depends:   - requests Python module
:configuration: See :py:mod:`salt.modules.artifactory` for setup instructions.

.. code-block:: yaml

    local_artifactory_repo:
      artifactory_repo.repo_present:
      - name: remote_artifactory_repo
      - package_type: generic
      - repo_type: local
    remote_artifactory_repo:
      artifactory_repo.repo_present:
      - name: remote_artifactory_repo
      - repo_type: remote
      - url: "http://totheremoterepo:80/"

'''

def __virtual__():
    '''
    Only load if the artifactory module is in __salt__
    '''
    return True


def repo_present(name, repo_type, package_type, url=None, **kwargs):
    '''
    Ensures that the artifactory repo exists
    
    :param name: new repo name
    :param description: short repo description
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Repository "{0}" already exists'.format(name)}

    # Check if repo is already present
    repo = __salt__['artifactory_repo.repo_get'](name=name, **kwargs)

    if 'Error' not in repo:
        #update repo
        pass
    else:
        # Create repo
        __salt__['artifactory_repo.repo_create'](name, repo_type, package_type, url, **kwargs)
        ret['comment'] = 'Repository "{0}" has been added'.format(name)
        ret['changes']['repo'] = 'Created'
    return ret
