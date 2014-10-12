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
    
class Tickets(Base):

    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    title = Column(Text)
    contents = Column(Text)
    closed = Column(Boolean)
    creation_datetime = Column(DateTime)
    

    @classmethod
    def add_ticket(cls, session, author_id, title, contents):
        """ Adds a new ticket to the system
        """
        
    @classmethod
    def close_ticket(cls, session, ticket_id):
        """ Sets a ticket's status to closed
        """

class TicketComments(Base):

    __tablename__ = 'ticketcomments'
    author_id = Column(Integer, ForeignKey('users.id'))    
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    contents = Column(Text)
    creation_datetime = Column(DateTime)
    
    @classmethod
    def add_ticket_comment(cls, session, authod_id, ticket_id, contents):
        """ Adds a comment to a ticket
        """
        
    