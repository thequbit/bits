
var baseEndPoint = {

	_get: function(url, callback) {
		return $.get(
			url,
			function(resp) {
				if ( typeof(callback) == 'function' ) {
					callback(resp);
				}
			}
		);
	},

	_post: function(url, payload, callback) {
		return $.post(
			url,
			JSON.stringify(payload),
			function(resp) {
				if ( typeof(callback) == 'function' ) {
					callback(resp);
				}
			}
		);
	},

	_put: function(url, payload, callback) {
		return $.ajax({ //$.put(
			url: url,
			method: 'PUT',
			data: JSON.stringify(payload),
			success: function(resp) {
				if ( typeof(callback) == 'function' ) {
					callback(resp);
				}
			}
		});
	},

	_delete: function(url, callback) {
		return $.ajax({
			url: url,
			type: 'DELETE',
			success: function(resp) {
				if ( typeof(callback) == 'function' ) {
					callback(resp);
				}
			}
		});
	}

}

var EndPoint = function(name) {

	this._url = '/api/v1/' + name;

	this.get_by = function(params, callback) {
		var url = this._url + '?';
		for( var key in params ) {
			url += '' + key + '=' + params[key] + '&';
		}
		return baseEndPoint._get(url, callback);
	}

	this.get_by_id = function(id, callback) {
		return baseEndPoint._get(this._url + '/' + id, callback);
	},

	this.get_collection = function(callback) {
		return baseEndPoint._get(this._url, callback);
	},

	this.create = function(payload, callback) {
		return baseEndPoint._post(this._url, payload, callback);
	},

	this.update = function(id, payload, callback) {
		///console.log('EndPoint.update(), payload: ', payload);
		delete payload['id']
		delete payload['creation_datetime']
		delete payload['modified_datetime']
		return baseEndPoint._put(this._url + '/' + id, payload, callback);
	},

	this.delete = function(id, callback) {
		return baseEndPoint._delete(this._url + '/' + id, callback);
	}

	return true;
}

var API = function() {

	this.users = new EndPoint('users');
	this.users.get_all_by_organization_id = function(organization_id, callback) {
		var url = '/api/v1/users?organization_id=' + organization_id;
		$.get(
			url,
			function(users) {
				if ( typeof(callback) == 'function' ) {
					callback(users);
				}
			}
		);
	};

	this.note_kudos = new EndPoint('note_kudos');

	this.notes = new EndPoint('notes');
	this.notes.get_by_task_id = function(task_id, callback) {
		var url = '/api/v1/notes?task_id=' + task_id;
		$.get(
			url,
			function(notes) {
				if ( typeof(callback) == 'function' ) {
					callback(notes);
				}
			}
		);
	};

	this.organizations = new EndPoint('organizations');

	this.tasks = new EndPoint('tasks');
	this.tasks.get_all_by_project_id = function(project_id, callback) {
		var url = '/api/v1/tasks?project_id=' + project_id;
		return $.get(
			url,
			function(tasks) {
				if ( typeof(callback) == 'function' ) {
					callback(tasks);
				}
			}
		);
	}

	this.milestones = new EndPoint('milestones');

	this.projects = new EndPoint('projects');

	this.settings = new EndPoint('settings');

}
