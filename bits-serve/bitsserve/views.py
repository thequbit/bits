import json
import datetime
import time

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    UserTypes,
    Users,
    Organizations,
    UserOrganizationAssignments,
    Projects,
    UserProjectAssignments,
    TicketTypes,
    TicketPriorities,
    Tickets,
    TicketContents,
    TicketComments,
    RequirementTypes,
    Requirements,
    RequirementContents,
    RequirementComments,
)

def make_response(resp_dict):

    print "[DEBUG]"
    print resp_dict
    print '\n'
    
    resp = Response(json.dumps(resp_dict), content_type='application/json', charset='utf8')
    resp.headerlist.append(('Access-Control-Allow-Origin', '*'))
    
    return resp

def check_auth(token):
    
    user = Users.check_authentication(
        session = DBSession,
        token = token,
    )
    return user



@view_config(route_name='authenticate.json')
def authenticate(request):

    """ End-point to authenticate user, and return a login token
    """

    result = {}
    result['success'] = False
    try:
        try:
            email = request.GET['email']
            password = request.GET['password']
        except:
            result['error_text'] = 'Missing Field'
            result['error_code'] = 1
            raise Exception('error')

        token = Users.authenticate_user(
            session = DBSession,
            email = email,
            password = password,
        )

        result['token'] = token
        if token == None:
            result['error_text'] = 'Invalid Credentials'
            result['error_code'] = 2
            raise Exception('error')

        result['success'] = True

    except:
        pass

    return make_response(result)

@view_config(route_name='get_projects.json')
def get_projects(request):

    """ End-point to get the list of projects the user has access to
    """

    result = {}
    result['success'] = False
    if True:
    #try:
        try:
            user = check_auth(request.GET['token'])
            if user == None:
                raise Exception('invalid or missing token')
        except:
            result['error_text'] = "Invalid or missing token"
            raise Exception('error')
        
        projects = UserProjectAssignments.get_users_projects(
            session = DBSession,
            user_id = user.id,
        )

        ret_projects = []
        for assignment_id, assignment_disabled, project_name,\
                project_description, project_creation_datetime, \
                project_disabled, user_first, user_last, user_email, \
                in projects:
            ret_projects.append({
                'assignment_id': assignment_id,
                'assignment_disabled': assignment_disabled,
                'project_name': project_name,
                'project_description': project_description,
                'project_creation_datetime': str(project_creation_datetime),
                'project_disabled': project_disabled,
                'author_first': user_first,
                'author_last': user_last,
                'author_email': user_email, 
            })

        result['projects'] = ret_projects

        result['success'] = True
        
    #except:
    #    pass

    return make_response(result)

@view_config(route_name='get_organizations.json')
def get_organizations(request):
    
    """ Get all of the organizations that the user has access to
    """

    result = {}
    result['success'] = False
    if True:
    try:
        try:
            user = check_auth(request.GET['token'])
            if user == None:
                raise Exception('invalid or missing token')
        except:
            result['error_text'] = "Invalid or missing token"
            raise Exception('error')

        projects = UserOrganizationAssignments.get_users_organizations(
            session = DBSession,
            user_id = user.id,
        )

        ret_organizations = []
        for assignment_id, assignment_disabled, organization_name,\
                organization_description, organization_creation_datetime, \
                organization_disabled, user_first, user_last, user_email, \
                in projects:
            ret_organizations.append({
                'assignment_id': assignment_id,
                'assignment_disabled': assignment_disabled,
                'organization_name': organization_name,
                'organization_description': organization_description,
                'organization_creation_datetime': str(organization_creation_datetime),
                'organization_disabled': organization_disabled,
                'author_first': user_first,
                'author_last': user_last,
                'author_email': user_email,
            })

        result['organizations'] = ret_organizations

        result['success'] = True

    except:
        pass

    return make_response(result)

