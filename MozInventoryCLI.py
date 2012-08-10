import sys, os
from tastypie_client import Api 
import tastypie_client.exceptions


class MozInventoryCLI(object):
    _api = None
    _auth = None
    _is_test = False
    _mock_api = None
    _is_test = False
    _return_code = 0
    _return_text = ''
    _credential_file = None

    def __init__(self, url=None, username=None, password=None, is_test=False, mock_api=None):
        self._credential_file = "%s/.tasty-cli" % os.path.expanduser('~')
        self._is_test = is_test
    
        if not self._is_test:
            self._auth = self._get_credentials(self._credential_file)
            url = self._get_url(self._credential_file)
            self._api = Api(url, auth=self._auth)
        else:
            self._api = mock_api
   
    def _cleanup(self):
        if not self._is_test:
            print self._return_text
            sys.exit(self._return_code)

    def _get_credentials(self, file):
        file_text = self._read_credential_file(file)
        file_split = file_text.split("\n")
        return (file_split[0], file_split[1])

    def _get_url(self, file):
        file_text = self._read_credential_file(file)
        file_split = file_text.split("\n")
        return file_split[2]

    def _read_credential_file(self, file):
        return open(file).read()

    def list_namespaces(self):
        endpoints = self._api.get_endpoints()
        ret = ''
        for e in endpoints.iterkeys():
            ret += '%s\n' % e
        self._return_text = ret
        self._cleanup()

    def list_schema_urls(self, the_obj=None):
        endpoints = self._api.get_endpoints()
        ret = ''
        for e in endpoints.iterkeys():
            if not the_obj:
                ret += '%s: %s\n' % (e, endpoints[e]['schema'] )
            else:
                ret += '%s: %s\n' % (e, endpoints[e]['schema'] ) if the_obj == e else ''
        self._return_code = 0
        self._return_text = ret
        self._cleanup()

    def create(self, type, arg_dict):
        status, result = getattr(self._api, type).create(**arg_dict)
        if status:
            print 
            self._return_text = "Success: %s" % result
        else:
            self._return_text = "Fail: %s" % result
            self.return_code = 2
        self._cleanup()

    def delete(self, type, id):
        try:
            status, result = getattr(self._api, type)(id).delete()
            print "Success: %s" % result
        except tastypie_client.exceptions.BadHttpStatus:
            print "Unable to delete"
            self.return_code = 1
        self._cleanup()

    def update(self, type, obj, arg_dict):
        updatable = getattr(self._api, type)(obj)
        for arg in arg_dict.iterkeys():
            setattr(updatable, arg, arg_dict[arg])
        status, result = updatable.save()
        if status:
            print "Success"
        else:
            print "Error: %s" % result
        self._cleanup()


    def search(self, type, arg_dict):
        icontains_arg_dict = {}
        for a in arg_dict.iterkeys():
            b = "%s__icontains" % a
            icontains_arg_dict[b] = arg_dict[a]
        try:
            type_attr = getattr(self._api, type)
        except AttributeError:
            print "Invalid search type %s" % (type)
            self.return_code = 2
        search_result = type_attr.find(**icontains_arg_dict)
        if len(search_result) > 0:
            for r in search_result:
                print r._url
        else:
            print 'No results found'
            self.return_code = 1
    def read(self, type, obj):
        try:
            obj = getattr(self._api, type)(obj)
            for key in sorted(obj._resource.iterkeys()):
                value = obj._resource[key]
                cls = str(value.__class__)
                lpr = "<class 'tastypie_client.core.ListProxy'>"
                if cls != "<type 'dict'>"and cls != lpr and value:
                    self._return_text += "%s: %s\n" % (key, str(value).strip() if value else '' )
                elif str(value.__class__) == "<type 'dict'>":
                    for inner_key in value.iterkeys():
                        self._return_text += "%s.%s: %s\n" % (key, inner_key, value[inner_key])
                elif str(value.__class__) == "<class 'tastypie_client.core.ListProxy'>":
                    for __dict in value:
                        for key in __dict.iterkeys():
                            if key != 'id' and key=='interface':
                                self._return_text += "%s:%s:%s: %s\n" % (key, __dict['interface'], key, __dict[key])
                            elif key != 'id':
                                self._return_text += "%s.%s.%s: %s\n" % (key, __dict['id'], key, __dict[key])
        except Exception, e:
            print 'Fail: Object not found'
            self.return_code = 1
        self._cleanup()

    def schema(self, the_obj):
        the_schema = self._api.get_schema(the_obj)
        for f in the_schema['fields'].iterkeys():
            if f != 'resource_uri':
                print "%s:" % f,\
                    "\n\tnullable=%s," % the_schema['fields'][f]['nullable'], \
                    "\n\tdefault='%s'," % the_schema['fields'][f]['default'], \
                    "\n\ttype='%s'," % the_schema['fields'][f]['type'], \
                    "\n\texample='%s'," % the_schema['fields'][f]['help_text'], \
                    "\n\tunique='%s'\n" % the_schema['fields'][f]['unique'] 
