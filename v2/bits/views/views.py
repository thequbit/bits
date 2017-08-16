
from pyramid.response import Response
from pyramid.view import (
    view_defaults,
    view_config,
    notfound_view_config,
)

from ..utils import (
    validate_uuid4,
    BaseRequest,
)

from ..models import (
    Users,
)

def _logout(request):
    token = None
    user = None
    if 'token' in request.session:
        token = request.session['token']
        request.session.__delitem__('token')
    elif 'token' in request.GET:
        token = request.GET['token']
    if token:
        user = Users.invalidate_token(request.dbsession, token)
        if user:
            print('\tUser {0} invalidated successfully.'.format(user.email))
    return user

@view_config(route_name='/', renderer='../templates/site.jinja2')
def view_index(request):
    token = None
    user = None
    if 'token' in request.session:
        token = request.session['token']
    elif 'token' in request.GET:
        token = request.GET['token']
    if token:
        user = Users.get_by_token(request.dbsession, token)
        if user:
            return {}
    return Response(status_int=302, location="/login")

@view_config(route_name='/login', renderer='../templates/login.jinja2')
def view_login(request):
    user = _logout(request);
    return {}    

@view_config(route_name='/logout')
def view_logout(request):
    user = _logout(request);
    return Response(status_int=302, location="/login")

    