
from config import config

import time
import json

import markdown

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    ActionTypes,
    ActionSubjects,
    Actions,
)

html = ''
try:
    with open('email.html') as f:
        html = f.read()
except:
    html = "Hello.  You are recieving this email because an item within a " \
           "project you are assigned to changed.  You can see more here: " \
           "http://bits.timduffy.me"

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

    if subject != 'project' and project_id != None:
        upas = UserProjectAssignments.get_users_assigned_to_project(
            session = DBSession,
            project_id = project_id,
        )
        for upa_id, u_id, u_first, u_last, u_email in upas:
            print 
            if u_id != user_id:
                send_notification(
                    user_id = u_id,
                    action_id = action.id,
                )

    return action

def get_actions(user_id, limit):

    _actions = Actions.get_user_action_list( #get_latest_actions_by_org_id(
        session = DBSession,
        user_id = user_id,
        #organization_id = 1,
        limit = limit,
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
            'owner_id': u_id,
            'project_id': p_id,
            'project_name': p_name,
            'ticket_id': t_id,
            'ticket_title': t_title,
            'task_id': task_id,
            'task_title': task_title,
        })

    return actions

def get_user_actions(user_id, limit):

    _actions = Actions.get_user_actions(
        session = DBSession,
        user_id = user_id,
        limit = limit,
    )
    
    target_user = Users.get_by_id(
        session = DBSession,
        user_id = user_id,
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

    return actions, target_user

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
        user_id = user_id,
        action_type = "created",
        subject = "project",
        project_id = project.id,
    )

    return project

def assign_user_to_project(user_id, project_id, email):

    target_user = Users.get_by_email(
        session = DBSession,
        email = email
    )
    
    if target_user == None:
        raise Excetion('Invalid User')

    valid = UserProjectAssignments.check_project_assignment(
        session = DBSession,
        user_id = user_id,
        project_id = project_id,
    )

    if valid == False:
        raise Exception('Unauthorized Project')

    _assignment = UserProjectAssignments.get_user_project_assignment(
        session = DBSession,
        user_id = target_user.id,
        project_id = project_id,
    )
    
    # make sure the assignment hasn't alreayd been made
    if _assignment == None:
        assignment = UserProjectAssignments.assign_user_to_project(
            session = DBSession,
            user_id = target_user.id,
            project_id = project_id,
        )
    else:
        assignment = _assignment
    
    return target_user, assignment
    
def get_users_assigned_to_project(user_id, project_id):

    valid = UserProjectAssignments.check_project_assignment(
        session = DBSession,
        user_id = user_id,
        project_id = project_id,
    )

    if valid == False:
        raise Exception('Unauthorized Project')

    _users = UserProjectAssignments.get_users_assigned_to_project(
        session = DBSession,
        project_id = project_id,
    )
    
    users = []
    for a_id, u_id, u_first, u_last, u_email in _users:
        users.append({
            'assignment_id': a_id,
            'user_id': u_id,
            'user': '{0} {1}'.format(u_first, u_last),
            'email': u_email,
        })
    
    return users
    
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



