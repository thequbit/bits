
from pyramid.response import Response
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import transaction

from ..utils import (
    validate_uuid4,
    authenticate,
    BaseRequest,
)

from ..models import (
    Users,
)

import json
import datetime

@view_defaults(route_name='/api/v1/users', renderer='json')
class UsersAPI(BaseRequest):

    cls = Users

    req = (
        'first',
        'last',
        'email',
        'password',
        'user_type',
        'enabled',
    )

    def __init__(self, request):
        super(UsersAPI, self).__init__(request)

    #[ GET ]
    @view_config(request_method='GET')
    def get(self):
        resp = []
        with transaction.manager:
            if self.auth():
                print("\nuser type: {0}\n".format(self.user.user_type))
                if self.user.user_type == 'administrator' or self.user.user_type == 'system':
                    _users = Users.get_paged(
                        self.request.dbsession,
                        self.start,
                        self.count
                    )
                    if _users:
                        resp = [u.to_dict() for u in _users]
                    else:
                        self.request.response.status = 403
                elif 'organization_id' in self.request.GET and validate_uuid4(self.request.GET['organization_id']):
                    organization_id = self.request.GET['organization_id']
                    if self.user.organization_id == organization_id:
                        users = Users.get_all_by_organization_id(self.request.dbsession, organization_id)
                        if users:
                            resp = [u.to_dict(with_auth=False) for u in users]
                    else:
                        self.request.response.status = 403
        return resp

    #[ POST ]
    @view_config(request_method='POST')
    def post(self):
        resp = {}
        with transaction.manager:
            if self.auth():
                if self.user.user_type == 'administrator' or self.user.user_type == 'system':
                    if self.validate():
                        user = Users.create_new_user(
                            self.request.dbsession,
                            first=self.payload['first'],
                            last=self.payload['last'],
                            phone=self.payload['phone'],
                            email=self.payload['email'],
                            password=self.payload['password'],
                            user_type=self.payload['user_type'],
                            enabled=self.payload['enabled'],
                        )
                        if user:
                            resp = user.to_dict(with_auth=True)
                            self.request.response.status = 201
                        else:
                            self.request.response.status = 500
                else:
                    self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/v1/users/{id}/_change_password', renderer='json')
class UserChangePasswordAPI(BaseRequest):

    cls = Users

    def __init__(self, request):
        super(UserChangePasswordAPI, self).__init__(request)

    #[ PUT ]
    @view_config(request_method='PUT')
    def put(self):
        resp = {}
        with transaction.manager:
            if self.auth():
                if 'new_password' in self.payload:
                    new_pass_hash = Users.build_pass_hash(self.user, self.payload['new_password'])
                    user = Users.update_by_id(
                        self.request.dbsession,
                        self.user.id,
                        pass_hash = new_pass_hash,
                        must_change_password=0,
                    )
                    if user:
                        resp = {'success': True}
                    else:
                        # uh ...
                        pass                   
        return resp


@view_defaults(route_name='/api/v1/users/{id}/_status', renderer='json')
class UserStatusAPI(BaseRequest):

    cls = Users

    def __init__(self, request):
        super(UserStatusAPI, self).__init__(request)

    #[ PUT ]
    @view_config(request_method='PUT')
    def put(self):
        resp = {}
        with transaction.manager:
            if self.auth():
                if 'enabled' in self.payload:
                    enabled = self.payload['enabled']
                    user_id = self.request.matchdict['id']
                    user = Users.update_by_id(
                        self.request.dbsession,
                        user_id,
                        enabled = enabled,
                    )
                    if user:
                        resp = {'success': True}
                    else:
                        self.request.response.status = 400
        return resp

@view_defaults(route_name='/api/v1/users/_login', renderer='json')
class UserLoginAPI(BaseRequest):

    cls = Users

    req = (
        'email',
        'password',
    )

    def __init__(self, request):
        super(UserLoginAPI, self).__init__(request)

    #[ GET ] - check if logged in
    @view_config(request_method='GET')
    def get(self):
        
        # todo: enable this
        #csrf_token = self.request.session.get_csrf_token()
        #resp = {'loggedin': False, 'csrf_token': csrf_token}
        resp = {'loggedin': False}
        if self.user:
            resp.update(
                loggedin=True,
                user=self.user.to_dict(with_auth=True)
            )
        return resp

    #[ POST ] - perform login
    @view_config(request_method='POST')
    def post(self):
        resp = {}
        with transaction.manager:
            if self.validate():
                email = self.payload['email']
                password = self.payload['password']
                self.user = Users.authenticate(
                    self.request.dbsession,
                    email,
                    password
                )
                if self.auth():
                    self.request.session['token'] = self.user.to_dict(with_auth=True)['token']
                    _user = self.user.to_dict(with_auth=True)
                    _user.update(token=self.user.token)
                    resp = _user
                else:
                    self.request.response.status = 401
        return resp


@view_defaults(route_name='/api/v1/users/_logout', renderer='json')
class UserLogoutAPI(BaseRequest):

    cls = Users

    def __init__(self, request):
        super(UserLogoutAPI, self).__init__(request)

    #[ POST ] - logs the user out
    @view_config(request_method='POST')
    def post(self):
        resp = {}
        if 'token' in self.request.session:
            token = self.request.session['token']
            self.request.session.__delitem__('token')
        elif 'token' in self.request.GET:
            token = self.request.GET['token']

        if token:
            with transaction.manager:
                user = Users.invalidate_token(
                    self.request.dbsession,
                    token,
                )
                if not user:
                    self.request.response.status = 403
        else:
            # nothing to do 
            pass

        return resp  

@view_defaults(route_name='/api/v1/users/_exists', renderer='json')
class UserExistsAPI(BaseRequest):

    cls = Users

    def __init__(self, request):
        super(UserExistsAPI, self).__init__(request)

    #[ GET ] - checks if email exists
    @view_config(request_method='GET')
    def post(self):
        resp = {'exists': False}
        with transaction.manager:
            if self.auth() and self.user.user_type == 'administrator':
                if 'email' in self.request.GET:
                    email = self.request.GET['email']
                    user = Users.get_by_email(self.request.dbsession, email)
                    if user:
                        resp = {'exists': True}
                else:
                    self.request.response.status = 400
        return resp  

@view_defaults(route_name='/api/v1/users/{id}', renderer='json')
class UserAPI(BaseRequest):

    cls = Users

    req = (
        'first',
        'last',
        'phone',
        'email',
        'user_type',
        'enabled',
    )

    def __init__(self, request):
        super(UserAPI, self).__init__(request)


    #[ GET ]
    @view_config(request_method='GET')
    def get(self):
        resp = {}
        if self.auth():
            resp = self._get()
        return resp

    #[ PUT ]
    @view_config(request_method='PUT')
    def put(self):
        resp = {}
        if self.auth():
            resp = self._put()
        return resp

    #[ DELETE ]
    @view_config(request_method='DELETE')
    def delete(self):
        resp = {}
        if self.auth():
            resp = self._delete()
        return resp
