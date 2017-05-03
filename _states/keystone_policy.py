#!/usr/bin/env python
'''
Management of policy.json
=========================

Merge user defined hash to policy.json
--------------------------------------

.. code-block:: yaml

/etc/keystone/policy.json:
  keystone_policy.present:
    - override_data:
        override_key: override_value
    - formatter: json

'''
import logging
import json

log = logging.getLogger(__name__)

JSON_LOCATION = '/etc/keystone/policy.json'


def _deep_merge(dct, merge_dct):
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)):
            _deep_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def present(name, override_data={}, **kwargs):
    '''
    Ensures that given key present in policy.json file. This is a wrapper
    around file.serialize state with additional argument: override_data.
    Rest parameters of file.serialize can be safely used as well.
    Function reads contents of existing policy.json file into a python
    dictionary. User defined data populated to this dictionary using deep
    merge procedure.

    :param name:          Name of the resource
    :param override_data: User defined data with overrides
    '''
    with open(JSON_LOCATION) as policy_json:
        json_content = json.load(policy_json)

    _deep_merge(json_content, override_data)

    kwargs['dataset'] = json_content
    ret = __states__['file.serialize']('/etc/keystone/policy.json', **kwargs)
    return ret
