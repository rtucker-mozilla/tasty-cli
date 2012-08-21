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
    """
        Stub class to simply mimic that of the tastypie api
    """

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
    """
        Decide if we want to use the cached file or hit the api
    """
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
    load_interface_defs(subparsers)
    return parser

def load_interface_defs(subparsers):
    tmp = subparsers.add_parser('interface', help='Interface Manipulation')
    tmp.add_argument('--create', help='create interface', action='store_true')
    tmp.add_argument('--site', help='', action='store')
    tmp.add_argument('--vlan', help='', action='store')
    tmp.add_argument('--base-domain', help='', action='store')
    tmp.add_argument('--network', help='', action='store')
    tmp.add_argument('--range', help='', action='store')
    tmp.add_argument('--ip', help='', action='store')
    tmp.add_argument('--mac', help='', action='store')
    tmp.add_argument('--label', help='', action='store')
    tmp.add_argument('--fqdn', help='', action='store')
    tmp.add_argument('--type', help='', action='store')
    tmp.add_argument('--primary', help='', action='store')
    tmp.add_argument('--alias', help='', action='store')
    tmp.add_argument('--system', help='', action='store')


def pickled():
    return build_response(False)

def file_age_in_seconds(pathname):
    import time, stat
    return time.time() - os.stat(pathname)[stat.ST_MTIME]

def load_args():
    """
        If the pickle file doesn't exist, let's create it
    """

    if not os.path.exists(pickle_file):
        return refresh()

    """
        check to see if the pickle file is too old. If it is,
        create a new one
        If it's less than the expiration, use the pickle file
    """

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
            if cmd.__dict__[na] is not None and\
                na != 'argument__' and na != 'command':
                action_dict[na] = cmd.__dict__[na]

    if not cmd.command == 'interface':
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

    else:
        if cmd.create:
            if not cmd.system:
                print "--system argument is required to create an interface"
                sys.exit(2)
            else:
                print cmd.system

            if not cmd.mac:
                print "--mac argument is required to create an interface"
                sys.exit(2)
            else:
                print cmd.mac

            if cmd.range and cmd.ip:
                print "--range and --ip are mutually exclusive"
                sys.exit(2)

            if not cmd.range and not cmd.ip:
                print "--range or --ip argument is required to create an interface"
                sys.exit(2)

            update_dict = {
                    'auto_create_interface': True,
                    'mac_address': cmd.mac,
                    }
            print m.update('system', cmd.system, update_dict)







