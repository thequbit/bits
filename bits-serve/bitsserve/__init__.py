from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('index', '/')
    
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    
    config.add_route('user','/user')
    
    config.add_route('usersettings', '/usersettings')

    config.add_route('newticket', '/newticket')
    config.add_route('ticket', '/ticket')
    config.add_route('tickets', '/tickets')

    config.add_route('newtask', '/newtask')
    config.add_route('task', '/task')
    config.add_route('tasks', '/tasks')

    config.add_route('newlist', '/newlist')
    #config.add_route('list', '/list')

    config.add_route('newproject', '/newproject')
    config.add_route('project', '/project')
    config.add_route('projectsettings', '/projectsettings')
 

    config.add_route('authenticate.json', 'authenticate.json')
    config.add_route('get_projects.json', 'get_projects.json')
    config.add_route('get_organizations.json', 'get_organizations.json')

    config.add_route('create_project.json','create_project.json')
    config.add_route('assign_user_to_project.json','assign_user_to_project.json')

    config.add_route('create_ticket.json','create_ticket.json')
    config.add_route('close_ticket.json','close_ticket.json')
    config.add_route('create_ticket_comment.json','create_ticket_comment.json')
    config.add_route('assign_user_to_ticket.json', 'assign_user_to_ticket.json')
    config.add_route('update_ticket_contents.json', 'update_ticket_contents.json')
    config.add_route('update_ticket_title.json', 'update_ticket_title.json')
 
    config.add_route('create_task.json','create_task.json')
    config.add_route('complete_task.json','complete_task.json')
    
    config.add_route('database_dump.json', 'database_dump.json')
    config.add_route('database_upload.json', 'database_upload.json')

    config.scan()
    return config.make_wsgi_app()
