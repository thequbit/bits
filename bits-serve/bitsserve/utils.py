import time
import json

import markdown

from pyramid.response import Response

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
    Tasks,
    TaskComments,
    Lists,
    RequirementTypes,
    Requirements,
    RequirementComments,
    Actions,
)

def make_response(resp_dict):

    print "[DEBUG]"
    print resp_dict
    print '\n'

    resp = Response(json.dumps(resp_dict), content_type='application/json', charset='utf8')
    resp.headerlist.append(('Access-Control-Allow-Origin', '*'))

    return resp

def do_login(email, password):

    _user, token = LoginTokens.do_login(
        session = DBSession,
        email = email,
        password = password,
    )
    
    user = None
    user_type = None
    if _user != None:
        user_type = UserTypes.user_type_from_id(
            session = DBSession,
            user_type_id = _user.user_type_id,
        )
        
        user = {
            'first': _user.first,
            'last': _user.last,
            'email': _user.email,
            'user_type': user_type.name,
            'user_type_description': user_type.description,
        }
        
    return user, token

def check_auth(request):

    try:
        token = request.cookies['token']
        if token == None or token == '':
            raise Exception('invalid token format')
    except:
        pass
        
    try:
        token = request.GET['token']
        if token == None or token == '':
            raise Exception('invalid token format')
    except:
        pass
        
    if token == None or token == '':
        raise Exception('Invalid Token')
        
    user = LoginTokens.check_authentication(
        session = DBSession,
        token = token,
    )
    
    if user == None:
        raise Exception('Invalid token')
    
    return user, token

def create_action(user_id, action_type, subject, project_id=None, \
        ticket_id=None, requirement_id=None, task_id=None, \
        list_id=None):

    action = Actions.add_action(
        session = DBSession,
        organization_id = 1,
        user_id = user_id,
        action_type = action_type,
        subject = subject,
        project_id = project_id,
        ticket_id = ticket_id,
        requirement_id = requirement_id,
        task_id = task_id,
        list_id = list_id,
    )

    return action


def get_actions(user, limit):

    _actions = Actions.get_user_action_list( #get_latest_actions_by_org_id(
        session = DBSession,
        user_id = user.id,
        #organization_id = 1,
        limit = 25,
    )

    actions = []
    for a_id, a_type, a_subject, a_created, u_id, u_first, u_last, u_email, \
            p_id, p_name, upa_id, t_id, t_title, task_id, task_title \
            in _actions:
        actions.append({
            'id': a_id,
            'action': a_type,
            'subject': a_subject,
            'created': a_created,
            'owner': '{0} {1}'.format(u_first, u_last),
            'project_id': p_id,
            'project_name': p_name,
            'ticket_id': t_id,
            'ticket_title': t_title,
            'task_id': task_id,
            'task_title': task_title,
        })

    return actions


def create_new_project(user_id, name, description):

    project = Projects.add_project(
        session = DBSession,
        author_id = user_id,
        organization_id = 1,
        name = name,
        description = description,
    )

    assignment = UserProjectAssignments.assign_user_to_project(
        session = DBSession,
        user_id = user_id,
        project_id = project.id,
    )
    
    action = create_action(
        user_id = user.id,
        action_type = "created",
        subject = "project",
        project_id = project.id,
    )

    return project


def get_user_projects(user):


    _projects = Projects.get_projects_from_user_id(
        session = DBSession,
        user_id = user.id,
    )

    projects = []
    for upa_id, upa_disabled, p_id, p_name, p_desc, p_created, \
            p_disabled, o_first, o_last, o_email, r_count, t_count \
            in _projects:
        if upa_disabled == False and p_disabled == False:
            projects.append({
                'id': p_id,
                'name': p_name,
                'description': p_desc,
                'created': p_created.strftime("%b %d, %Y"),
                'owner': '{0} {1}'.format(o_first, o_last),
                'owner_email': o_email,
                'requirement_count': r_count,
                'ticket_count': t_count,
                'note_count': 0,
            })

    return projects



