import json
from uuid import uuid4
import hashlib

from time import sleep
from random import randint
import datetime

import transaction

from sqlalchemy_utils import UUIDType
from sqlalchemy import (
    Column,
    #Date,
    ForeignKey,
    #Integer,
    #Float,
    Integer,
    UnicodeText,
    DateTime,
    #JSON,
    distinct,
    func,
    desc,
    #asc,
    #or_,
)

from .meta import Base

#def zeros(string, length):
#    for i in range(length-len(string)):
#        string = '0' + string
#    return string

class TimeStampMixin(object):
    creation_datetime = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    modified_datetime = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)


class CreationMixin():

    id = Column(UUIDType(binary=False), primary_key=True, unique=True)

    @classmethod
    def add(cls, dbsession, **kwargs):
        thing = cls(**kwargs)
        if thing.id is None:
            thing.id = str(uuid4())
        thing.creation_datetime = datetime.datetime.utcnow()
        thing.modified_datetime = datetime.datetime.utcnow()
        dbsession.add(thing)
        _thing = cls.get_by_id(dbsession, thing.id)
        return _thing

    @classmethod
    def get_all(cls, dbsession):
        things = []
        _things = dbsession.query(
            cls,
            Users,
        ).join(
            Users, Users.id == cls.author_id,
        ).order_by(
            desc(cls.creation_datetime),
        ).all()
        if _things:
            if not isinstance(things, list):
                _things = [_things]
            for _thing in things:
                thing = _thing[0]
                if hasattr(thing, 'creator'):
                    thing.creator = _thing[1]
                things.append(thing)
        return things

    @classmethod
    def get_paged(cls, dbsession, start=0, count=25):
        things = []
        _things = dbsession.query(
            cls,
            Users,
        ).join(
            Users, Users.id == cls.author_id,
        ).order_by(
            desc(cls.creation_datetime),
        ).slice(start, start+count).all()
        if _things:
            if not isinstance(things, list):
                _things = [_things]
            for _thing in _things:
                thing = _thing[0]
                if hasattr(thing, 'creator'):
                    thing.creator = _thing[1]
                things.append(thing)
        return things

    @classmethod
    def get_by_id(cls, dbsession, id):
        keys = set(cls.__dict__)
        if 'author_id' in keys:
            _thing = dbsession.query(
                cls,
                Users,
            ).outerjoin(
                Users, Users.id == cls.author_id,
            ).filter(
                cls.id == id,
            ).first()
            thing = _thing[0]
            if hasattr(thing, 'author'):
                thing.author = _thing[1]
        else:
            _thing = dbsession.query(
                cls,
                #Users,
            #).join(
            #    Users, Users.id == cls.author_id,
            ).filter(
                cls.id == id,
            ).first()
            thing = _thing
        return thing

    @classmethod
    def delete_by_id(cls, dbsession, _id):
        thing = cls.get_by_id(dbsession, _id)
        if thing is not None:
            dbsession.delete(thing)
        return thing

    @classmethod
    def update_by_id(cls, dbsession, _id, **kwargs):
        keys = set(cls.__dict__)
        thing = dbsession.query(cls).filter(cls.id==_id).first()
        _thing = None
        if thing is not None:
            for k in kwargs:
                if k in keys:
                    setattr(thing, k, kwargs[k])
            thing.modified_datetime = datetime.datetime.utcnow() 
            dbsession.add(thing)
            _thing = cls.get_by_id(dbsession, thing.id)
        return _thing

    def to_dict(self):
        return dict(
            id=str(self.id),
            creation_datetime=str(self.creation_datetime - datetime.timedelta(hours=4)),
            modified_datetime=str(self.modified_datetime - datetime.timedelta(hours=4)),
        )

class GetByMixin():

    @classmethod
    def get_by(cls, dbsession, params, start=0, count=25):
        _things = dbsession.query(
            cls,
            Users,
        ).join(
            Users, Users.id == cls.author_id,
        ).order_by(
            desc(cls.creation_datetime),
        )
        for param in params:
            _things = _things.filter(
                cls.__dict__[param] == params[param],
            )
        _things = _things.slice(start, start+count).all()
        things = []
        if hasattr(cls, 'creator'):
            for _thing in _things:
                thing = _thing[0]
                thing.creator = _thing[1]
                things.append(thing)
        else:
            things = _things
        return things

