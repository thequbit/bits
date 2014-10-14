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

@view_config(route_name='login', renderer='templates/login.mak')
def login(request):

    return {}

@view_config(route_name='index', renderer='templates/index.mak')
def index(request):

    token = None
    user = None
    #if True:
    try:
        token = request.GET['token']
        user = check_auth(token)
        if user == None:
            token = None
            raise Exception('invalid token')
    except:
        pass

    projects = []
    #if True:
    try:
        raw_projects = Projects.get_projects_from_user_id(
            session = DBSession,
            user_id = user.id,
        )
        for upa_id, upa_disabled, p_id, p_name, p_desc, p_created, \
                p_disabled, o_first, o_last, o_email in raw_projects:
            if upa_disabled == False and p_disabled == False:
                projects.append({
                    'id': p_id,
                    'name': p_name,
                    'description': p_desc,
                    'created': p_created.strftime("%b %d, %Y"),
                    'owner': '{0} {1}'.format(o_first, o_last),
                    'owner_email': o_email,
                })
        #print projects
    except:
        pass

    return {'token': token, 'user': user, 'projects': projects}

@view_config(route_name='project', renderer='templates/project.mak')
def project(request):

    result = {}
    #if True:
    try:
        token = request.GET['token']
        user = check_auth(token)
        if user == None:
            result['user'] = None
            result['token'] = None
            raise Exception('invalid token')

        result['user'] = user
        result['token'] = token

        project_id = request.GET['project_id']
            
        _project = Projects.get_from_id(
            session = DBSession,
            project_id = project_id,
        )

        if _project == None:
            raise Exception('invalid project')

        p_id, p_name, p_desc, p_created, p_disabled, o_first, o_last, \
                o_email = _project
        project = {
            'id': p_id,
            'name': p_name,
            'description': p_desc,
            'created': p_created.strftime("%b %d, %Y"),
            'disabled': p_disabled,
            'owner': '{0} {1}'.format(o_first, o_last),
            'owner_email': o_email,
        }

        valid = UserProjectAssignments.check_project_assignment(
            session = DBSession,
            user_id = user.id,
            project_id = project_id,
        )
        if valid == False:
            raise Exception('unauthorized project')

        result['project'] = project

        _tickets = Tickets.get_tickets_by_project_id(
            session = DBSession,
            project_id = project_id,
        )

        tickets = []
        for t_id, t_closed, t_closed_dt, t_created, o_first, o_last, \
                o_email, p_name, p_desc, p_created, tt_name, tt_desc, \
                tt_color, tc_title, tc_contents, tc_version, tc_created \
                in _tickets:
            if t_closed == False:
                tickets.append({
                    'id': t_id,
                    'created': t_created.strftime("%b %d, %Y"),
                    'owner': '{0} {1}'.format(o_first, o_last),
                    'owner_email': o_email,
                    'type': tt_name,
                    'type_description': tt_desc,
                    'type_color': tt_color,
                    'title': tc_title,
                    'contents': tc_contents,
                })

        result['tickets'] = tickets            

    except:
        pass

    return result


@view_config(route_name='tickets', renderer='templates/tickets.mak')
def tickets(request):

    tickets = None
    if True:
    #try:

        project_id = request.GET['project_id']
        
        tickets = Tickets.get_tickets_by_project_id(
            session = DBSession,
            project_id = project_id
        )

    #except:
    #    pass

    return {'tickets': tickets,'project_id':project_id}

@view_config(route_name='ticket', renderer='templates/ticket.mak')
def ticket(request):

    result = {}
    #if True:
    try:

        token = request.GET['token']
        user = check_auth(token)
        if user == None:
            result['user'] = None
            result['token'] = None
            raise Exception('invalid token')

        result['user'] = user
        result['token'] = token

        ticket_id = request.GET['ticket_id']
        project_id = request.GET['project_id']

        _ticket = Tickets.get_ticket_by_ticket_id(
            session = DBSession,
            ticket_id = ticket_id
        )

        if _ticket == None:
            raise Exception('no such ticket')
        
        t_id, t_closed, t_closed_dt, t_created, o_first, o_last, \
            o_email, p_name, p_desc, p_created, tt_name, tt_desc, \
            tt_color, tc_title, tc_contents, tc_version, tc_created  = _ticket
        ticket = None
        if t_closed == False:
            ticket = {
                'id': t_id,
                'created': t_created.strftime("%b %d, %Y"),
                'owner': '{0} {1}'.format(o_first, o_last),
                'owner_email': o_email,
                'type': tt_name,
                'type_description': tt_desc,
                'type_color': tt_color,
                'title': tc_title,
                'contents': tc_contents,
            }

        comments = TicketComments.get_ticket_comments_by_ticket_id(
            session = DBSession,
            ticket_id = _ticket.id,
        )

        if comments == None:
            raise Exception('invalid comments')

        _project = Projects.get_from_id(
            session = DBSession,
            project_id = project_id,
        )

        if _project == None:
            project = None
            raise Exception('invalid project')
        project = None
        if _project.disabled == False:
            project = {
                'id': _project.id,
                'name': _project.name,
                'description': _project.description,
                'created': _project.creation_datetime.strftime("%b %d, %Y"),
            }

        valid = UserProjectAssignments.check_project_assignment(
            session = DBSession,
            user_id = user.id,
            project_id = project_id,
        )

        if valid == False:
            raise Exception('unauthorized project')

        result['ticket'] = ticket
        result['comments'] = comments
        result['project'] = project

    except:
        pass

    return result