def get_project(user, project_id):

    _project = Projects.get_from_id(
        session = DBSession,
        project_id = project_id,
    )

    if _project == None:
        raise Exception('invalid project')

    valid = UserProjectAssignments.check_project_assignment(
        session = DBSession,
        user_id = user.id,
        project_id = project_id,
    )
    if valid == False:
        raise Exception('unauthorized project')

    p_id, p_name, p_desc, p_created, p_disabled, o_id, o_first, o_last, \
            o_email, r_count, t_count  = _project
    project = {
        'id': p_id,
        'name': p_name,
        'description': p_desc,
        'created': p_created.strftime("%b %d, %Y"),
        'disabled': p_disabled,
        'owner_id': o_id,
        'owner': '{0} {1}'.format(o_first, o_last),
        'owner_email': o_email,
        'requirement_count': r_count,
        'ticket_count': t_count,
        'note_count': 0,
    }

    return project

def _check_ticket_auth(user_id, ticket_id):

    _ticket = Tickets.get_ticket_by_id(
        session = DBSession,
        ticket_id = ticket_id
    )

    if _ticket == None:
        raise Exception('no such ticket')

    # unpack tuple to get project_id
    t_id, t_number, t_title, t_contents, t_closed, t_closed_dt, \
        t_created, o_first, o_last, o_email, p_id, p_name, p_desc, \
        p_created, tt_name, tt_desc, tt_color = _ticket

    valid = UserProjectAssignments.check_project_assignment(
        session = DBSession,
        user_id = user_id,
        project_id = p_id,
    )

    if valid == False:
        raise Exception('invalid credentials')
        
    return _ticket

def create_new_ticket(user_id, project_id, ticket_type_id, title, contents):

    valid = UserProjectAssignments.check_project_assignment(
        session = DBSession,
        user_id = user_id,
        project_id = project_id,
    )

    if valid == False:
        raise Exception('invalid credentials')

    _last_ticket_number = Tickets.get_last_ticket_number(
        session = DBSession,
        project_id = project_id,
    )

    ticket_number = 1;
    if _last_ticket_number != None:
        last_ticket_number, = _last_ticket_number
        ticket_number = int(last_ticket_number) + 1;

    ticket = Tickets.add_ticket(
        session = DBSession,
        author_id = user_id,
        project_id = project_id,
        ticket_type_id = ticket_type_id,
        number = ticket_number,
        title = title,
        contents = contents,
        #ticket_priority_id = 1, #ticket_priority_id,
    )
    
    # register an action on creation
    action = create_action(
        user_id = user.id,
        action_type = 'created',
        subject = 'ticket',
        project_id = project_id,
        ticket_id = ticket.id,
    )
    
    return ticket

def get_tickets(project_id, closed=False):

    _tickets = Tickets.get_tickets_by_project_id(
        session = DBSession,
        project_id = project_id,
        closed = closed,
    )

    tickets = []
    for t_id, t_number, t_title, t_contents, t_closed, t_closed_dt, \
            t_created, o_first, o_last, o_email, p_id, p_name, p_desc, \
            p_created, tt_name, tt_desc, tt_color in _tickets:
            
        closed_datetime = None
        if t_closed_dt != None:
            closed_datetime = t_closed_dt.strftime("%b %d, %Y")
            
        tickets.append({
            'id': t_id,
            'created': t_created.strftime("%b %d, %Y"),
            'owner': '{0} {1}'.format(o_first, o_last),
            'owner_email': o_email,
            'type': tt_name,
            'type_description': tt_desc,
            'type_color': tt_color,
            'number': t_number,
            'title': t_title,
            'contents': markdown.markdown(t_contents),
            'closed': t_closed,
            'closed_datetime': closed_datetime,
        })

    return tickets

def get_ticket(user_id, ticket_id):

    _ticket = _check_ticket_auth(user_id, ticket_id)

    t_id, t_number, t_title, t_contents, t_closed, t_closed_dt, t_created, \
        o_first, o_last, o_email, p_id, p_name, p_desc, p_created, tt_name, \
        tt_desc, tt_color = _ticket
        
    ticket = None
    if True:
    
        closed_datetime = None
        if t_closed_dt != None:
            closed_datetime = t_closed_dt.strftime("%b %d, %Y")
    
        ticket = {
            'id': t_id,
            'project_id': p_id,
            'created': t_created.strftime("%b %d, %Y"),
            'owner': '{0} {1}'.format(o_first, o_last),
            'owner_email': o_email,
            'type': tt_name,
            'type_description': tt_desc,
            'type_color': tt_color,
            'number': t_number,
            'title': t_title,
            'contents': markdown.markdown(t_contents),
            'closed': t_closed,
            'closed_datetime': closed_datetime,
        }
 
    return ticket

