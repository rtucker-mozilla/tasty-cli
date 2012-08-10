#!/usr/bin/python
import sys
from MozInventoryCLI import MozInventoryCLI

if __name__ == '__main__':
    m = MozInventoryCLI()
    arg_len = len(sys.argv)
    action = sys.argv[1]
    if arg_len == 2:
        print m.list_namespaces() if action == 'list' else ''
        print m.list_schema_urls() if action == 'schema_urls' else ''

    elif arg_len == 3:
        m.list_schema_urls(sys.argv[2]) if action == 'schema_urls' else ''
        m.schema(sys.argv[2]) if action == 'schema' else ''

    elif action =='read' or action == 'search':
        if action == 'search':
            type = sys.argv[2]
            arg_dict = {}
            for x in sys.argv[3:]:
                try:
                    the_split = x.split("=")
                    arg_dict[the_split[0]] = the_split[1]
                except Exception, e:
                    import pdb; pdb.set_trace()
            m.search(type, arg_dict)
        if action == 'read':
            type = sys.argv[2]
            obj = sys.argv[3]
            m.read(type, obj)
    elif arg_len > 3 and action !='read' and action != 'search':
        if action == 'update':
            type = sys.argv[2]
            obj = sys.argv[3]
            arg_dict = {}
            for x in sys.argv[4:]:
                the_split = x.split("=")
                arg_dict[the_split[0]] = the_split[1]
            m.update(type, obj, arg_dict)

        if action == 'create':
            type = sys.argv[2]
            arg_dict = {}
            for x in sys.argv[3:]:
                the_split = x.split("=")
                arg_dict[the_split[0]] = the_split[1]
            m.create(type, arg_dict)

        if action == 'delete':
            type = sys.argv[2]
            id = sys.argv[3]
            m.delete(type, id)
