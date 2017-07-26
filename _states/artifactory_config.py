# -*- coding: utf-8 -*-
'''
Management of artifactory configuration
======================================

:depends:   - requests Python module
:configuration: See :py:mod:`salt.modules.artifactory` for setup instructions.
'''

def __virtual__():
    '''
    Only load if the artifactory module is in __salt__
    '''
    return True


def artifactory_init( **kwargs):
    
    out = __salt__['artifactory_config.artifactory_init']( **kwargs)

    return out