class Logs(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'logs'
    __single__ = 'Log'
    author_id = Column(ForeignKey('users.id'), nullable=False)
    entry_type = Column(UnicodeText, nullable=False)
    entry = Column(UnicodeText, nullable=False)

    creator = None

    def to_dict(self):
        resp = super(UserActions, self).to_dict()
        resp.update(
            entry=self.entry,
        )
        return resp


class Users(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'users'
    __single__ = 'User'
    organization_id = Column(ForeignKey('organizations.id'), nullable=False)
    first = Column(UnicodeText, nullable=False)
    last = Column(UnicodeText, nullable=False)
    phone = Column(UnicodeText, nullable=False)
    email = Column(UnicodeText, nullable=False)
    pass_salt = Column(UnicodeText, nullable=False)
    pass_hash = Column(UnicodeText, nullable=False)
    user_type = Column(UnicodeText, nullable=False) # system, admin, super user, user
    token = Column(UnicodeText, nullable=True)
    token_expire_datetime = Column(DateTime, nullable=True)
    must_change_password = Column(Integer, nullable=False)
    enabled = Column(Integer, nullable=False)
    last_login_datetime = Column(DateTime, nullable=True)
    deleted = Column(Integer, nullable=False)

    organization = None

    req = (
        'organization_id',
        'first',
        'last',
        'phone',
        'email',
        'password',
        'user_type',
        'enabled',
        'deleted',
    )

    @classmethod
    def _unpack(cls, _user):
        user = None
        if _user:
            user = _user[0]
            user.organization = _user[1]
        return user

    @classmethod
    def create_new_user(cls, dbsession, organization_id, first, last, phone, email, password, user_type, enabled, deleted=False):
        user = None
        salt_bytes = hashlib.sha256(str(uuid4()).encode('utf-8')).hexdigest()
        pass_bytes = hashlib.sha256(password.encode('utf-8')).hexdigest()
        pass_val = pass_bytes + salt_bytes
        pass_hash = hashlib.sha256(pass_val.encode('utf-8')).hexdigest()
        token = str(uuid4()) # generate a unique token
        # add user
        user = Users.add(
            dbsession=dbsession,
            organization_id=organization_id,
            first=first,
            last=last,
            phone=phone,
            email=email,
            pass_salt=salt_bytes,
            pass_hash=pass_hash,
            user_type=user_type,
            token=token,
            token_expire_datetime=None,
            enabled=enabled,
            must_change_password=0,
            last_login_datetime=None,
            deleted=False,
        )
        return user

    @classmethod
    def get_by_id(cls, dbsession, _id):
        _user = dbsession.query(
            Users,
            Organizations,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).filter(
            Users.id == _id,
        ).first()
        user = Users._unpack(_user)
        return user

    @classmethod
    def get_all(cls, dbsession):
        _users = dbsession.query(
            Users,
            Organizations,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).all()
        users = []
        if _users:
            for _user in _users:
                users.append(Users._unpack(_user))
        return users

    @classmethod
    def get_paged(cls, dbsession, start=0, count=25):
        _users = dbsession.query(
            Users,
            Organizations,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).slice(start, start+count)
        users = []
        if _users:
            for _user in _users:
                users.append(Users._unpack(_user))
        return users

    @classmethod
    def get_all_by_organization_id(cls, dbsession, organization_id):
        _users = dbsession.query(
            Users,
            Organizations,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).filter(
            Organizations.id == organization_id,
        ).all()
        users = []
        if _users:
            for _user in _users:
                users.append(Users._unpack(_user))
        return users

    @classmethod
    def get_by_token(cls, dbsession, token):
        _user = dbsession.query(
            Users,
            Organizations,
        ).filter(
            Users.token == token,
            Users.enabled == 1,
        ).first()
        user = Users._unpack(_user)
        return user

    @classmethod
    def get_by_email(cls, dbsession, email):
        _user = dbsession.query(
            Users,
            Organizations,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).filter(
            func.lower(Users.email) == email.lower(),
        ).first()
        user = Users._unpack(_user)
        return user


    @classmethod
    def get_by_user_type(cls, dbsession, user_type):
        _users = dbsession.query(
            Users,
            Organizations,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).filter(
            Users.user_type == user_type,
        ).all()
        users = []
        if _users:
            for _user in _users:
                users.append(Users._unpack(_user))
        return users

    @classmethod
    def build_pass_hash(cls, user, password):
        if isinstance(user.pass_salt, bytes):
            salt_bytes = user.pass_salt.decode('utf-8')
        elif isinstance(user.pass_salt, str):
            salt_bytes = user.pass_salt
        else:
            salt_bytes = user.pass_salt
        pass_bytes = hashlib.sha256(password.encode('utf-8')).hexdigest()
        pass_val = pass_bytes + salt_bytes
        pass_hash = hashlib.sha256(pass_val.encode('utf-8')).hexdigest()
        return pass_hash


    @classmethod
    def authenticate(cls, dbsession, email, password):
        _user = Users.get_by_email(dbsession, email)
        user = None
        if _user is not None:
            pass_hash = Users.build_pass_hash(_user, password)
            if (_user.pass_hash == pass_hash):
                token_expire_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=24*365*100)
                user = Users.update_by_id(
                    dbsession, 
                    _user.id,
                )
        return user


    @classmethod
    def validate_token(cls, token):
        user = Users.get_by_token(token)
        valid = False
        if user != None:
            if user.token_expire_datetime > datetime.datetime.utcnow()():
                valid = True
        return valid, user


    @classmethod
    def invalidate_token(cls, dbsession, token):
        user = Users.get_by_token(dbsession, token)
        if user != None:
            user = Users.update_by_id(
                dbsession,
                user.id,
                token=str(uuid4()),
                token_expire_datetime=datetime.datetime.utcnow() + datetime.timedelta(hours=24*365*100),
            )
        return user


    @classmethod
    def update_last_login(cls, dbsession, user):
        user.last_login_datetime = datetime.datetime.utcnow();
        dbsession.add(user)
        return user


    def to_dict(self, with_auth=False):
        resp = super(Users, self).to_dict()
        resp.update(
            first=self.first,
            last=self.last,
            phone=self.phone,
            email=self.email, 
            user_type=self.user_type,
            enabled=self.enabled,
            organization=self.organization.to_dict() if self.organization != None else None,
        )
        if with_auth:
            resp.update(
                token=self.token,
                token_expire_datetime=str(self.token_expire_datetime),
                must_change_password=self.must_change_password,
            )
        return resp


class NoteKudos(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'note_kudos'
    __single__ = 'Note Kudos'
    author_id = Column(ForeignKey('users.id'), nullable=False)
    notes_id = Column(ForeignKey('notes.id'), nullable=False)

    req = (
        #'author_id',
        'notes_id',
    )

    def to_dict(self):
        resp = super(NoteKudos, self).to_dict()
        resp.update(
            author_id=str(self.author_id),
            notes_id=str(notes_id),
        )
        return resp


class Notes(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'notes'
    __single__ = 'Note'
    author_id = Column(ForeignKey('users.id'), nullable=False)
    contents = Column(UnicodeText,nullable=False)

    task_id = Column(ForeignKey('tasks.id'), nullable=True)
    milestone_id = Column(ForeignKey('milestones.id'), nullable=True)

    author = None
    kudo_count = None

    req = (
        #'author_id',
        'contents',
        #'task_id',
        #'milestone_id',
    )

    @classmethod
    def _unpack(cls, _note):
        note = None
        if _note:
            note = _note[0]
            note.author = _note[1]
            note.kudo_count = _note[2]
        return note

    @classmethod
    def get_by_id(cls, dbsession, _id):
        _note = dbsession.query(
            Notes,
            Users,
            dbsession.query(
                func.count(distinct(NoteKudos.id)).label('kudo_count'),
            ).filter(
                NoteKudos.notes_id == Notes.id,
            ).label('kudo_count'),
        ).outerjoin(
            Users, Users.id == Notes.author_id,
        ).filter(
            Notes.id == _id,
        ).first()
        note = Notes._unpack(_note)
        return note

    @classmethod
    def get_all(cls, dbsession):
        _notes = dbsession.query(
            Notes,
            Users,
            dbsession.query(
                func.count(distinct(NoteKudos.id)).label('kudo_count'),
            ).filter(
                NoteKudos.notes_id == Notes.id,
            ).label('kudo_count'),
        ).outerjoin(
            Users, Users.id == Notes.author_id,
        ).all()
        notes= []
        if _notes:
            for _note in _notes:
                notes.append(Notes._unpack(_note))
        return notes

    @classmethod
    def get_paged(cls, dbsession, start, count):
        _note = dbsession.query(
            Notes,
            Users,
            dbsession.query(
                func.count(distinct(NoteKudos.id)).label('kudo_count'),
            ).filter(
                NoteKudos.notes_id == Notes.id,
            ).label('kudo_count'),
        ).outerjoin(
            Users, Users.id == Notes.author_id,
        ).slice(start, start+count)
        notes= []
        if _notes:
            for _note in _notes:
                notes.append(Notes._unpack(_note))
        return note

    @classmethod
    def get_by_organization_id(cls, dbsession, _id):
        _notes = dbsession.query(
            Notes,
            Users,
            dbsession.query(
                func.count(distinct(NoteKudos.id)).label('kudo_count'),
            ).filter(
                NoteKudos.notes_id == Notes.id,
            ).label('kudo_count'),
        ).outerjoin(
            Users, Users.id == Notes.author_id,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).filter(
            Organizations.id == _id,
        ).all()
        notes= []
        if _notes:
            for _note in _notes:
                notes.append(Notes._unpack(_note))
        return notes

    @classmethod
    def get_by_task_id(cls, dbsession, _id):
        _notes = dbsession.query(
            Notes,
            Users,
            dbsession.query(
                func.count(distinct(NoteKudos.id)).label('kudo_count'),
            ).filter(
                NoteKudos.notes_id == Notes.id,
            ).label('kudo_count'),
        ).outerjoin(
            Users, Users.id == Notes.author_id,
        ).outerjoin(
            Tasks, Tasks.id == Notes.task_id,
        ).filter(
            Tasks.id == _id,
        ).all()
        notes= []
        if _notes:
            for _note in _notes:
                notes.append(Notes._unpack(_note))
        return notes

    @classmethod
    def get_by_milestone_id(cls, dbsession, _id):
        _notes = dbsession.query(
            Notes,
            Users,
            dbsession.query(
                func.count(distinct(NoteKudos.id)).label('kudo_count'),
            ).filter(
                NoteKudos.notes_id == Notes.id,
            ).label('kudo_count'),
        ).outerjoin(
            Users, Users.id == Notes.author_id,
        ).outerjoin(
            MileStones, MileStones.id == Notes.milestone_id,
        ).filter(
            MileStones.id == _id,
        ).all()
        notes= []
        if _notes:
            for _note in _notes:
                notes.append(Notes._unpack(_note))
        return notes

    def to_dict(self):
        resp = super(Notes, self).to_dict()
        resp.update(
            author_id=str(self.author_id),
            author=self.author.to_dict() if self.author != None else None,
            contents=self.contents,
            task_id=str(self.task_id),
            milestone_id=str(self.milestone_id),
            kudo_count=self.kudo_count,
        )
        return resp


class Organizations(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'organizations'
    __single__ = 'Organization'
    #author_id = Column(UnicodeText, nullable=False)
    name = Column(UnicodeText,nullable=False)
    description = Column(UnicodeText, nullable=False)

    def to_dict(self):
        resp = super(Organizations, self).to_dict()
        resp.update(
            name=self.name,
            description=self.description,
        )
        return resp


class Tasks(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'tasks'
    __single__ = 'Task'
    author_id = Column(ForeignKey('users.id'), nullable=False)
    assignee_id = Column(ForeignKey('users.id'), nullable=True)
    project_id = Column(ForeignKey('projects.id'), nullable=False)
    #milestone_id = Column(ForeignKey('milestones.id'), nullable=True)
    title = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)
    priority = Column(Integer, nullable=False)
    due_datetime = Column(UnicodeText, nullable=True)
    complete = Column(Integer, nullable=False)
    completed_datetime = Column(DateTime, nullable=True)

    author = None
    assignee = None

    req = (
        #'author_id',
        'assignee_id',
        'project_id',
        #'milestone_id',
        'title',
        'description',
        'priority',
        #'due_datetime',
        'complete',
        #'completed_datetime',
        
    )

    @classmethod
    def _unpack(cls, _task):
        task = None
        if _task:
            task = _task[0]
            task.author = _task[1]
        return task

    @classmethod
    def get_by_id(cls, dbsession, _id):
        _task = dbsession.query(
            Tasks,
            Users,
        ).outerjoin(
            Users, Users.id == Tasks.author_id,
        ).filter(
            Tasks.id == _id,
        ).first()
        task = Tasks._unpack(_task)
        return task

    @classmethod
    def get_all(cls, dbsession):
        _tasks = dbsession.query(
            Tasks,
            Users,
        ).outerjoin(
            Users, Users.id == Tasks.author_id,
        ).all()
        tasks= []
        if _tasks:
            for _task in _tasks:
                tasks.append(Tasks._unpack(_task))
        return tasks

    @classmethod
    def get_paged(cls, dbsession, start, count):
        _task = dbsession.query(
            Tasks,
            Users,
        ).outerjoin(
            Users, Users.id == Tasks.author_id,
        ).slice(start, start+count)
        tasks= []
        if _tasks:
            for _task in _tasks:
                tasks.append(Tasks._unpack(_task))
        return task

    @classmethod
    def get_by_organization_id(cls, dbsession, _id):
        _tasks = dbsession.query(
            Tasks,
            Users,
        ).outerjoin(
            Users, Users.id == Tasks.author_id,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).filter(
            Organizations.id == _id,
        ).all()
        tasks= []
        if _tasks:
            for _task in _tasks:
                tasks.append(Tasks._unpack(_task))
        return tasks

    '''
    @classmethod
    def get_by_milestone_id(cls, dbsession, _id):
        _tasks = dbsession.query(
            Tasks,
            Users,
        ).outerjoin(
            Users, Users.id == Tasks.author_id,
        ).outerjoin(
            MileStones, MileStones.id == Tasks.milestone_id,
        ).filter(
            MileStones.id == _id,
        ).all()
        tasks= []
        if _tasks:
            for _task in _tasks:
                tasks.append(Tasks._unpack(_task))
        return tasks
    '''

    @classmethod
    def get_by_project_id(cls, dbsession, _id):
        _tasks = dbsession.query(
            Tasks,
            Users,
        ).outerjoin(
            Users, Users.id == Tasks.author_id,
        ).outerjoin(
            Projects, Projects.id == Tasks.project_id,
        ).filter(
            Projects.id == _id,
        ).all()
        tasks= []
        if _tasks:
            for _task in _tasks:
                tasks.append(Tasks._unpack(_task))
        return tasks

    def to_dict(self):
        resp = super(Tasks, self).to_dict()
        resp.update(
            author_id=str(self.author_id),
            author=self.author.to_dict() if self.author != None else None,
            assignee_id=str(self.assignee_id),
            assignee=self.assignee.to_dict() if self.assignee != None else None,
            project_id=str(self.project_id),
            #milestone_id=str(self.milestone_id),
            title=self.title,
            description=self.description,
            priority=self.priority,
            due_datetime=str(self.due_datetime),
            complete=self.complete,
            completed_datetime=str(self.completed_datetime),
        )
        return resp


class MileStones(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'milestones'
    __single__ = 'MileStone'
    author_id = Column(ForeignKey('users.id'), nullable=False)
    project_id = Column(ForeignKey('projects.id'), nullable=False)
    title = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)
    due_datetime = Column(DateTime, nullable=False)
    complete = Column(Integer, nullable=False)

    author = None

    req = (
        #'author_id',
        'project_id',
        'title',
        'description',
        'due_datetime',
        'complete',
    )

    @classmethod
    def _unpack(cls, _milestone):
        milestone = None
        if _milestone:
            milestone = _milestone[0]
            milestone.author = _milestone[1]
        return milestone

    @classmethod
    def get_by_id(cls, dbsession, _id):
        _milestone = dbsession.query(
            MileStones,
            Users,
        ).outerjoin(
            Users, Users.id == MileStones.author_id,
        ).filter(
            MileStones.id == _id,
        ).first()
        milestone = MileStones._unpack(_milestone)
        return milestone

    @classmethod
    def get_all(cls, dbsession):
        _MileStones = dbsession.query(
            MileStones,
            Users,
        ).outerjoin(
            Users, Users.id == MileStones.author_id,
        ).all()
        MileStones= []
        if _MileStones:
            for _milestone in _MileStones:
                MileStones.append(MileStones._unpack(_milestone))
        return MileStones

    @classmethod
    def get_paged(cls, dbsession, start, count):
        _milestone = dbsession.query(
            MileStones,
            Users,
        ).outerjoin(
            Users, Users.id == MileStones.author_id,
        ).slice(start, start+count)
        MileStones= []
        if _MileStones:
            for _milestone in _MileStones:
                MileStones.append(MileStones._unpack(_milestone))
        return milestone

    @classmethod
    def get_by_organization_id(cls, dbsession, _id):
        _MileStones = dbsession.query(
            MileStones,
            Users,
        ).outerjoin(
            Users, Users.id == MileStones.author_id,
        ).outerjoin(
            Organizations, Organizations.id == Users.organization_id,
        ).filter(
            Organizations.id == _id,
        ).all()
        MileStones= []
        if _MileStones:
            for _milestone in _MileStones:
                MileStones.append(MileStones._unpack(_milestone))
        return MileStones

    @classmethod
    def get_by_project_id(cls, dbsession, _id):
        _MileStones = dbsession.query(
            MileStones,
            Users,
        ).outerjoin(
            Users, Users.id == MileStones.author_id,
        ).outerjoin(
            Projects, Projects.id == Users.project_id,
        ).filter(
            Projects.id == _id,
        ).all()
        MileStones= []
        if _MileStones:
            for _milestone in _MileStones:
                MileStones.append(MileStones._unpack(_milestone))
        return MileStones

    def to_dict(self):
        resp = super(Organizations, self).to_dict()
        resp.update(
            author_id=str(self.author_id),
            author=self.author.to_dict() if self.author != None else None,
            title=self.title,
            description=self.description,
            due_datetime=str(self.due_datetime),
            complete=self.complete,
        )
        return resp


class Projects(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'projects'
    __single__ = 'Project'
    author_id = Column(ForeignKey('users.id'), nullable=False)
    title = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)
    color = Column(UnicodeText, nullable=False)
    closed = Column(Integer, nullable=False)

    author = None

    req = (
        #'author_id',
        'title',
        'description',
        'color',
        'closed',
    )

    @classmethod
    def _unpack(cls, _project):
        project = None
        if _project:
            project = _project[0]
            project.author = _project[1]
        return project

    @classmethod
    def get_by_id(cls, dbsession, _id):
        _project = dbsession.query(
            Projects,
            Users,
        ).outerjoin(
            Users, Users.id == Projects.author_id,
        ).filter(
            Projects.id == _id,
        ).first()
        return Projects._unpack(_project)

    def to_dict(self):
        resp = super(Projects, self).to_dict()
        resp.update(
            author_id=str(self.author_id),
            author=self.author.to_dict() if self.author != None else None,
            title=self.title,
            description=self.description,
            color=self.color,
            closed=self.closed,
        )
        return resp


class Settings(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'settings'
    __single__ = 'Setting'
    setting_type = Column(UnicodeText, nullable=False)
    name = Column(UnicodeText, nullable=False)
    value = Column(UnicodeText, nullable=False)
    data_type = Column(UnicodeText, nullable=False)
    meta = Column(UnicodeText, nullable=False)

    req = (
        'setting_type',
        'name',
        'value',
        'data_type',
        'meta',
    )

    def to_dict(self):
        resp = super(Settings, self).to_dict()
        resp.update(
            setting_type=self.setting_type,
            name=self.name,
            value=self.value,
            data_type=self.data_type,
            meta=self.meta,
        )
        return resp
