import json
import datetime
import time

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

import markdown

from utils import (

    make_response,
    
    check_auth,
    do_login,

    create_action,
    get_actions,
    get_user_actions,
    
    create_new_project,
    get_user_projects,
    get_project,
    assign_user_to_project,
    get_users_assigned_to_project,
    
    create_new_ticket,
    get_tickets,
    get_ticket,
    get_ticket_comments,
    create_new_ticket_comment,
    
    get_tasks,
    get_task,
    get_task_comments,
    
    get_lists,
    get_list,
    get_list_comments,    
)

from .models import (
    DBSession,
    UserTypes,
    Users,
    LoginTokens,
    Organizations,
    UserOrganizationAssignments,
    Projects,
    UserProjectAssignments,
    TicketTypes,
    TicketPriorities,
    Tickets,
    TicketComments,
    RequirementTypes,
    Requirements,
    RequirementComments,
    Tasks,
    Actions,
)

@view_config(route_name='login', renderer='templates/login.mak')
def login(request):

    return {}

@view_config(route_name='logout', renderer='templates/logout.mak')
def logout(request):

    result = {'user': None}
    ###if True:
    try:

        user, token = check_auth(request)
        
        LoginTokens.logout(
            session = DBSession,
            token = token,
        )

    except:
        pass

    return result

