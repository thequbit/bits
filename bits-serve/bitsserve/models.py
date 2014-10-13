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
        id = user_type.id
        return id

    @classmethod
    def get_all_user_types(cls, session):
        """ Returns all available user types
        """
        with transaction.manager:
            user_types = session.query(
                UserTypes,
            ).all()
        return user_types

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_type_id = Column(Integer, ForeignKey('usertypes.id'))
    first = Column(Text)
    last = Column(Text)
    email = Column(Text)
    username = Column(Text)
    pass_hash = Column(Text)
    pass_salt = Column(Text)
    disabled = Column(Boolean)
    token = Column(Text, nullable=True)
    token_expire_datetime = Column(DateTime, nullable=True)
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
                token = None,
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
        token = None
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
            if user != None:
                pass_hash = hashlib.sha256('{0}{1}'.format(
                    password,
                    user.pass_salt,
                )).hexdigest()
                if user.pass_hash == pass_hash:
                    token = str(uuid.uuid4())
                    user.token_expire_datetime = datetime.datetime.now() + \
                        datetime.timedelta(hours=24)
                    user.token = token
                    session.add(user)
                    transaction.commit()
        return token

    @classmethod
    def check_authentication(cls, session, token):
        """ Check to see if the token is valid for the user
        """
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.token == token,
                Users.token_expire_datetime > datetime.datetime.now(),
            ).first()
        return user

class Organizations(Base):

    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Text)
    description = Column(Text)
    disabled = Column(Boolean)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_organization(cls, session, author_id, name, description):
        """ Adds a new organization from a user
        """
        with transaction.manager:
            organization = cls(
                author_id = author_id,
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
                Projects.project_id == project_id,
            ).first()
            project.disabled = True
            session.add(project)
            transaction.commit()
        return project

    @classmethod
    def get_projects_from_user_id(cls, session, user_id):
        """ get all of the projects the user has access to
        """

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
    def get_users_projects(cls, session, user_id):
        """ Get all projects the user is assigned to
        """
        with transaction.manager:
            projects = session.query(
                UserProjectAssignments.id,
                UserProjectAssignments.disabled,
                Projects.name,
                Projects.description,
                Projects.creation_datetime,
                Projects.disabled,
                Users.first,
                Users.last,
                Users.email,
            ).join(
                Projects,Projects.id == UserProjectAssignments.project_id,
            ).join(
                Users,Users.id == Projects.author_id,
            ).filter(
                UserProjectAssignments.user_id == user_id,
            ).all()
        return projects

class TicketTypes(Base):

    __tablename__ = 'tickettypes'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(Text)
    description = Column(Text)
    creation_datetime = Column(DateTime)
    
    @classmethod
    def add_ticket_type(cls, session, author_id, project_id, name, \
            description):
        """ Adds a new ticket type
        """
        with transaction.manager:
            ticket_type = cls(
                author_id = author_id,
                project_id = project_id,
                name = name,
                description = description,
                creation_datetime = datetime.datetime.now(),
            )
            session.add(ticket_type)
            transaction.commit()
        return ticket_type
    
    @classmethod
    def get_all_ticket_types(cls, session, project_id):
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
    def add_ticket_priority(cls, session, author_id, name, description, \
            weight, color):
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
    ticket_priority_id = Column(Integer, ForeignKey('ticketpriorities.id'))
    closed = Column(Boolean)
    closed_datetime = Column(DateTime, nullable=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_ticket(cls, session, author_id, project_id, ticket_type_id):
        """ Adds a new ticket to the system
        """
        with transaction.manager:
            ticket = cls(
                author_id = author_id,
                project_id = project_id,
                ticket_type_id = ticket_type_id,
                ticket_priority_id = ticket_priority_id,
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
                Tickets.ticket_id == ticket_id,
            ).first()
            session.add(ticket)
            transaction.commit()
        return ticket

class TicketContents(Base):

    __tablename__ = 'ticketcontents' 
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    title = Column(Text)
    contents = Column(Text)
    version = Column(Integer, autoincrement=True)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_ticket_content(cls, session, author_id, ticket_id, title, \
            contents):
        """ Add new ticket contents.  version numbers always increase.
        """
        with transaction.manager:
            ticket_contents = cls(
                author_id = author_id,
                ticket_id = ticket_id,
                title = title,
                contents = contents,
                #version = ,    # auto increment
                creation_datetime = datetime.datetime.now(),
            )
            session.add(ticket_contents)
            transaction.commit()
        return ticket_contents

    @classmethod
    def get_all_versions_by_ticket_id(cls, session, ticket_id):
        """ Get all versions of the ticket contents for ticket id.
        """
        with transaction.manager:
            ticket_contents = session.query(
                TicketContents,
            ).filter(
                TicketContents.ticket_id == ticket_id,
            ).all()
        return ticket_contents

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
    def add_ticket_comment(cls, session, authod_id, ticket_id, contents):
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

class RequirementTypes(Base):

    __tablename__ = 'requirementtypes'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(Text)
    description = Column(Text)

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

    @classmethod
    def get_requirement_types_by_project_id(cls, session, project_id):
        """ Get the requirement types for a project
        """

class Requirements(Base):

    __tablename__ = 'requirements'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    requirement_type_id = Column(Integer, ForeignKey('requirementtypes.id'))
    version = Column(Integer)
    removed = Column(Boolean)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_requirement(cls, session, author_id, project_id, \
            requirement_type_id):
        """ Adds a new requirement
        """

    @classmethod
    def remove_requirement(cls, session, requirement_id):
        """ Remove a requirement from a project (sets removed flag)
        """

    @classmethod
    def get_requirements_by_project_id(cls, session, project_id):
        """ Gets all of the requirements for a project
        """

    @classmethod
    def get_all_versions_by_requirement_id(cls, session, requirement_id):
        """ Returns all of the versions of the requirement
        """

class RequirementContents(Base):

    __tablename__ = 'requirementcontents'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    requirement_id = Column(Integer, ForeignKey('requirements.id')) 
    title = Column(Text)
    contents = Column(Text)
    version = Column(Integer)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_requirements_content(cls, session, requirement_id, title, \
            contents):
        """ Create a version of the contentents of a requirement.  Version
            numbers always increase.
        """

    @classmethod
    def get_all_versions_by_requirement_id(cls, session, requirement_id):
        """ Gets all version of a requirements contents by requirement id
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

        

