
#import json
#import uuid
#import hashlib
#import os

from pyramid.view import (
    view_defaults,
    view_config,
)

from ..utils import (
    validate_uuid4,
    validate_date,
    save_file, 
    BaseRequest,
)

import transaction

from ..models import (
    NoteKudos,
    Notes,
    Tasks,
    MileStones,
    Organizations,
    Projects,
    Settings,
)

@view_defaults(route_name='/api/v1/note_kudos', renderer='json')
class NoteKudosAPI(BaseRequest):
    
    cls = NoteKudos

    def __init__(self, request):
        super(NoteKudosAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        resp = []
        with transaction.manager:
            resp = self._get_collection()
        return resp

    @view_config(request_method='POST')
    def post(self):
        with transaction.manager:
            resp = self._post()
        return resp


@view_defaults(route_name='/api/v1/note_kudos/{id}', renderer='json')
class NoteKudoAPI(BaseRequest):

    cls = NoteKudos

    def __init__(self, request):
        super(NoteKudoAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get()
        return resp

    @view_config(request_method='PUT')
    def put(self):
        with transaction.manager:
            resp = self._put()
        return resp

    @view_config(request_method='DELETE')
    def delete(self):
        with transaction.manager:
            resp = self._delete()
        return resp


@view_defaults(route_name='/api/v1/notes', renderer='json')
class NotesAPI(BaseRequest):
    
    cls = Notes

    def __init__(self, request):
        super(NotesAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            if 'task_id' in self.request.GET:
                resp = {}
                task_id = self.request.GET['task_id']
                if validate_uuid4(task_id):
                    _notes = self.cls.get_by_task_id(
                        dbsession=self.request.dbsession,
                        _id=task_id,
                    )
                    if _notes:
                        resp = [n.to_dict() for n in _notes]
                    #else:
                    #    self.request.response.status = 400 # 404 here?    
                else:
                    self.request.response.status = 400
            elif 'milestone_id' in self.request.GET:
                resp = {}
                milestone_id = self.request.GET['milestone_id']
                if validate_uuid4(milestone_id):
                    _notes = self.cls.get_by_milestone_id(
                        dbsession=self.request.dbsession,
                        _id=milestone_id,
                    )
                    if _notes:
                        resp = [n.to_dict() for n in _notes]
                    #else:
                    #    self.request.response.status = 400 # 404 here?    
                else:
                    self.request.response.status = 400
            else:
                resp = self._get_collection()
        return resp

    @view_config(request_method='POST')
    def post(self):
        with transaction.manager:
            resp = self._post()
        return resp


@view_defaults(route_name='/api/v1/notes/{id}', renderer='json')
class NoteAPI(BaseRequest):

    cls = Notes

    def __init__(self, request):
        super(NoteAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get()
        return resp

    @view_config(request_method='PUT')
    def put(self):
        with transaction.manager:
            resp = self._put()
        return resp

    @view_config(request_method='DELETE')
    def delete(self):
        with transaction.manager:
            resp = self._delete()
        return resp


@view_defaults(route_name='/api/v1/organizations', renderer='json')
class OrganizationsAPI(BaseRequest):
    
    cls = Organizations

    def __init__(self, request):
        super(OrganizationsAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get_collection()
        return resp

    @view_config(request_method='POST')
    def post(self):
        with transaction.manager:
            resp = self._post()
        return resp


@view_defaults(route_name='/api/v1/organizations/{id}', renderer='json')
class OrganizationAPI(BaseRequest):

    cls = Organizations

    def __init__(self, request):
        super(OrganizationAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get()
        return resp

    @view_config(request_method='PUT')
    def put(self):
        with transaction.manager:
            resp = self._put()
        return resp

    @view_config(request_method='DELETE')
    def delete(self):
        with transaction.manager:
            resp = self._delete()
        return resp


@view_defaults(route_name='/api/v1/tasks', renderer='json')
class TasksAPI(BaseRequest):
    
    cls = Tasks

    def __init__(self, request):
        super(TasksAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        resp = []
        with transaction.manager:
            if 'milestone_id' in self.request.GET:
                milestone_id = self.request.GET['milestone_id']
                if validate_uuid4(milestone_id):
                    _notes = self.cls.get_by_milestone_id(
                        dbsession=self.request.dbsession,
                        _id=milestone_id,
                    )
                    if _notes:
                        resp = [n.to_dict() for n in _notes]
                    #else:
                    #    self.request.response.status = 400 # 404 here?    
                else:
                    self.request.response.status = 400
            elif 'project_id' in self.request.GET:
                project_id = self.request.GET['project_id']
                if validate_uuid4(project_id):
                    _notes = self.cls.get_by_project_id(
                        dbsession=self.request.dbsession,
                        _id=project_id,
                    )
                    if _notes:
                        resp = [n.to_dict() for n in _notes]
                    #else:
                    #    self.request.response.status = 400 # 404 here?    
                else:
                    self.request.response.status = 400
            else:
                resp = self._get_collection()
        return resp

    @view_config(request_method='POST')
    def post(self):
        with transaction.manager:
            resp = self._post()
        return resp


@view_defaults(route_name='/api/v1/tasks/{id}', renderer='json')
class TaskAPI(BaseRequest):

    cls = Tasks

    def __init__(self, request):
        super(TaskAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get()
        return resp

    @view_config(request_method='PUT')
    def put(self):
        with transaction.manager:
            resp = self._put()
        return resp

    @view_config(request_method='DELETE')
    def delete(self):
        with transaction.manager:
            resp = self._delete()
        return resp


@view_defaults(route_name='/api/v1/milestones', renderer='json')
class MileStonesAPI(BaseRequest):
    
    cls = MileStones

    def __init__(self, request):
        super(MileStonesAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            if 'project_id' in self.request.GET:
                resp = {}
                project_id = self.request.GET['project_id']
                if validate_uuid4(project_id):
                    _notes = cls.get_by_project_id(
                        dbsession=self.request.dbsession,
                        _id=project_id,
                    )
                    if _notes:
                        resp = [n.to_dict() for n in _notes]
                    else:
                        self.request.response.status = 400 # 404 here?    
                else:
                    self.request.response.status = 400
            else:
                resp = self._get_collection()
            resp = self._get_collection()
        return resp

    @view_config(request_method='POST')
    def post(self):
        with transaction.manager:
            resp = self._post()
        return resp


@view_defaults(route_name='/api/v1/milestones/{id}', renderer='json')
class MileStoneAPI(BaseRequest):

    cls = MileStones

    def __init__(self, request):
        super(MileStoneAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get()
        return resp

    @view_config(request_method='PUT')
    def put(self):
        with transaction.manager:
            resp = self._put()
        return resp

    @view_config(request_method='DELETE')
    def delete(self):
        with transaction.manager:
            resp = self._delete()
        return resp


@view_defaults(route_name='/api/v1/projects', renderer='json')
class ProjectsAPI(BaseRequest):
    
    cls = Projects

    def __init__(self, request):
        super(ProjectsAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get_collection()
        return resp

    @view_config(request_method='POST')
    def post(self):
        with transaction.manager:
            resp = self._post()
        return resp


@view_defaults(route_name='/api/v1/projects/{id}', renderer='json')
class ProjectAPI(BaseRequest):

    cls = Projects

    def __init__(self, request):
        super(ProjectAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get()
        return resp

    @view_config(request_method='PUT')
    def put(self):
        with transaction.manager:
            resp = self._put()
        return resp

    @view_config(request_method='DELETE')
    def delete(self):
        with transaction.manager:
            resp = self._delete()
        return resp


@view_defaults(route_name='/api/v1/settings', renderer='json')
class SettingsAPI(BaseRequest):
    
    cls = Settings

    def __init__(self, request):
        super(ProjectAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get_collection()
        return resp

    @view_config(request_method='POST')
    def post(self):
        with transaction.manager:
            resp = self._post()
        return resp


@view_defaults(route_name='/api/v1/settings/{id}', renderer='json')
class SettingAPI(BaseRequest):

    cls = Settings

    def __init__(self, request):
        super(SettingAPI, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        with transaction.manager:
            resp = self._get()
        return resp

    @view_config(request_method='PUT')
    def put(self):
        with transaction.manager:
            resp = self._put()
        return resp

    @view_config(request_method='DELETE')
    def delete(self):
        with transaction.manager:
            resp = self._delete()
        return resp