def create_new_ticket_comment(user_id, ticket_id, contents):

    _ticket = _check_ticket_auth(user_id, ticket_id)

    ticket_comment = TicketComments.add_ticket_comment(
        session = DBSession,
        author_id = user_id,
        ticket_id = ticket_id,
        contents = contents,
    )
    
    action = create_action(
        user_id = user.id,
        action_type = "created",
        subject = "ticket_comment",
        project_id = ticket['project_id'],
        ticket_id = ticket_id,
    )
    
    return ticket_comment

def get_ticket_comments(user_id, ticket_id):

    _ticket = _check_ticket_auth(user_id, ticket_id)

    _comments = TicketComments.get_ticket_comments_by_ticket_id(
        session = DBSession,
        ticket_id = ticket_id,
    )

    if _comments == None:
        raise Exception('invalid ticket/comments')

    comments = []
    for tc_id, tc_contents, tc_flagged, tc_flagged_dt, tc_updated_dt, \
            tc_created, o_id, o_first, o_last, o_email in _comments:
        flagged_datetime = None
        if tc_flagged_dt != None:
            flagged_datetime = tc_flagged_dt.strftime("%b %d, %Y")
        updated_datetime = None
        if tc_updated_dt != None:
            updated_datetime = tc_updated_dt.strftime("%b %d, %Y")
        comments.append({
            'id': tc_id,
            'contents': markdown.markdown(tc_contents),
            'flagged': tc_flagged,
            'flagged_datetime': flagged_datetime,
            'updated_datetime': updated_datetime,
            'created': tc_created.strftime("%b %d, %Y"),
            'owner_id': o_id,
            'owner': '{0} {1}'.format(o_first, o_last),
            'owner_email': o_email,
         })
    return comments

def create_new_task():

    task = Tasks.add_task(
        session = DBSession,
        author_id = user.id,
        project_id = project_id,
        title = title,
        contents = contents,
        assigned = assigned,
        due = None, #due,
    )

    return task

def get_tasks(project_id):

    _tasks = Tasks.get_tasks_by_project_id(
        session = DBSession,
        project_id = project_id,
    )

    tasks = []
    for t_id, t_title, t_contents, t_due, t_completed, t_completed_dt, \
            t_created, o_id, o_first, o_last, o_email, p_id, p_name \
            in _tasks:
        tasks.append({
            'id': t_id,
            'title': t_title,
            'contents': t_contents,
            'due': t_due,
            'completed': t_completed,
            'completed_datetime': t_completed_dt,
            'created': t_created.strftime("%b %d, %Y"),
            'owner_id': o_id,
            'owner': '{0} {1}'.format(o_first, o_last),
            'owner_email': o_email,
            'project_id': p_id,
            'project_name': p_name,
        })

    return tasks

def get_task(task_id):

    _task = Tasks.get_by_id(
        session = DBSession,
        task_id = task_id,
    )

    t_id, t_title, t_contents, t_due, t_completed, t_completed_dt, \
        t_created, o_id, o_first, o_last, o_email, p_id, p_name = _task
    task = {
        'id': t_id,
        'title': t_title,
        'contents': t_contents,
        'due': t_due,
        'completed': t_completed,
        'completed_datetime': t_completed_dt,
        'created': t_created.strftime("%b %d, %Y"),
        'owner_id': o_id,
        'owner': '{0} {1}'.format(o_first, o_last),
        'owner_email': o_email,
        'project_id': p_id,
        'project_name': p_name,
    }

    return task

def get_task_comments(task_id):

    return []

def get_lists(project_id):

    _lists = Lists.get_lists_by_project_id(
        session = DBSession,
        project_id = project_id,
    )

    lists = []
    for l_id, l_name, l_disabled, l_disabled_dt, o_id, o_first, o_last, \
            o_email, p_id, p_name in _lists:
        lists.append({
            'id': l_id,
            'name': l_name,
            'disabled': l_disabled,
            'disabled_datetime': l_disabled_dt,
            'owner_id': o_id,
            'owner': '{0} {1}'.format(o_first, o_last),
            'project_id': p_id,
            'project_name': p_name,
        })

    return lists

def get_list(list_id):

    return {}

def get_list_comments(list_id):

    return []
