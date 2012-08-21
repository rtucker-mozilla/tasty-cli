#!/usr/bin/python
import sys, os
import argparse
from MozInventoryCLI import MozInventoryCLI
import pickle
pickle_file = "%s/.tasty-pickle" % os.path.expanduser('~')
pickle_file_expiration = 3600
native_args = [
        'create',
        'delete',
        'update',
        'search',
        'read',
        ]

m = MozInventoryCLI()

class PickledResponse(object):
    namespaces = {}
    def __init__(self, ns):
        self.namespaces = ns

    def list_namespaces(self):
        return self.namespaces

    def schema(self, ns):
        return self.namespaces[ns]

def refresh():
    return build_response(should_pickle=True, moz_inv_object=m)

def build_response(should_pickle=True, moz_inv_object=None):
    if not should_pickle:
        pickled_response = pickle.load( open( pickle_file, "rb" ) )
        m = PickledResponse(pickled_response)
    else:
        m = moz_inv_object

    parser = argparse.ArgumentParser(prog='PROG')
    subparsers = parser.add_subparsers(dest='command')
    namespaces = {}
    for ns in m.list_namespaces().iterkeys():
        tmp = subparsers.add_parser(ns, help='api access to %s' % ns,)
        tmp.add_argument('--create', help='ACTION: create %s' % ns, action='store_true')
        tmp.add_argument('--delete', help='ACTION: create %s' % ns, action='store_true')
        tmp.add_argument('--update', help='ACTION: update %s' % ns, action='store_true')
        tmp.add_argument('--search', help='ACTION: search for %s' % ns, action='store_true')
        tmp.add_argument('--read', help='ACTION: read %s' % ns, action='store_true')
        if '--create' not in sys.argv and '--delete' not in sys.argv and '--search' not in sys.argv:
            tmp.add_argument('argument__', help='OBJECT to act upon', action='store')
        schema = m.schema(ns)
        if should_pickle:
            namespaces[ns] = schema
        for sc in schema['fields'].iterkeys():
            tmp.add_argument(
                '--%s' % sc,
                help=schema['fields'][sc]['help_text'],
                )
    if should_pickle:
        pickle.dump( namespaces, open( pickle_file, "wb" ) )
    return parser

def pickled():
    return build_response(False)

def file_age_in_seconds(pathname):
    import time, stat
    return time.time() - os.stat(pathname)[stat.ST_MTIME]

def load_args():
    if not os.path.exists(pickle_file):
        return refresh()

    if file_age_in_seconds(pickle_file) > pickle_file_expiration:
        return refresh()
    else:
        return pickled()

if __name__ == '__main__':

    parser = load_args()

    cmd = parser.parse_args()
    action_dict = {}
    for na in cmd.__dict__:
        if na not in native_args:
            if cmd.__dict__[na] is not None and na != 'argument__' and na != 'command':
                action_dict[na] = cmd.__dict__[na]
    if cmd.update:
        m.update(cmd.command, cmd.__dict__['argument__'], action_dict)

    if cmd.read:
        m.read(cmd.command, cmd.argument__)

    if cmd.create:
        m.create(cmd.command, action_dict)

    if cmd.delete:
        m.delete(cmd.command, action_dict)

    if cmd.search:
        m.search(cmd.command, action_dict)
