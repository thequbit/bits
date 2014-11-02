import uuid
import datetime
import hashlib

import transaction

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    )

from sqlalchemy import func, desc

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension(),
        expire_on_commit=False
    )
)
Base = declarative_base()

class UserTypes(Base):

    __tablename__ = 'usertypes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)

    @classmethod
    def add_user_type(cls, session, name, description):
        """
        """
        with transaction.manager:
            user_type = cls(
                name = name,
                description = description,
            )
            session.add(user_type)
            transaction.commit()
        return user_type

    @classmethod
    def user_type_id_from_user_type(cls, session, user_type_name):
        """ Gets the UserType.id from a UserType.name
        """
        user_type = None
        with transaction.manager:
            user_type = session.query(
                UserTypes,
            ).filter(
                UserTypes.name == user_type_name,
            ).first()
        id = None
        if user_type != None:
            id = user_type.id
        return id

    @classmethod
    def user_type_from_id(cls, session, user_type_id):
        """ Returns the user type from it's id
        """
        with transaction.manager:
            user_type = session.query(
                UserTypes,
            ).filter(
                UserTypes.id == user_type_id,
            ).first()
        return user_type

    @classmethod
    def get_all_user_types(cls, session):
        """ Returns all available user types
        """
        with transaction.manager:
            user_types = session.query(
                UserTypes,
            ).order_by(
                UserTypes.id,
            ).all()
        return user_types

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    user_type_id = Column(Integer, ForeignKey('usertypes.id'))
    first = Column(Text)
    last = Column(Text)
    email = Column(Text)
    username = Column(Text)
    pass_hash = Column(Text)
    pass_salt = Column(Text)
    disabled = Column(Boolean)
    theme = Column(Text)
    creation_datetime = Column(DateTime)
 
    @classmethod
    def add_user(cls, session, user_type_id, first, last, email, password):
        """ Adds a new user to the database.  Generates a salt and hashes the 
            password concatendated with that salt.  Also must decode the
            user_type field into a user_type_id
        """
        with transaction.manager:
            pass_salt = str(uuid.uuid4())
            pass_hash = hashlib.sha256('{0}{1}'.format(
                password,
                pass_salt
            )).hexdigest()
            user = cls(
                user_type_id = user_type_id,
                first = first,
                last = last,
                email = email,
                pass_hash = pass_hash,
                pass_salt = pass_salt,
                disabled = False,
                theme = 'light', # default
                creation_datetime = datetime.datetime.now(),
            )
            session.add(user)
            transaction.commit()
        return user
        
    @classmethod
    def disable_user(cls, session, email):
        """
        """
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
            user.disabled = True
            session.add(user)
            transaction.commit()
        return user

    @classmethod
    def authenticate_user(cls, session, email, password):
        """ Authenticates a users login.  Returns a token if successful
        """
        with transaction.manager:
            user = None
            _user = session.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
            if _user != None:
                pass_hash = hashlib.sha256('{0}{1}'.format(
                    password,
                    _user.pass_salt,
                )).hexdigest()
                if _user.pass_hash == pass_hash:
                    user = _user
        return user

    @classmethod
    def get_by_id(cls, session, user_id):
        """ Get a user by their ID
        """
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.id == user_id,
            ).first()

        return user

    @classmethod
    def get_by_email(cls, session, email):
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
        return user

    @classmethod
    def get_all_users(cls, session):
        with transaction.manager:
            users = session.query(
                Users,
            ).order_by(
                Users.id,
            ).all()
        return users
        
    @classmethod
    def get_users_from_organization_id(cls, session, organization_id):
        with transaction.manager:
            users = session.query(
                Users,
            ).filter(
                Users.organization_id == organization_id,
            ).all()
        return users

class LoginTokens(Base):

    __tablename__ = 'logintokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(Text, nullable=True)
    token_expire_datetime = Column(DateTime)
    login_datetime = Column(DateTime) 

    @classmethod
    def do_login(cls, session, email, password):
        """ Login a user
        """
        with transaction.manager:
            user = Users.authenticate_user(
                session = session,
                email = email,
                password = password,
            )
            if user != None:
                login_token = cls(
                    user_id = user.id,
                    token = str(uuid.uuid4()),
                    token_expire_datetime = datetime.datetime.now() + \
                        datetime.timedelta(hours=24),
                    login_datetime = datetime.datetime.now(),
                )
                session.add(login_token)
                transaction.commit() 
        return user, login_token.token

    @classmethod
    def check_authentication(cls, session, token):
        """ Check to see if the token is valid for the user
        """
        with transaction.manager:
            user = None
            login_token = session.query(
                LoginTokens,
            ).filter(
                LoginTokens.token == token,
                LoginTokens.token_expire_datetime > datetime.datetime.now(),
            ).first()
            if login_token != None:
                user = Users.get_by_id(
                    session = session,
                    user_id = login_token.user_id,
                )
        return user

    @classmethod
    def logout(cls, session, token):
        with transaction.manager:
            login_token = session.query(
                LoginTokens,
            ).filter(
                LoginTokens.token == token,
            ).first()
            session.delete(login_token)
            transaction.commit()
        return

