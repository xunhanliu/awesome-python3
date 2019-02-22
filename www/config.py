#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Configuration
'''

__author__ = 'Michael Liao'

import config_default


class Dict(dict):
    '''
    Simple dict but support access as x.y style.原生的dict不支持x.y形式的属性操作，这里进行了支持。
    也支持传入两个tuple,分别自建dict的key和value
    '''

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    '''
    注意override新的key不起作用。
    :param defaults:
    :param override:
    :return:
    '''
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)
if __name__=='__main__':
    ex0={"n0":123,"n1":444,"n2":{"a":11,"b":22}}
    ex0=dict(ex0)
    ex1=Dict(("a","s","d"),(1,2,3))
    ex1 = Dict(**ex0)
    a={'1': 1, '2': 2}
    b={'3': 3, '4': 4}
    c = merge(a, b)
    a=0