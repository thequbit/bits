import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    UserTypes,
    Users,
    Organizations,
    Projects,
    UserProjectAssignments,
    UserOrganizationAssignments,
    TicketTypes,
    TicketPriorities,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
#    with transaction.manager:
#        model = MyModel(name='one', value=1)
#        DBSession.add(model)

    system_user_type = UserTypes.add_user_type(
        session = DBSession,
        name = "System User",
        description = "System Admin User"
    )

    system_user = Users.add_user(
        session = DBSession,
        user_type_id = system_user_type.id,
        first = "System",
        last = "User",
        email = "system",
        password = "password",
    )

    regular_user_type = UserTypes.add_user_type(
        session = DBSession,
        name = "System User",
        description = "System Admin User"
    )

    tim_user = Users.add_user(
        session = DBSession,
        user_type_id = regular_user_type.id,
        first = "Tim",
        last = "Duffy",
        email = "tim@timduffy.me",
        password = "password",
    )

    megan_user = Users.add_user(
        session = DBSession,
        user_type_id = regular_user_type.id,
        first = "Megan",
        last = "Duffy",
        email = "megan@meganduffy.me",
        password = "password",
    )

    temp_user = Users.add_user(
        session = DBSession,
        user_type_id = regular_user_type.id,
        first = 'Temp',
        last = 'User',
        email = 'temp',
        password = 'password',
    )

    default_organization = Organizations.add_organization(
        session = DBSession,
        author_id = system_user.id,
        name = 'Default Organization',
        description = 'Default Organization.',
    )

    #default_user_organization_assignment = \
    #    UserOrganizationAssignments.assign_user_to_organization(
    #        session = DBSession,
    #        user_id = system_user.id,
    #        organization_id = default_organization.id,
    #    )
 
    #default_project = Projects.add_project(
    #    session = DBSession,
    #    author_id = system_user.id,
    #    organization_id = default_organization.id,
    #    name = 'Default Project',
    #    description = 'Default Project.',
    #)

    #system_user_project_assignment = \
    #    UserProjectAssignments.assign_user_to_project(
    #        session = DBSession,
    #        user_id = system_user.id,
    #        project_id = default_project.id,
    #    )

    todo_ticket_type = TicketTypes.add_ticket_type(
        session = DBSession,
        author_id = system_user.id,
        project_id = 1, #default_project.id,
        name = "Todo",
        description = "An item that needs to be completed",
        color = "#0066FF",
    )

    bug_ticket_type = TicketTypes.add_ticket_type(
        session = DBSession,
        author_id = system_user.id,
        project_id = 1, #default_project.id,
        name = "bug",
        description = "An item that needs to be fixed",
        color = "#FF00CC",
    )

    today_ticket_priority = TicketPriorities.add_ticket_priority(
        session = DBSession,
        author_id = system_user.id,
        project_id = 1, #default_project.id,
        name = "Today",
        description = "Must be completed today.",
        weight = 1,
        color = "red",
    )