@view_config(route_name='user', renderer='templates/user.mak')
def user(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        user_id = request.GET['user_id']

        actions, target_user = get_user_actions(
            user_id = user_id,
            limit = 50,
        )
        
        result['actions'] = actions
        result['target_user'] = target_user

    except:
        pass

    return result


@view_config(route_name='usersettings', renderer='templates/usersettings.mak')
def usersettings(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

    except:
        pass

    return result

@view_config(route_name='projectsettings', renderer='templates/projectsettings.mak')
def projectsettings(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        project_id = request.GET['project_id']
            
        result['project'] = get_project(user.id, project_id)

        assigned_users = get_users_assigned_to_project(user.id, project_id)
        
        result['assigned_users'] = assigned_users

        result['tasks'] = get_tasks(project_id)

        result['tickets'] = get_tickets(project_id)


    except:
        pass

    return result

@view_config(route_name='index', renderer='templates/index.mak')
def index(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        result['projects'] = get_user_projects(user)

        result['actions'] = get_actions(user.id, limit=25)


    except:
        pass

    return result #{'token': token, 'user': user, 'projects': projects}

@view_config(route_name='project', renderer='templates/project.mak')
def project(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        project_id = request.GET['project_id']
            
        result['project'] = get_project(user.id, project_id)

        result['tasks'] = get_tasks(project_id)

        result['tickets'] = get_tickets(project_id)


    except:
        pass

    return result

@view_config(route_name='tickets', renderer='templates/tickets.mak')
def tickets(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        project_id = int(request.GET['project_id'])

        closed = False
        try:
            closed = int(request.GET['closed']);
        except:
            pass

        result['closed'] = closed

        result['tickets'] = get_tickets(project_id, closed)

        result['project'] = get_project(user.id, project_id)

    except:
        pass

    return result 

@view_config(route_name='ticket', renderer='templates/ticket.mak')
def ticket(request):

    result = {'user': None}
    if True:
    #try:

        user, token = check_auth(request)
        result['user'] = user

        ticket_id = request.GET['ticket_id']
        #project_id = request.GET['project_id']

        ticket = get_ticket(
            user_id = user.id, 
            ticket_id = ticket_id,
        )
        
        result['ticket'] = ticket

        result['comments'] = get_ticket_comments(user.id, ticket['id'])

        result['tickets'] = get_tickets(ticket['project_id'])

        result['project'] = get_project(user.id, ticket['project_id'])

    #except:
    #    pass

    return result

@view_config(route_name='task', renderer='templates/task.mak')
def task(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        task_id = request.GET['task_id']
        #project_id = request.GET['project_id']

        task = get_task(task_id)
        result['task'] = task

        result['comments'] = get_task_comments(task['id'])

        result['tasks'] = get_tasks(task['project_id'])

        result['project'] = get_project(user.id, task['project_id'])


    except:
        pass

    return result


@view_config(route_name='newticket', renderer='templates/newticket.mak')
def new_ticket(request):

    result = {'user': None}
    #if True:
    try:
    
        user, token = check_auth(request)
        result['user'] = user

        project_id = request.GET['project_id']

        result['project'] = get_project(user.id, project_id)
   
        result['assigned_users'] = get_users_assigned_to_project(user.id, project_id)
   
        result['tickets'] = get_tickets(project_id)
 
    except:
        pass

    return result

@view_config(route_name='newtask', renderer='templates/newtask.mak')
def new_task(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        project_id = request.GET['project_id']

        result['project'] = get_project(user.id, project_id)

        result['tickets'] = get_tickets(project_id)

    except:
        pass

    return result

@view_config(route_name='newlist', renderer='templates/newlist.mak')
def new_list(request):

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)
        result['user'] = user

        project_id = request.GET['project_id']

        result['project'] = get_project(user.id, project_id)

        result['lists'] = get_lists(project_id)

    except:
        pass

    return result


@view_config(route_name='newproject', renderer='templates/newproject.mak')
def new_project(request):

    result = {'user': None}
    ##if True:
    try:

        user, token = check_auth(request)

        result['user'] = user

        result['projects'] = get_projects(user);

    except:
        pass

    return result
 

@view_config(route_name='authenticate.json')
def authenticate(request):

    """ End-point to authenticate user, and return a login token
    """

    result = {'user': None}
    result['success'] = False
    #if True:
    try:
        try:
            email = request.GET['email']
            password = request.GET['password']
        except:
            result['error_text'] = 'Missing Field'
            result['error_code'] = 1
            raise Exception('error')

        user, token = do_login(email, password)

        if user == None or token == None:
            result['error_text'] = 'Invalid Credentials'
            result['error_code'] = 2
            raise Exception('error')

        result['token'] = token
        result['user'] = user

        result['success'] = True

    except:
        pass

    return make_response(result)

@view_config(route_name='create_ticket.json')
def create_ticket(request):

    """ Create a new ticket
    """

    result = {'user': None}
    result['success'] = False

    if True:
    #try:

        user, token = check_auth(request)

        project_id = request.POST['project_id']
        title = request.POST['title']
        contents = request.POST['contents']
        assigned_id = request.POST['assigned_user_id']
        ticket_type_id = None #1 # request.POST['ticket_type_id']

        ticket = create_new_ticket(
            user_id = user.id,
            project_id = project_id,
            ticket_type_id = ticket_type_id,
            title = title,
            contents = contents,
            assigned_id = assigned_id,
        )

        result['ticket_id'] = ticket.id

        result['success'] = True

    #except:
    #    pass

    return make_response(result)

@view_config(route_name='close_ticket.json')
def close_ticket(request):

    """ Create a new ticket
    """

    result = {'user': None}
    result['success'] = False

    #if True:
    try:

        user, token = check_auth(request)

        ticket_id = request.POST['ticket_id']
        
        
        ticket = Tickets.close_ticket(
            session = DBSession,
            ticket_id = ticket_id,
        )

        result['ticket_id'] = ticket.id

        result['success'] = True

    except:
        pass

    return make_response(result)


@view_config(route_name='create_project.json')
def create_project(request):
    """ Create a new project
    """

    result = {'user': None}
    #if True:
    try:

        user, token = check_auth(request)

        name = request.POST['name']
        description = request.POST['description']

        project = create_new_project(
            user_id = user.id, 
            name = name,
            description = description,
        )
        
        result['project_id'] = project.id
        
        result['success'] = True

    except:
        pass

    return make_response(result)

@view_config(route_name='assign_user.json')
def assign_user(request):
    """ Assign a user to a project
    """

    result = {}
    #if True:
    try:

        user, token = check_auth(request)
        
        project_id = int(request.POST['project_id'])
        email = request.POST['email']

        target_user, assignment = assign_user_to_project(
            user_id = user.id,
            project_id = project_id,
            email = email,
        )
    
        if assignment != None:
            result['assignment_id'] = assignment.id
        else:
            result['assignment_id'] = -1;
            
        result['project_id'] =  project_id
        result['user_id'] = target_user.id
    
        
        result['success'] = True

    except:
        pass

    return make_response(result)



@view_config(route_name='create_ticket_comment.json')
def create_ticket_comment(request):
    """ Get all of the organizations that the user has access to
    """

    result = {'user': None}
    result['success'] = False

    if True:
    #try:

        user, token = check_auth(request)

        #author_id = request.POST['author_id']
        #project_id = request.POST['project_id']
        ticket_id = request.POST['ticket_id']
        contents = request.POST['contents']
        
        ticket = get_ticket(user.id, ticket_id)

        ticket_comment = create_new_ticket_comment(
            user.id,
            ticket_id = ticket_id,
            contents = contents,
        )

        result['ticket_comment_id'] = ticket_comment.id

        result['success'] = True

    #except:
    #    pass

    return make_response(result)

@view_config(route_name='create_task.json')
def create_task(request):
    """ Get all of the organizations that the user has access to
    """
    
    result = {'user': None}
    result['success'] = False

    #if True:
    try:

        user, token = check_auth(request)

        project_id = request.POST['project_id']
        title = request.POST['title']
        contents = request.POST['contents']
        assigned = request.POST['assigned']
        #due = request.POST['due']

        task = Tasks.add_task(
            session = DBSession,
            author_id = user.id,
            project_id = project_id,
            title = title,
            contents = contents,
            assigned = assigned,
            due = None, #due,
        )

        if task == None:
            result['error_code'] = 1
            raise Exception('invalid assigned')

        result['task_id'] = task.id

        action = Actions.add_action(
            session = DBSession,
            organization_id = 1,
            user_id = user.id,
            action_type = "created",
            subject = "task",
            project_id = task.id,
            ticket_id = None,
            requirement_id = None,
            task_id = task.id,
            list_id = None,
        )

        result['success'] = True

    except:
        pass

    return make_response(result)