class Organizations(Base):

    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    #author_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Text)
    description = Column(Text)
    disabled = Column(Boolean)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_organization(cls, session, name, description):
        """ Adds a new organization from a user
        """
        with transaction.manager:
            organization = cls(
                #author_id = author_id,
                name = name,
                description = description,
                disabled = False,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(organization)
            transaction.commit()
        return organization

    @classmethod
    def disable_organization(cls, session, organization_id):
        """ Disable an orgnization
        """
        with transaction.manager:
            organization = session.query(
                Organizations,
            ).filter(
                Organizations.id == organization_id,
            ).first()
            organization.disabled= True
            session.add(organization)
            transaction.commit()
        return organization

    @classmethod
    def update_organization(cls, session, organization_id, name, description):
        """ update organization definition
        """
        with transaction.manager:
            organization = session.query(
                Organizations,
            ).filter(
                Organizations.id == organization_id,
            ).first()
            organization.name = name
            organization.description = description
            session.add(organization)
            transaction.commit()
        return organization
        
    @classmethod
    def get_by_name(cls, session, organization_name):
        """ get organization by name
        """
        with transaction.manager:
            organization = session.query(
                Organizations,
            ).filter(
                Organizations.name == organization_name,
            ).first()
        return organization

    @classmethod
    def get_all_organizations(cls, session):
        with transaction.manager:
            organizations = session.query(
                Organizations,
            ).order_by(
                Organizations.id,
            ).all()
        return organizations

class UserOrganizationAssignments(Base):

    __tablename__ = 'userorganizationassignments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    disabled = Column(Boolean)
    creation_datetime = Column(DateTime)


    @classmethod
    def assign_user_to_organization(cls, session, user_id, organization_id):
        """ Assign a user to an organization
        """
        with transaction.manager:
            user_organization_assignment = cls(
                user_id = user_id,
                organization_id = organization_id,
                disabled = False,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(user_organization_assignment)
            transaction.commit()
        return user_organization_assignment

    @classmethod
    def unassign_user_from_organization(cls, session, \
            user_organization_assignment_id):
        """ Unassign a user form an organization
        """
        with transaction.manager:
            user_organization_assignment = session.query(
                UserOrganizationAssignments,
            ).filter(
                UserOrganizationAssignments.id == \
                    user_organization_assignment_id,
            ).first()
            user_organization_assignment.disabled = True
            session.add(user_organization_assignment)
            transaction.commit()
        return user_organization_assignment

    @classmethod
    def get_users_organizations(cls, session, user_id):
        """ Get all organizations the user is assigned to
        """
        with transaction.manager:
            organizations = session.query(
                UserOrganizationAssignments.id,
                UserOrganizationAssignments.disabled,
                Organizations.id,
                Organizations.name,
                Organizations.description,
                Organizations.creation_datetime,
                Organizations.disabled,
                Users.first,
                Users.last,
                Users.email,
            ).join(
                Organizations,Organizations.id == \
                    UserOrganizationAssignments.organization_id,
            ).join(
                Users,Users.id == Organizations.author_id,
            ).filter(
                UserOrganizationAssignments.user_id == user_id,
            ).all()
        return organizations


class Projects(Base):

    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    organization_id = Column(Integer, ForeignKey('projects.id'))
    number = Column(Integer, autoincrement=True)
    name = Column(Text)
    description = Column(Text)
    creation_datetime = Column(DateTime)
    disabled = Column(Boolean)
    
    @classmethod
    def add_project(cls, session, author_id, organization_id, name, \
            description):
        """ Adds a new project from a user, and connected to an organization
        """
        with transaction.manager:
            project = cls(
                author_id = author_id,
                organization_id = organization_id,
                name = name,
                description = description,
                creation_datetime = datetime.datetime.now(),
                disabled = False,
            )
            session.add(project)
            transaction.commit()
        return project
        
    @classmethod
    def disable_project(cls, session, project_id):
        """ Disables a project
        """
        with transaction.manager:
            project = session.query(
                Projects,
            ).filter(
                Projects.id == project_id,
            ).first()
            project.disabled = True
            session.add(project)
            transaction.commit()
        return project

    @classmethod
    def get_from_id(cls, session, project_id):
        """ Get a project from it's id
        """

        with transaction.manager:
            project = session.query(
                Projects.id,
                Projects.name,
                Projects.description,
                Projects.creation_datetime,
                Projects.disabled,
                Users.id,
                Users.first,
                Users.last,
                Users.email,
                func.count(Requirements.id),
                func.count(Tickets.id),
            ).join(
                Users,Users.id == Projects.author_id,
            ).outerjoin(
                Requirements,Requirements.project_id == Projects.id,
            ).outerjoin(
                Tickets,Tickets.project_id == Projects.id,
            ).filter(
                Projects.id == project_id,
            ).first()

        return project

    @classmethod
    def get_name_from_id(cls, session, project_id):
        """ Get a project'sname from it's id
        """
        with transaction.manager:
            project_name = session.query(
                Projects.name,
            ).filter(
                Projects.id == project_id,
            ).first()

        return project_name

    @classmethod
    def get_projects_from_user_id(cls, session, user_id):
        """ Get all of the projects the user has access to
        """
        projects = UserProjectAssignments.get_user_projects(
            session = session,
            user_id = user_id,
        )
        return projects
        
    @classmethod
    def get_all_projects(cls, session):
        with transaction.manager:
            projects = session.query(
                Projects,
            ).order_by(
                Projects.id
            ).all()
        return projects

class UserProjectAssignments(Base):

    __tablename__ = 'userprojectassignments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    disabled = Column(Boolean)
    creation_datetime = Column(DateTime)    

    @classmethod
    def assign_user_to_project(cls, session, user_id, project_id):
        """ Assign a user to a project
        """
        with transaction.manager:
            user_project_assignment = cls(
                user_id = user_id,
                project_id = project_id,
                disabled = False,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(user_project_assignment)
            transaction.commit()
        return user_project_assignment

    @classmethod
    def unassign_user_from_project(cls, session, user_project_assignment_id):
        """ Unassign a user form a project
        """
        with transaction.manager:
            user_project_assignment = session.query(
                UserProjectAssignments,
            ).filter(
                UserProjectAssignments.id == user_project_assignment_id,
            ).first()
            user_project_assignment.disabled = True
            session.add(user_project_assignment)
            transaction.commit()
        return user_project_assignment

    @classmethod
    def get_user_project_assignment(cls, session, user_id, project_id):
        """ get a user project assignment from a user id and project_id
        """
        with transaction.manager:
            assignment = session.query(
                UserProjectAssignments
            ).filter(
                UserProjectAssignments.user_id == user_id,
                UserProjectAssignments.project_id == project_id,
            ).first()
        return assignment

    @classmethod
    def get_users_assigned_to_project(cls, session, project_id):
        """ Get all of the users assigned to a project
        """
        with transaction.manager:
            users = session.query(
                UserProjectAssignments.id,
                Users.id,
                Users.first,
                Users.last,
                Users.email,
            ).join(
                Users, UserProjectAssignments.user_id == Users.id,
            ).filter(
                UserProjectAssignments.project_id == project_id,
            ).all()
        return users
        
    @classmethod
    def get_user_projects(cls, session, user_id):
        """ Get all projects the user is assigned to
        """
        with transaction.manager:
            projects = session.query(
                UserProjectAssignments.id,
                UserProjectAssignments.disabled,
                Projects.id,
                Projects.name,
                Projects.description,
                Projects.creation_datetime,
                Projects.disabled,
                Users.first,
                Users.last,
                Users.email,
                func.count(Requirements.id),
                func.count(Tickets.id),
                #func.count(Notes.id),
            ).join(
                Projects,Projects.id == UserProjectAssignments.project_id,
            ).join(
                Users,Users.id == Projects.author_id,
            ).outerjoin(
                Requirements,Requirements.project_id == Projects.id,
            ).outerjoin(
                Tickets,Tickets.project_id == Projects.id,
            ).filter(
                UserProjectAssignments.user_id == user_id,
            ).group_by (
                UserProjectAssignments.id,
            ).all()
        return projects

    @classmethod
    def check_project_assignment(cls, session, user_id, project_id):
        """ Checks to ensure that a user and project are matched
        """
        with transaction.manager:
            assignment = session.query(
                UserProjectAssignments,
            ).filter(
                UserProjectAssignments.user_id == user_id,
                UserProjectAssignments.project_id == project_id,
                UserProjectAssignments.disabled == False,
            ).first()
            valid = False
            if assignment != None:
                valid = True
        return valid
        
    @classmethod
    def get_all_user_project_assignments(cls, session):
        with transaction.manager:
            user_project_assignments = session.query(
                UserProjectAssignments,
            ).order_by(
                UserProjectAssignments.id,
            ).all()
        return user_project_assignments

class TicketTypes(Base):

    __tablename__ = 'tickettypes'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(Text)
    description = Column(Text)
    color = Column(Text)
    creation_datetime = Column(DateTime)
    
    @classmethod
    def add_ticket_type(cls, session, author_id, project_id, name, \
            description, color):
        """ Adds a new ticket type
        """
        with transaction.manager:
            ticket_type = cls(
                author_id = author_id,
                project_id = project_id,
                name = name,
                description = description,
                color = color,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(ticket_type)
            transaction.commit()
        return ticket_type
    
    @classmethod
    def get_all_ticket_types(cls, session):
        """ Returns all of the ticket types for the project
        """
        with transaction.manager:
            ticket_types = session.query(
                TicketTypes,
            ).all()
        return ticket_types
    
class TicketPriorities(Base):

    __tablename__ = 'ticketpriorities'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(Text)
    description = Column(Text)
    weight = Column(Integer)
    color = Column(Text)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_ticket_priority(cls, session, author_id, project_id, name, \
            description, weight, color):
        """ Adds a new ticket priority
        """
        with transaction.manager:
            ticket_priority = cls(
                author_id = author_id,
                project_id = project_id, 
                name = name,
                description = description,
                weight = weight,
                color = color,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(ticket_priority)
            transaction.commit()
        return ticket_priority

    @classmethod
    def get_ticket_priorities_by_project_id(cls, session, project_id):
        """ Returns the list of ticket priorities for a project.
        """
        with transaction.manager:
            ticket_priorities = session.query(
                TicketPriorities,
            ).filter(
                TicketPriorities.project_id == project_id,
            ).all()
        return ticket_priorities

class Tickets(Base):

    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    ticket_type_id = Column(Integer, ForeignKey('tickettypes.id'))
    number = Column(Integer)
    title = Column(Text)
    contents = Column(Text)
    #ticket_priority_id = Column(Integer, ForeignKey('ticketpriorities.id'))
    assigned_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    closed = Column(Boolean)
    closed_datetime = Column(DateTime, nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_ticket(cls, session, author_id, project_id, ticket_type_id, \
            number, title, contents, assigned_id):
        """ Adds a new ticket to the system
        """
        with transaction.manager:
            ticket = cls(
                author_id = author_id,
                project_id = project_id,
                ticket_type_id = ticket_type_id,
                number = number,
                title = title,
                contents = contents,
                assigned_id = assigned_id,
                closed = False,
                closed_datetime = None,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(ticket)
            transaction.commit()
        return ticket

    @classmethod
    def close_ticket(cls, session, ticket_id):
        """ Sets a ticket's status to closed
        """
        with transaction.manager:
            ticket = session.query(
                Tickets,
            ).filter(
                Tickets.id == ticket_id,
            ).first()
            ticket.closed = True
            ticket.closed_datetime = datetime.datetime.now()
            session.add(ticket)
            transaction.commit()
        return ticket

    @classmethod
    def _build_ticket_query(cls, session):
        #with transaction.manager:
        if True:
            ticket_query = session.query(
                Tickets.id,
                Tickets.number,
                Tickets.title,
                Tickets.contents,
                Tickets.assigned_id,
                Tickets.closed,
                Tickets.closed_datetime,
                Tickets.creation_datetime,
                Users.first,
                Users.last,
                Users.email,
                Projects.id,
                Projects.name,
                Projects.description,
                Projects.creation_datetime,
                TicketTypes.name,
                TicketTypes.description,
                TicketTypes.color,
                #TicketPriorities.name,
                #TicketPriorities.description,
                #TicketPriorities.weight,
                #TicketPriorities.color,
            ).join(
                Users,Users.id == Tickets.author_id,
            ).join(
                Projects,Projects.id == Tickets.project_id,
            ).outerjoin(
                TicketTypes,TicketTypes.id == Tickets.ticket_type_id,
            #).join(
            #    TicketPriorities,TicketPriorities.id == \
            #        Tickets.ticket_priority_id,
            )
        return ticket_query

    @classmethod
    def get_tickets_by_project_id(cls, session, project_id, closed):
        """ Get all of the tickets, and their conents by project id
        """
        with transaction.manager:
            ticket_query = Tickets._build_ticket_query(session)
            tickets = ticket_query.filter(
                Tickets.project_id == project_id,
                Tickets.closed == closed,
            ).all()
        return tickets

    @classmethod
    def get_ticket_by_id(cls, session, ticket_id):
        """ Get all of the tickets, and their conents by project id
        """
        with transaction.manager:
            ticket_query = Tickets._build_ticket_query(session)
            ticket = ticket_query.filter(
                Tickets.id == ticket_id,
            ).first()
            
        return ticket
          
    @classmethod
    def get_raw_ticket_by_id(cls, session, ticket_id):
        with transaction.manager:
            ticket = session.query(
                Tickets,
            ).filter(
                Tickets.id == ticket_id,
            ).first()
        return ticket
        
    @classmethod
    def get_last_ticket_number(cls, session, project_id):
        with transaction.manager:
            last_number = session.query(
                #Tickets.id,
                Tickets.number,
            ).filter(
                Tickets.project_id == project_id,
            #).group_by(
            #    Tickets.id,
            ).order_by(
                desc(Tickets.number),
            ).first();
        return last_number

    @classmethod
    def get_all_tickets(cls, session):
        with transaction.manager:
            tickets = session.query(
                Tickets,
            ).order_by(
                Tickets.id,
            ).all()
        return tickets
        
    @classmethod
    def assign_user_to_ticket(cls, session, ticket_id, email):
        with transaction.manager:
            user = Users.get_by_email(session, email)
            ticket = Tickets.get_raw_ticket_by_id(session, ticket_id)
            ticket.assigned_id = user.id
            session.add(ticket)
            transaction.commit()
        return ticket

class TicketComments(Base):

    __tablename__ = 'ticketcomments'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))    
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    contents = Column(Text)
    update_datetime = Column(DateTime, nullable=True)
    flagged = Column(Boolean)
    flagged_author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    creation_datetime = Column(DateTime)
    
    @classmethod
    def add_ticket_comment(cls, session, author_id, ticket_id, contents):
        """ Adds a comment to a ticket
        """
        with transaction.manager:
            ticket_comment = cls(
                author_id = author_id,
                ticket_id = ticket_id,
                contents = contents,
                update_datetime = None,
                flagged = False,
                flagged_author_id = None,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(ticket_comment)
            transaction.commit()
        return ticket_comment

    @classmethod
    def update_ticket_comment(cls, session, ticket_comment_id, content):
        """ Updates the content of a ticket comment
        """
        with transaction.manager:
            ticket_comment = session.query(
                TicketComments,
            ).filter(
                TicketComments.id == ticket_comment_id,
            ).first()
            ticket_comment.contents = contents
            ticket_comments.update_datetime = datetime.datetime.now()
            session.add(ticket_comment)
            transaction.commit()
        return ticket_comment

    @classmethod
    def flag_ticket_comment(cls, session, ticket_comment_id):
        """ Flaggs a ticket comment
        """
        with transaction.manager:
            ticket_comment = session.query(
                TicketComments,
            ).filter(
                TicketComments.id == ticket_comment_id,
            ).first()
            ticket_comment.flagged = True
            session.add(ticket_comment)
            transaction.commit()
        return ticket_comment

    @classmethod
    def get_ticket_comments_by_ticket_id(cls, session, ticket_id):
        """ Get all comments for a specific ticket
        """
        with transaction.manager:
            comments = session.query(
                TicketComments.id,
                TicketComments.contents,
                TicketComments.flagged,
                TicketComments.flagged_author_id,
                TicketComments.update_datetime,
                TicketComments.creation_datetime,
                Users.id,
                Users.first,
                Users.last,
                Users.email,
            ).outerjoin(
                Users, Users.id == TicketComments.flagged_author_id,
            ).join(
                Users, Users.id == TicketComments.author_id,
            ).filter(
                TicketComments.ticket_id == ticket_id,
            ).order_by(
                TicketComments.creation_datetime,
            ).all() 
        return comments
        
    @classmethod
    def get_all_ticket_comments(cls, session):
        with transaction.manager:
            ticket_comments = session.query(
                TicketComments,
            ).order_by(
                TicketComments.id,
            ).all()
        return ticket_comments

class Tasks(Base):

    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    title = Column(Text)
    contents = Column(Text)
    assigned_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    due_datetime = Column(DateTime, nullable=True)
    completed = Column(Boolean)
    completed_datetime = Column(DateTime, nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_task(cls, session, author_id, project_id, title, contents, \
            assigned, due):
        with transaction.manager:
            assigned_user_id = None
            if assigned != '' and assigned != None:
                assigned_user = Users.get_by_email(
                    session = session,
                    email = assigned,
                )
                assigned_user_id = assigned_user.id
            task = cls(
                author_id = author_id,
                project_id = project_id,
                title = title,
                contents = contents,
                assigned_id = assigned_user_id,
                due_datetime = due,
                completed = False,
                completed_datetime = None,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(task)
            transaction.commit()
        return task

    @classmethod
    def complete_task(cls, session, task_id):
        with transaction.manager:
            task = session.query(
                Tasks,
            ).filter(
                Tasks.id == task_id,
            ).first()
            task.completed = False
            task.completed_datetime = datetime.datetime.now()
            session.add(task)
            transaction.commit()
        return task

    @classmethod
    def _build_task_query(cls, session):
        if True:
            task_query = session.query(
                Tasks.id,
                Tasks.title,
                Tasks.contents,
                Tasks.due_datetime,
                Tasks.completed,
                Tasks.completed_datetime,
                Tasks.creation_datetime,
                Users.id,
                Users.first,
                Users.last,
                Users.email,
                Projects.id,
                Projects.name,
            ).join(
                Users, Users.id == Tasks.author_id,
            ).join(
                Projects, Projects.id == Tasks.project_id,
            )
        return task_query

    @classmethod
    def get_by_id(cls, session, task_id):
        with transaction.manager:
            task_query = Tasks._build_task_query(session)
            task = task_query.filter(
                Tasks.id == task_id,
            ).first()
        return task

    @classmethod
    def get_tasks_by_project_id(cls, session, project_id):
        with transaction.manager:
            task_query = Tasks._build_task_query(session)
            tasks = task_query.filter(
                Tasks.project_id == project_id,
            ).all()
        return tasks

class TaskComments(Base):

    __tablename__ = 'taskcomments'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    contents = Column(Text)
    update_datetime = Column(DateTime, nullable=True)
    flagged = Column(Boolean)
    flagged_author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_task_comment(cls, session, author_id, task_id, contents):
        """ Adds a comment to a task
        """
        with transaction.manager:
            task_comment = cls(
                author_id = author_id,
                task_id = task_id,
                contents = contents,
                update_datetime = None,
                flagged = False,
                flagged_author_id = None,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(task_comment)
            transaction.commit()
        return task_comment

    @classmethod
    def update_task_comment(cls, session, task_comment_id, content):
        """ Updates the content of a task comment
        """
        with transaction.manager:
            task_comment = session.query(
                TaskComments,
            ).filter(
                TaskComments.id == task_comment_id,
            ).first()
            task_comment.contents = contents
            task_comments.update_datetime = datetime.datetime.now()
            session.add(task_comment)
            transaction.commit()
        return task_comment

    @classmethod
    def flag_task_comment(cls, session, task_comment_id):
        """ Flaggs a task comment
        """
        with transaction.manager:
            task_comment = session.query(
                TaskComments,
            ).filter(
                TaskComments.id == task_comment_id,
            ).first()
            task_comment.flagged = True
            session.add(task_comment)
            transaction.commit()
        return task_comment

class Lists(Base):

    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(Text)
    disabled = Column(Boolean)
    disabled_datetime = Column(DateTime, nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_list(cls, session, owner_id, project_id, name):
        with transaction.manager:
            l = cls(
                owner_id = owner_id,
                project_id = project_id,
                name = name,
                disabled = False,
                disabled_datetime = None,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(l)
            transaction.commit()
        return l
    
    @classmethod
    def _build_list_query(cls, session):
        if True:
            list_query = session.query(
                Lists.id,
                Lists.name,
                Lists.disabled,
                Lists.disabled_datetime,
                Lists.creation_datetime,
                Users.id,
                Users.first,
                Users.last,
                Users.email,
                Projects.id,
                Projects.name,
            ).join(
                Users, Users.id == Lists.owner_id,
            ).join(
                Projects, Projects.id == Lists.project_id,
            )
        return list_query

    @classmethod
    def get_lists_by_project_id(cls, session, project_id):
        list_query = Lists._build_list_query(session)
        lists = list_query.filter(
            Lists.project_id == project_id,
        ).all()
        return lists

    @classmethod
    def get_by_id(cls, session, list_id):
        list_query = Lists._build_list_query(session)
        l = list_query.filter(
            Lists.id == list_id,
        ).first()
        return l 

class ListItems(Base):

    __tablename__ = 'listitems'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    list_id = Column(Integer, ForeignKey('lists.id'))
    contents = Column(Text)
    removed = Column(Boolean)
    removed_datetime = Column(DateTime)
    modified = Column(Boolean)
    modifed_datetime = Column(DateTime, nullable=True)
    creation_datetime = Column(Text)

    @classmethod
    def add_item(cls, session, owner_id, list_id, contents):
        with transaction.manager:
            list_item = cls(
                owner_id = owner_id,
                list_id = list_id,
                contents = contents,
                removed = False,
                removed_datetime = None,
                modifed = False,
                modified_datetime = False,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(list_item)
            transaction.commit()
        return

    @classmethod
    def remove_item(cls, session, item_id):
        with transaction.manager:
            item = session.query(
                ListItems,
            ).filter(
                ListItem.id == item_id,
            ).first()
            item.removed = True
            session.add(item)
            transaction.commit()
        return item

class RequirementTypes(Base):

    __tablename__ = 'requirementtypes'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(Text)
    description = Column(Text)
    removed = Column(Boolean)
    removed_datetime = Column(DateTime, nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_requirement_type(cls, session, author_id, project_id, name, \
            description):
        """ Add a requirement type to a project.
        """
        with transaction.manager:
            requirement_type = cls(
                author_id = author_id,
                project_id = project_id,
                name = name,
                description = description,
            )
            session.add(requirement_type)
            transaction.commit()
        return requirement_type

    @classmethod
    def remove_requirement_type(cls, session, requirement_type_id):
        """ Removes a requirement type from a project.
        """
        with transaction.manager:
            requirement_type = session.query(
                RequirementTypes,
            ).filter(
                RequirementTypes.id == requirement_type_id,
            ).first()
            requirement_type.removed = True
            session.add(requirement_type)
            transaction.commit()
        return requirement_type

    @classmethod
    def _build_requirement_types_qury(cls, session):
        if True:
            requirement_type_query = session.query(
                RequirementTypes.id,
                RequirementTypes.name,
                RequirementTypes.description,
                RequirementTypes.removed,
                RequirementTypes.removed_datetime,
                RequirementTypes.created_datetime,
                Users.id,
                Users.first,
                Users.last,
                Users.email,
                Projects.id,
            ).join(
                Users, Users.id == RequirementTypes.project_id,
            ).join(
                Projects, Projects.id == RequirementTypes.project_id,
            )
        return requirement_type_query

    @classmethod
    def get_requirement_types_by_project_id(cls, session, project_id):
        """ Get the requirement types for a project
        """
        with transaction.manager:
            requirement_type_query = \
                RequirementTypes._buil_requirements_type_query(session)
            requirement_types = requirement_type_query.filter(
                RequirementTypes.project_id == project_id,
            ).all()
        return requirement_types

class Requirements(Base):

    __tablename__ = 'requirements'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    requirement_type_id = Column(Integer, ForeignKey('requirementtypes.id'))
    number = Column(Integer, autoincrement=True)
    title = Column(Text)
    contents = Column(Text)
    version = Column(Integer)
    modified_datetime = Column(DateTime, nullable=True)
    removed = Column(Boolean)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_requirement(cls, session, author_id, project_id, \
            requirement_type_id, title, contents):
        """ Adds a new requirement
        """
        with transaction.manager:
            requirement = cls(
                author_id = author_id,
                project_id = project_id,
                requirement_type_id = requirement_type_id,
                title = title,
                contents = contents,
                version = 1,
                modified_datetime = None,
                removed = False,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(requirement)
            transaction.commit()
        return requirement

    @classmethod
    def remove_requirement(cls, session, requirement_id):
        """ Remove a requirement from a project (sets removed flag)
        """
        with transaction.manager:
            requirement = session.querty(
                Requirements,
            ).filter(
                Requirements.id == requirement_id,
            ).first()
            requirement.removed = True
            session.add(requirement)
            transaction.commit()
        return requirement

    @classmethod
    def get_requirements_by_project_id(cls, session, project_id):
        """ Gets all of the requirements for a project
        """

    @classmethod
    def get_all_versions_by_requirement_id(cls, session, requirement_id):
        """ Returns all of the versions of the requirement
        """

class RequirementComments(Base):

    __tablename__ = 'requirementcomments'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    requirement_id = Column(Integer, ForeignKey('requirements.id'))
    contents = Column(Text)
    update_datetime = Column(DateTime, nullable=True)
    flagged = Column(Boolean)
    flagged_author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_requirement_comment(cls, session, author_id, requirement_id, contents):
        """ Adds a comment to a requirement
        """
        with transaction.manager:
            ticket_comment = cls(
                author_id = author_id,
                requirement_id = requirement_id,
                contents = contents,
                update_datetime = None,
                flagged = False,
                flagged_author_id = None,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(ticket_comment)
            transaction.commit()
        return ticket_comment

    @classmethod
    def update_requirement_comment(cls, session, requirement_comment_id, content):
        """ Updates the content of a requirement comment
        """
        with transaction.manager:
            ticket_comment = session.query(
                RequirementComments,
            ).filter(
                RequirementComments.id == requirement_comment_id,
            ).first()
            requirement_comment.contents = contents
            requirement_comments.update_datetime = datetime.datetime.now()
            session.add(ticket_comment)
            transaction.commit()
        return ticket_comment

    @classmethod
    def flag_requirement_comment(cls, session, requirement_comment_id):
        """ Flaggs a ticket comment
        """
        with transaction.manager:
            requirement_comment = session.query(
                RequirementComments,
            ).filter(
                RequirementComments.id == requirement_comment_id,
            ).first()
            requirement_comment.flagged = True
            session.add(requirement_comment)
            transaction.commit()
        return requirement_comment

class ActionTypes(Base):

    """ These are actions that can be applied to a subject.
        Examples include create, delete, edit, close, etc.
    """

    __tablename__ = 'actiontypes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    @classmethod
    def add(cls, session, name):
        with transaction.manager:
            action_type = cls(
                name = name,
            )
            session.add(action_type)
            transaction.commit()
        return action_type

    @classmethod
    def get_by_name(cls, session, name):
        with transaction.manager:
            action_type = session.query(
                ActionTypes,
            ).filter(
                ActionTypes.name == name,
            ).first()
        return action_type
        
    @classmethod
    def get_all_action_types(cls, session):
        with transaction.manager:
            action_types = session.query(
                ActionTypes,
            ).order_by(
                ActionTypes.id,
            ).all()
        return action_types

class ActionSubjects(Base):

    """ These are the subjects actions can be applied to.
        Examples include projects, tickets, requirements, etc.
    """

    __tablename__ = 'actionsubjects'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    @classmethod
    def add(cls, session, name):
        with transaction.manager:
            action_subject = cls(
                name = name,
            )
            session.add(action_subject)
            transaction.commit()
        return action_subject

    @classmethod
    def get_by_name(cls, session, name):
        with transaction.manager:
            action_subject = session.query(
                ActionSubjects,
            ).filter(
                ActionSubjects.name == name,
            ).first()
        return action_subject

    @classmethod
    def get_all_action_subjects(cls, session):
        with transaction.manager:
            action_subjects = session.query(
                ActionSubjects,
            ).filter(
                ActionSubjects.id,
            ).first()
        return action_subjects

class Actions(Base):

    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    contents = Column(Text)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_action(cls, session, organization_id, user_id, project_id, \
            contents):
        """ Add an action
        """
        with transaction.manager:
            action = cls(
                organization_id = organization_id,
                user_id = user_id,
                project_id = project_id,
                contents = contents,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(action)
            transaction.commit()
        return action

    @classmethod
    def _build_action_query(cls, session):
        action_query = session.query(
            Actions.id,
            Actions.contents,
            Actions.creation_datetime,
            Users.id,
            Users.first,
            Users.last,
            Users.email,
            Projects.id,
            Projects.name,
            UserProjectAssignments.id,
        ).join(
            Users, Users.id == Actions.user_id,
        ).join(
            Projects, Projects.id == Actions.project_id,
        ).join(
            UserProjectAssignments,
            UserProjectAssignments.project_id == \
                Actions.project_id,
        )
        
        return action_query

    @classmethod
    def get_action_by_id(cls, session, action_id):
        """ Gets an action by its id
        """
        with transaction.manager:
            action_query = Actions._build_action_query(session)
            action = action_query.filter(
                Actions.id == action_id,
            ).first()
        return action

    @classmethod
    def get_user_action_list(cls, session, user_id, limit=25):
        """ Get's the action feed for a user
        """ 
        with transaction.manager:
            action_query = Actions._build_action_query(session)
            actions = action_query.filter(
                UserProjectAssignments.user_id == user_id,
            ).group_by(
                Actions.id,
            ).order_by(
                desc(Actions.creation_datetime),
            ).all()
        return actions

    @classmethod
    def get_user_actions(cls, session, user_id, limit=25):
        """ Get's the action feed for a user
        """ 
        with transaction.manager:
            action_query = Actions._build_action_query(session)
            actions = action_query.filter(
                Actions.user_id == user_id,
            ).group_by(
                Actions.id,
            ).order_by(
                desc(Actions.creation_datetime),
            ).all()
        return actions

    @classmethod
    def get_latest_actions_by_org_id(cls, session, organization_id, limit):
        """ Get latest actions
        """
        with transaction.manager:
            actions = session.query(
                Actions,
            ).filter(
                Actions.organization_id == organization_id,
            ).limit(limit)
        return actions
        
    @classmethod
    def get_all_actions(cls, session):
        with transaction.manager:
            actions = session.query(
                Actions,
            ).order_by(
                Actions.id,
            ).all()
        return actions