def get_project(user_id, project_id):

    _project = Projects.get_from_id(
        session = DBSession,
        project_id = project_id,
    )

    if _project == None:
        raise Exception('invalid project')

    valid = UserProjectAssignments.check_project_assignment(
        session = DBSession,
        user_id = user_id,
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
    t_id, t_number, t_title, t_contents, t_a_id, t_closed, t_closed_dt, \
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

def create_new_ticket(user_id, project_id, ticket_type_id, title, contents, \
        assigned_id):

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
        assigned_id = assigned_id,
    )
    
    # register an action on creation
    action = create_action(
        user_id = user_id,
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
    for t_id, t_number, t_title, t_contents, t_a_id, t_closed, t_closed_dt, \
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

    t_id, t_number, t_title, t_contents, t_a_id, t_closed, t_closed_dt, \
        t_created, o_first, o_last, o_email, p_id, p_name, p_desc, p_created, \
        tt_name, tt_desc, tt_color = _ticket
        
    ticket = None
    if True:
    
        closed_datetime = None
        if t_closed_dt != None:
            closed_datetime = t_closed_dt.strftime("%b %d, %Y")

        assigned_user_name = ''
        if t_a_id != None:    
            assigned_user = Users.get_by_id(
                session = DBSession,
                user_id = t_a_id,
            )
            assgined_user_name =  '{0} {1}'.format(assigned_user.first, assigned_user.last),

        ticket = {
            'id': t_id,
            'project_id': p_id,
            'created': t_created.strftime("%b %d, %Y"),
            'owner': '{0} {1}'.format(o_first, o_last),
            'owner_email': o_email,
            'assigned_id': t_a_id,
            'assigned_user': assigned_user_name,
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
    
    # unpack tuple to get project_id
    t_id, t_number, t_title, t_contents, t_a_id, t_closed, t_closed_dt, \
        t_created, o_first, o_last, o_email, p_id, p_name, p_desc, \
        p_created, tt_name, tt_desc, tt_color = _ticket
    
    action = create_action(
        user_id = user_id,
        action_type = "created",
        subject = "ticket_comment",
        project_id = p_id,
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
    
def send_notification(user_id, action_id):

    target_user = Users.get_by_id(
        session = DBSession,
        user_id = user_id,
    )

    _action = Actions.get_action_by_id(
        session = DBSession,
        action_id = action_id,
    )

    a_id, a_type, a_subject, a_created, u_id, u_first, u_last, u_email, \
        p_id, p_name, upa_id, t_id, t_title, task_id, task_title = _action

    if a_type == 'created' and a_subject == 'project':
        action_text = " created a project "
    elif a_type == 'created' and a_subject == 'ticket':
        action_text = " created a ticket "
    elif a_type == 'created' and a_subject == 'ticket_comment':
        action_text = ' created a comment in ticket '

    html = """
    <html>
    <head>
        <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    </head>
    <body>
        <div style="margin-left: 20px; font-family: 'Lato', sans-serif !important; font-size: 110%;">
            <h4>bits</h4>
            <p>
               Hello.  You are recieving this email because an item within a project you are
               assigned to has changed.
            </p>
            <p>
                Project: <a style="color: #008CBA; text-decoration: none; line-height: inherit;" href="{0}project?project_id={1}">{2}</a>
            </p>
            <p>
                <div style="margin-left: 20px; padding: 10px; font-size: 90%; margin-top: 10px; max-width: 450px; box-shadow: 0px 0px 0px 1px #DDD, 0px 4px 8px rgba(221, 221, 221, 0.9);">
                    <div class="small-light-text">{3}</div>
                    <a style="color: #008CBA; text-decoration: none; line-height: inherit;" href="{0}user?user_id={4}">{5}</a>
                    {6} 
                    <a style="color: #008CBA; text-decoration: none; line-height: inherit;" href="{0}ticket?ticket_id={7}">{8}</a>.
                </div>
            </p>
            <br/>
        </div>
    </body>
    </html>
    """.format(
        config['root_domain'],
        p_id,
        p_name,
        a_created,
        u_id,
        '{0} {1}'.format(u_first, u_last),
        action_text,
        t_id,
        t_title,
    )

    success = False

    try:
    #if True:

        password =  config['notification_email_password']; #"h1chaos4ever"
        
        server = smtplib.SMTP()
        server.connect(config['notification_email_server'], config['notification_email_server_port'])
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(config['notification_email_address'], password)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Bits Notification"
        msg['From'] = config['notification_email_address']
        msg['To'] = target_user.email

        text = "Hello.  You are recieving this email because an item within a " \
               "project you are assigned to changed.  You can see more here: " \
               "{0}".format(config['root_domain'])

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(
            config['notification_email_address'],
            target_user.email,
            msg.as_string()
        )
        server.quit()
    
        success = True

    except:
        pass
    
    return success

def export_database(user_id):

    if user_id != 1:
        raise Exception("Invalid Credentails")
        
    _user_types = UserTypes.get_all_user_types(
        session = DBSession,
    )
    user_types = []
    for user_type in _user_types:
        user_types.append({
            'id': user_type.id,
            'name': user_type.name,
            'description': user_type.description,
        })
        
    _organizations = Organizations.get_all_organizations(
        session = DBSession,
    )
    organizations = []
    for organization in _organizations:
        organizations.append({
            'id': organization.id,
            'author_id': organization.author_id,
            'name': organization.name,
            'description': organization.description,
            'disabled': organization.disabled,
            'creation_datetime': str(organization.creation_datetime),
        })
        
    _users = Users.get_all_users(
        session = DBSession,
    )
    users = []
    for user in _users:
        users.append({
            'id': user.id,
            'user_type_id': user.user_type_id,
            'first': user.first,
            'last': user.last,
            'email': user.email,
            'username': user.username,
            'pass_hash': user.pass_hash,
            'pass_salt': user.pass_salt,
            'disabled': user.disabled,
            'theme': user.theme,
            'creation_datetime': str(user.creation_datetime),
        })
        
    _projects = Projects.get_all_projects(
        session = DBSession,
    )
    projects = []
    for project in _projects:
        projects.append({
            'id': project.id,
            'author_id': project.author_id,
            'organization_id': project.organization_id,
            'number': project.number,
            'name': project.name,
            'description': project.description,
            'creation_datetime': str(project.creation_datetime),
            'disabled': project.disabled,
        })
    
    _user_project_assignments = \
        UserProjectAssignments.get_all_user_project_assignments(
            session = DBSession,
        )
    user_project_assignments = []
    for upa in _user_project_assignments:
        user_project_assignments.append({
            'id': upa.id,
            'user_id': upa.user_id,
            'project_id': upa.project_id,
            'disabled': upa.disabled,
            'creation_datetime': str(upa.creation_datetime),
        })
    
    _ticket_types = TicketTypes.get_all_ticket_types(
        session = DBSession,
    )
    ticket_types = []
    for ticket_type in _ticket_types:
        ticket_type.append({
            'id': ticket_type.id,
            'author_id': ticket_type.author_id,
            'project_id': ticket_type.project_id,
            'name': ticket_type.name,
            'description': ticket_type.description,
            'color': ticket_type.color,
            'creation_datetime': str(ticket_type.creation_datetime),
        })
    
    _tickets = Tickets.get_all_tickets(
        session  = DBSession,
    )
    tickets = []
    for ticket in _tickets:
        tickets.append({
            'id': ticket.id,
            'author_id': ticket.author_id,
            'project_id': ticket.project_id,
            'ticket_type_id': ticket.ticket_type_id,
            'number': ticket.number,
            'title': ticket.title,
            'contents': ticket.contents,
            'assigned_id': ticket.assigned_id,
            'closed': ticket.closed,
            'closed_datetime': str(ticket.closed_datetime),
            'creation_datetime': str(ticket.creation_datetime),
        })
    
    _ticket_comments = TicketComments.get_all_ticket_comments(
        session = DBSession,
    )
    ticket_comments = []
    for ticket_comment in _ticket_comments:
        ticket_comments.append({
            'id': ticket_comment.id,
            'author_id': ticket_comment.author_id,
            'ticket_id': ticket_comment.ticket_id,
            'contents': ticket_comment.contents,
            'update_datetime': ticket_comment.update_datetime,
            'flagged': ticket_comment.flagged,
            'flagged_author_id': ticket_comment.flagged_author_id,
            'creation_datetime': str(ticket_comment.creation_datetime),
        })
    
    # _tasks =
    
    # _task_comments =
    
    # _lists =
     
    # _list_items =
    
    # _requirement_types =
    
    # _requirements = 
    
    # _requirement_comments =
    
    _action_types = ActionTypes.get_all_action_types(
        session = DBSession,
    )
    action_types = []
    if _action_types != None:
        for action_type in _action_types:
            action_types.append({
                'id': action_type.id,
                'name': action_type.name,
            })
    
    _action_subjects = ActionSubjects.get_all_action_subjects(
        session = DBSession,
    )
    action_subjects = []
    if _action_subjects != None:
        for action_subject in _action_subjects:
            action_subjects.append({
                'id': action_subject.id,
                'name': action_subject.name,
            })
    
    _actions = Actions.get_all_actions(
        session = DBSession,
    )
    actions = []
    for action in _actions:
        actions.append({
            'id' : action.id,
            'organization_id': action.organization_id,
            'user_id': action.user_id,
            'action_type': action.action_type,
            'subject': action.subject,
            'target_id': action.target_id,
            'project_id': action.project_id,
            'ticket_id': action.ticket_id,
            'requirement_id': action.requirement_id,
            'task_id': action.task_id,
            'list_id': action.list_id,
            'creation_datetime': str(action.creation_datetime),
        })
    
    output = {
        'user_types': user_types,
        'organizations': organizations,
        'users': users,
        'projects': projects,
        'user_project_assignments': user_project_assignments,
        'ticket_types': ticket_types,
        'tickets': tickets,
        'ticket_comments': ticket_comments,
    }
    
    return output
    
    
    