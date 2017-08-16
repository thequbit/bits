
from pyramid.response import Response

from pyramid.view import view_config

from .models import (
    Users,
    #Histories,
)

import datetime
import json
from uuid import UUID

def validate_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except:
        return None
    return val.hex == uuid_string.replace('-','')

# needs format month/day/year
def validate_date(d):
    _d = None
    try:
        _d = datetime.datetime.strptime(d, '%m/%d/%Y')
    except:
        pass
    return _d

def get_payload(request):

    #print("\npayload:")
    #print("\tbody:     %s" % request.body[0:100])

    payload = {}

    try:
    #if True:
        if request.body == '' or request.body == b'' or request.body == None:
            #print('\twarning:  request body empty')
            pass
        else:
            payload = request.json_body
            for key in payload:
                # hack: due_date_of_next
                if '_date' in key:
                    try:
                        payload[key] = datetime.datetime.strptime(payload[key], '%m/%d/%Y')
                    except:
                        try:
                            #2016-07-26T04:02:15.454275
                            payload[key] = datetime.datetime.strptime(payload[key].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                        except:
                            raise Exception("invalid date format")
                #
                # This is for the whole Boolean issue with sqlite3 and foreign key length thing ... or something like that.
                #
                elif key == 'enabled' or key == 'selected':
                    int(payload[key])
                    
    except Exception as ex:
        print("\tpayload parsing error:   %s" % ex)
        payload = None
    return payload

def get_params(request, cls):
    print('\nbuilding params:')
    params = {}
    for key in request.GET:
        if key in cls.__dict__:
            if key[-3:] == '_id':
                if validate_uuid4(request.GET[key]):
                    params[key] = request.GET[key]
                else:
                    print('\twarning! invalid id in key %s = "%s"' % (key, request.GET[key]))    
            else:
                params[key] = request.GET[key]
    print('\tparams:   ', params)
    return params

def build_paging(request):
    start = 0
    count = 2500
    if 'start' in request.GET and 'count' in request.GET:
        try:
            start = int(float(request.GET['start']))
            count = int(float(request.GET['count']))
            if count > 2500:
                count = 2500
        except:
            start = 0
            count = 2500
    #print('\npaging:')
    #print('\tstart:    %i' % start)
    #print('\tcount:    %i' % count)
    return start, count

def authenticate(request):
    token = None
    user = None
    print("\nauthenticate:")
    try:
        # get as token
        token = request.GET['token']
        print('\tresult:   token in GET param: "{0}"'.format(token))
    except:
        try:
            # get from session
            token = request.session['token']
            print('\tresult:   token in session: "{0}"'.format(token))
        except:
            try:
                # get from cookie
                token = request.cookies['token']
            except:
                print('\tresult:   warning! no token found')
                pass
    if token:
        print('\ttoken:   ', token)
        if validate_uuid4(token):
            user = Users.get_by_token(request.dbsession, token)
            if user:
                print('\tuser:    ', user.email)
                Users.update_last_login(request.dbsession, user)
            else:
                print('\tuser:     <none> ( could not find token )')
        else:
            print('\terror:    invalid token format. token = %s' % token)
            pass
    else:
        print('\terror:    no token found!')
        pass
    if user:
        print('\tuser:     %s' % user.id)
        print('\ttype:     %s' % user.user_type)
        pass
    else:
        print('\tuser:     warning! user not found')
        pass
    return user 

def set_history_payload(history, payload):
    found = False
    _ids = (
        'project_id',
        'supplier_id',
        'component_id',
        'modification_id',
        'assembly_id',
        'entity_id',
    );
    print("\n\n SET HISTORY PAYLOAD \n\n")
    for item in payload:
        for _id in _ids:
            print('\t\titem = {0}, _id = {1}', item, _id)
            if _id == item:
                print('\t\tEqual!', _id, item)
                history[item] = payload[item]
                found = True
                break
    if not found:
        raise Exception('error in history payload')
    print("\n\n SET HISTORY PAYLOAD \n\n")
    return history

def save_file(filename, input_file):
    ''' filename should be absolute path '''
    size = 0
    with open(filename, 'wb') as f:
        input_file.seek(0)
        while True:
            data = input_file.read(2<<16)
            if not data:
                break
            size += f.write(data)
    return size

class BaseRequest(object):

    def __init__(self, request):
        self.request = request
        print("\n\n--------------------------------")
        print("\nrequest:")
        print("\tclient:   %s" % self.request.client_addr)
        print("\tpath:     %s" % self.request.path)
        print("\tmethod:   %s" % self.request.method)
        print("\tparams:   %s" % self.request.GET)
        print("\tparams:   %s" % self.request.POST)
        print("\tfull url: %s" % self.request.url)
        
        self.start, self.count = build_paging(request)
        self.user = authenticate(request)
        self.payload = get_payload(request)
        self.params = get_params(request, self.cls)

    def auth(self, needs_admin=False):
        ret = False
        if self.user and self.user.enabled:
            print('\tuser.token: ', self.user.token)
            if needs_admin:
                if self.user.user_type == 'administrator' or self.user.user_type == 'system':
                    print("\tauth:     true ( with admin )")
                    ret = True
                else:
                    print("\tauth:     false ( with admin )")
                    ret = False
            else:
                print("\tauth:     true ( without admin )")
                ret = True
        else:
            print("\tauth:     false ( without admin )")
            self.request.response.status = 401
            ret = False
        return ret

    def validate(self, selective=False):
        '''
            selective = False - all req items are in payload
            selective = True - all payload items are in req
        '''
        valid = False
        req = None
        if hasattr(self, 'req'):
            req = self.req
        elif hasattr(self, 'cls') and hasattr(self.cls, 'req'):
            req = self.cls.req
        else:
            # no good ...
            raise Exception('missing req in class!')
        print('\nvalidate:')
        print('\tpayload:  {0}'.format(self.payload))
        print('\trequired: {0}'.format(req))
        print('\titems:')
        if selective:
            if self.payload:
                for item in self.payload:
                    if item in req:
                        print('\t          %s [ OKAY ]' % item)
                    else:
                        print('\t          %s [ INVALID ]' % item)
                if self.payload and all(r in req for r in self.payload):
                    print("\tvalid:    true")
                    valid = True
            else:
                print('\t          Warning! Empty payload.')
        else:
            if self.payload:
                for item in req:
                    if item in self.payload:
                        #print('\t          %s [ OKAY ] %s' % (item, self.payload[item]))
                        print('\t          %s [ OKAY ]' % item)
                    else:
                        print('\t          %s [ MISSING ]' % item)
            else:
                print('\t          Warning! Empty payload.')
            print('')
            if self.payload and all(r in self.payload for r in req):
                print("\tvalid:    true")
                valid = True
        if not valid:
            print("\tvalid:    false")
            self.request.response.status = 400
        return valid

    def __get(self):
        resp = {}
        if 'id' in self.request.matchdict and validate_uuid4(self.request.matchdict['id']):
            _id = self.request.matchdict['id']
            if _id != None and _id != 'null':
                print('\tget:')
                print('\tid:      valid (%s' % _id)
                thing = self.cls.get_by_id(
                    self.request.dbsession,
                    _id,
                )
                if thing:
                    resp = thing.to_dict()
                else:
                    self.request.response.status = 404
            else:
                print('\tid:      invalid ( %s )' % _id)
                self.request.response.status = 400
        else:
            print('\tid:      invalid ( missing )')
            self.request.response.status = 400
        #else:
        #    self.request.response.status = 404
        return resp

    def __get_collection(self):
        resp = []
        print('\nget collection:')
        things = self.cls.get_paged(
            self.request.dbsession,
            self.start,
            self.count,
        )
        print('\tcount:    %i' % len(things))
        if things:
            #print('\ttype:   json')
            #resp = Response(json.dumps([t.to_dict() for t in things]), content_type='application/json')
            resp = [t.to_dict() for t in things]
        #else:
        #    self.request.response.status = 404
        #    resp = Response('\n'.join([]))
        return resp    

    def __get_collection_by(self):
        resp = []
        print('\nget collection by:')
        #things = self.cls.get_paged(
        #    self.request.dbsession,
        #    self.start,
        #    self.count,
        #)
        if len(self.params):
            things = self.cls.get_by(
                self.request.dbsession,
                self.params,
                self.start,
                self.count,
            )
            print('\tcount:    %i' % len(things))
            if things:
                resp = [t.to_dict() for t in things]
        else:
            print('error: self.params is empty.')
            self.request.response.status = 400
        return resp

    def __post(self):
        resp = {}
        print('\npost:')
        if self.validate():
            if 'author_id' in self.cls.__dict__ and not 'author_id' in self.payload:
                print('\tnote: adding author_id to payload for class %s' % self.cls.__single__)
                self.payload.update(
                    author_id=self.user.id,
                )
            thing = self.cls.add(self.request.dbsession, **self.payload)
            if thing:
                print('\tcreation: successful')
                resp = thing.to_dict()
                #history_payload = dict(
                #    creator_id=self.user.id,
                #    action='CREATION',
                #    description='Created New {0}.'.format(self.cls.__single__),
                #)
                #history_payload['{0}_id'.format(self.cls.__single__.replace(' ', '_').lower())] = thing.id
                #history_payload = set_history_payload(history_payload, self.payload)
                #history = Histories.add(self.request.dbsession, **history_payload)
            else:
                print('\tcreation: error')
                self.request.response.status = 500
        return resp

    def __put(self):
        resp = {}
        print('\nput:')
        if self.validate(selective=True):
            id = self.request.matchdict['id'].replace('-','')
            thing = self.cls.update_by_id(self.request.dbsession, id, **self.payload)
            if thing:
                print('\tupdate: successful')
                resp = thing.to_dict()
            else:
                print('\tupdate: error ( not found )')
                self.request.response.status = 404
        return resp

    def __delete(self):
        resp = {}
        print('\ndelete:')
        _id = self.request.matchdict['id']
        thing = self.cls.delete_by_id(
            self.request.dbsession,
            _id,
        )
        if thing:
            print('removal: succesful')
            resp = thing.to_dict()
        else:
            print('removal: error ( not found )')
            self.request.response.status = 404
        return resp

    #[ GET ]
    def _get(self):
        resp = {}
        if self.auth():
            resp = self.__get()
        return resp

    #[ GET COLLECTION ]
    def _get_collection(self):
        resp = {}
        if self.auth():
            if 'token' in self.request.GET:
                del self.request.GET['token']
            if len(self.request.GET) != 0 and len(self.params) == 0:
                resp = {'error': 'invalid param for get by query.'}
                self.request.response.status = 400 
            elif len(self.params) == 0:
                resp = self.__get_collection()
            else:
                resp = self.__get_collection_by()
        return resp

    #[ POST ]
    def _post(self):
        resp = {}
        if not 'id' in self.request.matchdict:
            if self.auth():
                resp = self.__post()
        else:
            self.request.response.status = 501
        return resp

    #[ PUT ]
    def _put(self):
        resp = {}
        if self.auth():
            resp = self.__put()
        return resp

    #[ DELETE ]
    def _delete(self):
        resp = {}
        if self.auth():
            resp = self.__delete()
        return resp
       
    
