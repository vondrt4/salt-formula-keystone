import io
import json
import logging

LOG = logging.getLogger(__name__)


def __virtual__():
    return True


def rule_list(path, **kwargs):
    try:
        with io.open(path, 'r') as file_handle:
            rules = json.loads(file_handle.read())
        rules =  {str(k): str(v) for (k, v) in rules.items()}
    except Exception as e:
        msg = "Unable to load policy JSON %s: %s" % (path, repr(e))
        LOG.debug(msg)
        rules = {'Error': msg}
    return rules


def rule_delete(name, path, **kwargs):
    ret = {}
    rules = __salt__['keystone_policy.rule_list'](path, **kwargs)
    if 'Error' not in rules:
        if name not in rules:
            return ret
        del rules[name]
        try:
            with io.open(path, 'w') as file_handle:
                file_handle.write(unicode(json.dumps(rules, indent=4)))
        except Exception as e:
            msg = "Unable to save policy json: %s" % repr(e)
            LOG.error(msg)
            return {'Error': msg}
        ret = 'Rule {0} deleted'.format(name)
    return ret


def rule_set(name, rule, path, **kwargs):
    rules = __salt__['keystone_policy.rule_list'](path, **kwargs)
    if 'Error' not in rules:
        if name in rules and rules[name] == rule:
            return {name: 'Rule %s already exists and is in correct state' % name}
        rules.update({name: rule})
        try:
            with io.open(path, 'w') as file_handle:
                file_handle.write(unicode(json.dumps(rules, indent=4)))
        except Exception as e:
            msg = "Unable to save policy JSON %s: %s" % (path, repr(e))
            LOG.error(msg)
            return {'Error': msg}
        return rule_get(name, path, **kwargs)
    return rules


def rule_get(name, path, **kwargs):
    ret = {}
    rules = __salt__['keystone_policy.rule_list'](path, **kwargs)
    if 'Error' in rules:
        ret['Error'] = rules['Error']
    elif name in rules:
        ret[name] = rules.get(name)

    return ret

