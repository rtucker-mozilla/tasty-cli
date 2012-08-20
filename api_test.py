#!/usr/bin/python
import sys
import argparse
from MozInventoryCLI import MozInventoryCLI

if __name__ == '__main__':

    m = MozInventoryCLI()
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    #parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(dest='command')
    # create the parser for the "a" command
    namespaces = m.list_namespaces()
    native_args = [
            'create',
            'delete',
            'update',
            'search',
            'read',
            ]
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

        for sc in schema['fields'].iterkeys():
            tmp.add_argument(
                '--%s' % sc,
                #type=string,
                help=schema['fields'][sc]['help_text'],
                )
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