@view_config(route_name='newticket', renderer='templates/newticket.mak')
def new_ticket(request):

    result = {}
    if True:
    #try:
        token = request.GET['token']
        user = check_auth(token)
        if user == None:
            result['user'] = None
            result['token'] = None
            raise Exception('invalid token')

        result['user'] = user
        result['token'] = token

        project_id = request.GET['project_id']

        _project = Projects.get_from_id(
            session = DBSession,
            project_id = project_id,
        )

        if _project == None:
            project = None
            raise Exception('invalid project')
        project = None
        if _project.disabled == False:
            project = {
                'id': _project.id,
                'name': _project.name,
                'description': _project.description,
                'created': _project.creation_datetime.strftime("%b %d, %Y"),
            }

        valid = UserProjectAssignments.check_project_assignment(
            session = DBSession,
            user_id = user.id,
            project_id = project_id,
        )

        if valid == False:
            raise Exception('unauthorized project')
    
        result['project'] = project
    
    #except:
    #    pass

    return result

@view_config(route_name='authenticate.json')
def authenticate(request):

    """ End-point to authenticate user, and return a login token
    """

    result = {}
    result['success'] = False
    if True:
    #try:
        try:
            email = request.GET['email']
            password = request.GET['password']
        except:
            result['error_text'] = 'Missing Field'
            result['error_code'] = 1
            raise Exception('error')

        token, user = Users.authenticate_user(
            session = DBSession,
            email = email,
            password = password,
        )

        if token == None:
            result['error_text'] = 'Invalid Credentials'
            result['error_code'] = 2
            raise Exception('error')

        user_type = UserTypes.user_type_from_id(
            session = DBSession,
            user_type_id = user.user_type_id,
        )

        result['token'] = token
        result['user'] = {
            'first': user.first,
            'last': user.last,
            'email': user.email,
            'user_type': user_type.name,
            'user_type_description': user_type.description,
        }

        result['success'] = True

    #except:
    #    pass

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
        
        projects = Projects.get_projects_from_user_id(
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
        for assignment_id, assignment_disabled, organization_id, \
                organization_name, organization_description, \
                organization_creation_datetime, organization_disabled, \
                user_first, user_last, user_email in projects:
            ret_organizations.append({
                'assignment_id': assignment_id,
                'assignment_disabled': assignment_disabled,
                'organization_id': organization_id,
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

@view_config(route_name='create_ticket.json')
def create_ticket(request):

    """ Get all of the organizations that the user has access to
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

        try:
            author_id = request.POST['author_id']
            project_id = request.POST['project_id']
            ticket_type_id = request.POST['ticket_type_id']
            #ticket_priority_id = request.POST['ticket_priority_id']
            title = request.POST['title']
            contents = request.POST['contents']
        except:
            result['error_text'] = "Missing fields."
            raise Exception('error')

        ticket = Tickets.add_ticket(
            session = DBSession,
            author_id = author_id,
            project_id = project_id,
            ticket_type_id = ticket_type_id,
            #ticket_priority_id = 1, #ticket_priority_id,
        )
        ticket_contents = TicketContents.add_ticket_content(
            session = DBSession,
            author_id = author_id,
            ticket_id = ticket.id,
            title = title,
            contents = contents,
        )

        result['ticket_id'] = ticket.id

        result['success'] = True

    #except:
    #    pass

    return make_response(result)

@view_config(route_name='create_comment.json')
def create_comment(request):

    """ Get all of the organizations that the user has access to
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

        try:
            author_id = request.POST['author_id']
            project_id = request.POST['ticket_id']
            contents = request.POST['contents']
        except:
            result['error_text'] = "Missing fields."
            raise Exception('error')

        ticket_comment = TicketComments.add_ticket_comment(
            author_id = author_id,
            ticket_id = ticket_id,
            contents = contents,
        )

        result['ticket_comment_id'] = ticket_comment.id

        result['success'] = True

    #except:
    #    pass

    return make_response(result)

