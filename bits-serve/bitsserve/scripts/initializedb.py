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
    Tickets,
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


    #
    # Create default Organization
    #

    default_organization = Organizations.get_by_name(
        session = DBSession,
        organization_name = 'Default Organization',
    )

    if default_organization == None:
        default_organization = Organizations.add_organization(
            session = DBSession,
            #author_id = system_user.id,
            name = 'Default Organization',
            description = 'Default Organization.',
        )
    
    
    #
    # Create default user type
    #
    
    regular_user_type_id = UserTypes.user_type_id_from_user_type(
        session = DBSession,
        user_type_name = "Standard User",
    )
    
    if regular_user_type_id == None:
        regular_user_type = UserTypes.add_user_type(
            session = DBSession,
            name = "Standard User",
            description = "Standard User"
        )
    
    
    #
    # Create system user
    #
    
    system_user = Users.get_by_email(
        session = DBSession,
        email = "system",
    )
    
    if system_user == None:
        system_user_type = UserTypes.add_user_type(
            session = DBSession,
            name = "System User",
            description = "System Admin User"
        )

        system_user = Users.add_user(
            session = DBSession,
            organization_id = default_organization.id,
            user_type_id = system_user_type.id,
            first = "System",
            last = "User",
            email = "system",
            password = "password",
        )

    high_priority = TicketPriorities.get_by_name(
        session = DBSession,
        name = 'high',
    )
    if high_priority == None:
        TicketPriorities.add_ticket_priority(
            session = DBSession,
            author_id = system_user.id,
            project_id = None,
            name = 'high',
            description = 'High Priority Ticket',
            weight = 0,
            color = "#B22222",
        )

    medium_priority = TicketPriorities.get_by_name(
        session = DBSession,
        name = 'medium',
    )
    if medium_priority == None:
        TicketPriorities.add_ticket_priority(
            session = DBSession,
            author_id = system_user.id,
            project_id = None,
            name = 'medium',
            description = 'Medium Priority Ticket',
            weight = 1,
            color = "#DAA520",
        )

    low_priority = TicketPriorities.get_by_name(
        session = DBSession,
        name = 'low',
    )
    if low_priority == None:
        TicketPriorities.add_ticket_priority(
            session = DBSession,
            author_id = system_user.id,
            project_id = None,
            name = 'low',
            weight = 2,
            description = 'Low Priority Ticket',
            color = "#22B222",
        )
