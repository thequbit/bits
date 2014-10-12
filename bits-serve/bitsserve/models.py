from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


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

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_type_id = Column(Integer, ForeignKey('usertypes.id')
    first = Column(Text)
    last = Column(Text)
    email = Column(Text)
    username = Column(Text)
    passhash = Column(Text)
    passsalt = Column(Text)
    disabled = Column(Boolean)   
    creation_datetime = Column(DateTime)
 
    @classmethod
    def add_user(cls, session, user_type, first, last, email, password):
        """ Adds a new user to the database.  Generates a salt and hashes the 
            password concatendated with that salt.  Also must decode the
            user_type field into a user_type_id
        """
        
    @classmethod
    def disable_user(cls, session):
        """
        """

class Organizations(Base):

    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    creation_datetime = Column(DateTime)
    
    @classmethod
    def add_organization(cls, session):
        """ Adds a new organization from a user
        """

class Projects(Base):

    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    organization_id = Column(Integer, ForeignKey('projects.id'))
    creation_datetime = Column(DateTime)
    disabled = Column(Boolean)
    
    @classmethod
    def add_project(cls, session, name, author_id, organization_id):
        """ Adds a new project from a user, and connected to an organization
        """
        
    @classmethod
    def disable_project(cls, session, project_id):
        """ Disables a project
        """
    
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
    
    @classmethod
    def get_all_ticket_types(cls, session, project_id):
        """ Returns all of the ticket types for the project
        """
    
class TicketPriorities(Base):

    __tablename__ = 'ticketpriorities'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, FreignKey('projects.id'))
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
                
                name = name,
                description = description,
                weight = weight,
                color = color,
            )
        return ticket_priority

    @classmethod
    def get_ticket_priorities_by_project_id(cls, session, project_id):
        """ Returns the list of ticket priorities for a project.
        """

class Tickets(Base):

    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    ticket_type_id = Column(Integer, ForeignKey('tickettypes.id'))
    closed = Column(Boolean)
    closed_datetime = Column(DateTime)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_ticket(cls, session, author_id, title, contents):
        """ Adds a new ticket to the system
        """
        
    @classmethod
    def close_ticket(cls, session, ticket_id):
        """ Sets a ticket's status to closed
        """

class TicketContents(Base):

    """
    """

    __tablename__ = 'ticketcontents' 
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    title = Column(Text)
    contents = Column(Text)
    version = Column(Integer)
    creation_datetime = Column(DateTime)

    @classmethod
    def add_ticket_content(cls, session, author_id, ticket_id, title, \
            contents):

        """ Add new ticket contents.  version numbers always increase.
        """

    @classmethod
    def get_all_versions_by_ticket_id(cls, session, ticket_id):
        """ Get all versions of the ticket contents for ticket id.
        """

class TicketComments(Base):

    __tablename__ = 'ticketcomments'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))    
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    contents = Column(Text)
    update_datetime = Column(DateTime, nullable=True)
    flagged = Column(Boolean)
    creation_datetime = Column(DateTime)
    
    @classmethod
    def add_ticket_comment(cls, session, authod_id, ticket_id, contents):
        """ Adds a comment to a ticket
        """

    @classmethod
    def update_ticket_comment(cls, session, ticket_comment_id, content):
        """ Updates the content of a ticket comment
        """

    @classmethod
    def flag_ticket_comment(cls, session, ticket_comment_id):
        """ Flaggs a ticket comment
        """

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

    @class method
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


        

