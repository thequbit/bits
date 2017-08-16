
var Site = function() {



	this.load_projects = function() {

		var that = this;

		api.projects.get_collection(function(projects) {
			var html = '';
			if ( projects.length == 0 ) {
				html += '<i>No Projects Found</i>';
			}
			else {
				for(var i=0;i<projects.length;i++) {
					html += '<div id="' + projects[i].id + '-project" class="entity-container" style="background: ' + projects[i].color + ';">';
					html += '' + projects[i].title;
					html += '</div>';
				}
			}

			$('#page-projects-contents').html(html);

			for(var i=0;i<projects.length;i++) {
				var project = projects[i];
				$('#' + project.id + '-project').off('click');
				$('#' + project.id + '-project').on('click', function() {
					that.display_page('project', false, project.id)
				});
			}

		});
	};

	this.load_new_project = function() {

		var that = this;

		$('#page-new-project-create').off('click');
		$('#page-new-project-create').on('click', function() {
			
			console.log('creating new project ... ');

			var payload = {
				title: $('#page-new-project-title').val(),
				description: $('#page-new-project-description').val(),
				color: $('#page-new-project-color').val(),
				closed: false
			};
			api.projects.create(payload, function(project) {
				//alert("Project created successfully.");
				that.display_page('projects', false);
			});
		});

	};

	this.load_project = function() {

		var that = this;

		var id = utils.get_params()['id'];

		if ( typeof(id) == 'undefined' )
			that.display_page('projects');

		api.projects.get_by_id(id, function(project) {

			$('#page-project-bread-crumbs').html(project.title);

			var html = '';
			html += '<h3><b>' + project.title + '</b></h3>'
			html += '<p>';
			html += '<div id="' + project.id + '-project-description" class="entity-description">';
			html += '<b>' + project.author.first + ' ' + project.author.last + '</b>';
			html += '<i class="right">' + project.modified_datetime.split('.')[0] + '</i>';
			html += '<div class="indent">'
			html += project.description;
			html += '</div>';
			html += '</div>';
			html += '</p>';
			html += '<a class="button right" href="/#/new-task?project_id=' + project.id + '&project_title=' + encodeURIComponent(project.title) + '">New Task</a>';
			html += '<h3>Tasks:</h3>'
			html += '<div id="page-project-tasks">'
			html += '    <center><img src="/static/media/loading.gif"></img></center>';
			html += '</div>';
			$('#page-project-contents').html(html);

			api.tasks.get_all_by_project_id(project.id, function(tasks) {
				var html = '';
				html += '<div class="indent">';
				if ( tasks.length == 0 ) {
					html += '<i>No Tasks Found</i>';
				}
				for(var i=0;i<tasks.length;i++) {
					var task_location = '/#/task?id=' + tasks[i].id + '&project_id=' + project.id + '&project_title=' + project.title;
					html += '<div id="' + tasks[i].id + '-task" class="entity-container" onclick="window.location=\'' + task_location + '\';">';
					html += tasks[i].title;
					html += '</div>';
				}
				html += '</div>';
				$('#page-project-tasks').html(html);
			});

			function setup_edit_project() {

				$('.entity-description').off('click');
				$('.entity-description').on('click', function() {
					console.log('entity-description');
					$('.entity-description').off('click');
					//var id = $(this).prop('id').split('-project-description')[0];
					var html = '';
					html += '<h4>Edit Project:</h4>';
					html += '<textarea id="' + project.id + '-edit-project" rows="6">';
					html += project.description;
					html += '</textarea>';
					html += '<a id="page-project-submit-edit-project" class="button right">Update</a>';
					html += '<a id="page-project-cancel-edit-project" class="button">Cancel</a>';
					$('#' + project.id + '-project-description').html(html);
					
					$('#page-project-cancel-edit-project').off('click');
					$('#page-project-cancel-edit-project').on('click', function() {
						
						var html = '';
						html += '<b>' + project.author.first + ' ' + project.author.last + '</b>';
						html += '<i class="right">' + project.modified_datetime.split('.')[0] + '</i>';
						html += '<div class="indent">'
						html += project.description;
						html += '</div>';
						$('#' + project.id + '-project-description').html(html);
						///// MEGA MOTHER FUCKING HACK BITCHES /////
						window.setTimeout( function() {
							setup_edit_task();
							}, 
							500
						);
					});

					$('#page-project-submit-edit-project').off('click');
					$('#page-project-submit-edit-project').on('click', function() {
						var pyaload = {
							title: project.title,
							description: $('#' + id + '-edit-project').val()
						};
						api.projects.update(id, pyaload, function(_project) {
							var html = '';
							html += '<b>' + _project.author.first + ' ' + _project.author.last + '</b>';
							html += '<i class="right">' + _project.modified_datetime.split('.')[0] + '</i>';
							html += '<div class="indent">'
							html += _project.description;
							html += '</div>';
							$('#' + project.id + '-project-description').html(html);
							///// MEGA MOTHER FUCKING HACK BITCHES /////
							window.setTimeout( function() {
								setup_edit_task();
								}, 
								500
							);
						});
					});

				});

			}

			auth.is_logged_in( function(logged_in, _user) {
				//console.log(_user.id, project.author.id, _user.id == project.author.id);
				if ( logged_in && _user.id == project.author.id )	
					setup_edit_project();
			});

		});

	};

	this.load_new_task = function() {
		
		//console.log('Site.load_new_task()');

		var that = this;

		var project_id = utils.get_params()['project_id'];
		var project_title = utils.get_params()['project_title'];
		var crumb_html = '<a src="/#/project?project_id=' + project_id + '">' + decodeURIComponent(project_title) + '</a> &gt; New Task';
		$('#page-new-task-bread-crumbs').html(crumb_html);

		$('#page-new-task-create').off('click');
		$('#page-new-task-create').on('click', function() {
			console.log('page-new-task-create');
			var payload = {
				assignee_id: $('#page-new-task-assignee').val(),
				project_id: project_id,
				title: $('#page-new-task-title').val(),
				description: $('#page-new-task-description').val(),
				priority: $('#page-new-task-priority').val(),
				due_datetime: $('#page-new-task-due_datetime').val(),
				complete: false
			};
			api.tasks.create(payload, function(task) {
				//alert('Task created successfully.');
				//that.display_page('task', false, task.id);
				window.location = '/#/task?id=' + task.id + '&project_title=' + project_title;
			});
		});

		auth.is_logged_in( function(logged_in, _user) {
			if( logged_in ) {
				api.users.get_all_by_organization_id(_user.organization_id, function(users) {
					var html = '';
					for(var i=0;i<users.length;i++) {
						var user = users[i];
						html += '<option value="' + user.id + '">' + user.first + ' ' + user.last + '</option>';
					}
					$('#page-new-task-assignee').html(html);
				});
			}
		});

	};

	this.load_task = function() {
		
		var that = this;
		var id = utils.get_params()['id'];
		var project_id = utils.get_params()['project_id'];
		var project_title = utils.get_params()['project_title'];

		api.tasks.get_by_id(id, function(task) {
			
			var crumb_html = '';
			crumb_html += '<a href="/#/project?id=' + project_id + '">';
			crumb_html += decodeURIComponent(project_title);
			crumb_html += '</a> &gt; ';
			crumb_html += '' + task.title;
			$('#page-task-bread-crumbs').html(crumb_html);

			$('#page-task-title').html(task.title);

			var html = '';
			html += '<p>';
			html += '<div id="' + task.id + '-task-description" class="entity-description">';// + task.description + '</div></p>'
			html += '<b>' + task.author.first + ' ' + task.author.last + '</b>';
			html += '<i class="right">' + task.modified_datetime.split('.')[0] + '</i>';
			html += '<div class="indent">'
			html += task.description;
			html += '</div>';
			html += '</div>';
			html += '</p>';
			html += '<h3>Notes:</h3>';
			html += '<div id="page-task-notes"></div>';
			html += '</br>';
			html += '<textarea id="page-task-new-note-contents" rows="6">'
			html += '</textarea>'
			html += '<a id="page-task-post-note" class="button right">Post Note</a>';
			html += '<div id="page-task-post-note-spinner"></div>';
			$('#page-task-contents').html(html);

			function setup_edit_task() {

				$('.entity-description').off('click');
				$('.entity-description').on('click', function() {
					$('.entity-description').off('click');
					var id = $(this).prop('id').split('-task-description')[0];
					var html = '';
					html += '<h4>Edit Task:</h4>';
					html += '<textarea id="' + task.id + '-edit-task" rows="6">';
					html += task.description;
					html += '</textarea>';
					html += '<a id="page-task-submit-edit-task" class="button right">Update</a>';
					html += '<a id="page-task-cancel-edit-task" class="button">Cancel</a>';
					$('#' + id + '-task-description').html(html);
					
					$('#page-task-cancel-edit-task').off('click');
					$('#page-task-cancel-edit-task').on('click', function() {
						
						var html = '';
						html += '<b>' + task.author.first + ' ' + task.author.last + '</b>';
						html += '<i class="right">' + task.modified_datetime.split('.')[0] + '</i>';
						html += '<div class="indent">'
						html += task.description;
						html += '</div>';
						$('#' + id + '-task-description').html(html);
						///// MEGA MOTHER FUCKING HACK BITCHES /////
						window.setTimeout( function() {
							setup_edit_task();
							}, 
							500
						);
					});

					$('#page-task-submit-edit-task').off('click');
					$('#page-task-submit-edit-task').on('click', function() {
						var pyaload = {
							title: task.title,
							description: $('#' + id + '-edit-task').val()
						};
						api.tasks.update(id, pyaload, function(_task) {
							var html = '';
							html += '<b>' + _task.author.first + ' ' + _task.author.last + '</b>';
							html += '<i class="right">' + _task.modified_datetime.split('.')[0] + '</i>';
							html += '<div class="indent">'
							html += _task.description;
							html += '</div>';
							$('#' + id + '-task-description').html(html);
							///// MEGA MOTHER FUCKING HACK BITCHES /////
							window.setTimeout( function() {
								setup_edit_task();
								}, 
								500
							);
						});
					});

				});

			}

			auth.is_logged_in( function(logged_in, _user) {
				//console.log(_user.id, task.author.id, _user.id == task.author.id);
				if ( logged_in && _user.id == task.author.id )	
					setup_edit_task();
			});

			api.notes.get_by_task_id(id, function(notes) {
				var html = '';
				if ( notes.length == 0 ) {
					html += '<i>No Notes Found</i>';
				}
				for(var i=0; i<notes.length;i++) {
					html += '<div id="' + notes[i].id + '-note" class="entity-container task-note">';
					html += '<b>' + notes[i].author.first + ' ' + notes[i].author.last + '</b>';
					html += '<i class="right">' + notes[i].modified_datetime.split('.')[0] + '</i>';
					html += '<div class="indent">'
					html += notes[i].contents;
					html += '</div>';
					html += '</div>';
				}
				$('#page-task-notes').html(html);

				$('#page-task-post-note').off('click');
				$('#page-task-post-note').on('click', function() {
					$('#page-task-post-note-spinner').html('Please wait ... ');
					var payload = {
						contents: $('#page-task-new-note-contents').val(),
						task_id: id,
					}
					api.notes.create(payload, function(_note) {
						var html = '';
						html += '<div id="' + _note.id + '-note" class="entity-container task-note">';
						html += '<b>' + _note.author.first + ' ' + _note.author.last + '</b>';
						html += '<i class="right">' + _note.modified_datetime.split('.')[0] + '</i>';
						html += '<div class="indent">'
						html += _note.contents;
						html += '</div>';
						html += '</div>';
						$('#page-task-notes').html($('#page-task-notes').html() + html);
						///// MEGA MOTHER FUCKING HACK BITCHES /////
						window.setTimeout( function() {
							setup_edit_note();
							}, 
							500
						);
						$('#page-task-post-note-spinner').html('');
						$('#page-task-new-note-contents').val('');
					});
				});

				function setup_edit_note() {
					$('.task-note').off('click');
					$('.task-note').on('click', function() {
						$('.task-note').off('click');
						var id = $(this).prop('id').split('-note')[0];
						$('#' + id + '-note').html('<center><img src="/static/media/loading.gif"></img></center>');
						api.notes.get_by_id(id, function(note) {
							var html = '';
							html += '<h4>Edit Note:</h4>';
							html += '<textarea id="' + note.id + '-edit-note" rows="6">';
							html += note.contents;
							html += '</textarea>';
							html += '<a id="page-task-submit-edit-note" class="button right">Update</a>';
							html += '<a id="page-task-cancel-edit-note" class="button">Cancel</a>';
							$('#' + id + '-note').html(html);

							$('#page-task-cancel-edit-note').off('click');
							$('#page-task-cancel-edit-note').on('click', function() {
								$('#page-task-cancel-edit-note').off('click');
								var html = '';
								html += '<b>' + note.author.first + ' ' + note.author.last + '</b>';
								html += '<i class="right">' + note.modified_datetime.split('.')[0] + '</i>';
								html += '<div class="indent">'
								html += note.contents;
								html += '</div>';
								$('#' + id + '-note').html(html);
								///// MEGA MOTHER FUCKING HACK BITCHES /////
								window.setTimeout( function() {
									setup_edit_note();
									}, 
									500
								);
							});
							
							$('#page-task-submit-edit-note').off('click');
							$('#page-task-submit-edit-note').on('click', function() {
								$('#page-task-submit-edit-note').off('click');
								var pyaload = {
									contents: $('#' + id + '-edit-note').val()
								};
								api.notes.update(id, pyaload, function(_note) {
									var html = '';
									html += '<b>' + _note.author.first + ' ' + _note.author.last + '</b>';
									html += '<i class="right">' + _note.modified_datetime.split('.')[0] + '</i>';
									html += '<div class="indent">'
									html += _note.contents;
									html += '</div>';
									$('#' + id + '-note').html(html);
									///// MEGA MOTHER FUCKING HACK BITCHES /////
									window.setTimeout( function() {
										setup_edit_note();
										}, 
										500
									);
								});
							});

						});
					});
				}

				setup_edit_note();

			});

		});

	};

	this.get_page = function() {
		if ( window.location.hash == '' )
			return null;
		return window.location.hash.split('#/')[1];
	}

	this.display_page = function(page_name, from_hash_change, id) {
		
		// scroll to top
		// taken from:
		//	https://stackoverflow.com/a/4210804
		$(function() {
   			$('body').scrollTop(0);
		});

		//console.log('Site.display_page(), page_name = ', page_name);
        page_name = page_name.split('?')[0];
        if ( from_hash_change != true ) {
            if( window.location.hash.split('?')[0].substr(2) != page_name ) {
                //console.log('Site.display_page(), hash change to: ', '/' + page_name);
                var afters = '';
                if ( typeof(id) != 'undefined' ) {
                	afters = '?id=' + id;
                }
                window.location.hash = '/' + page_name + afters;
                // we've been called directly.  we'll return here and let the 
                // window.onhashchange function to call us
                return;
            }
        }

        var loading_html = '<center><img src="/static/media/loading.gif"></img></center>';

        var pages = [
			'projects',
			'new-project',
			'project',
			'milestones',
			'milestone',
			'tasks',
			'new-task',
			'task',
			'settings',
		];

        for(var i=0;i<pages.length;i++) {
        	//console.log('hiding ' + pages[i]);
			$('#page-' + pages[i]).hide();
			//$('#page-' + pages[i] + '-contents').html(loading_html);
        }

		if ( pages.indexOf(page_name) >= 0 ) {
        	$('#page-' + page_name).show();
        }
        else {
        	//$('#page-projects').show();
        	window.location = '/#/projects';
        }

        switch(page_name) {
        	case 'projects':
        		this.load_projects();
        		break;
        	case 'new-project':
        		this.load_new_project();
        		break;
        	case 'project':
        		this.load_project();
        		break;
        	case'tasks':
        		break;
        	case'new-task':
        		this.load_new_task();
        		break;
        	case'task':
        		this.load_task();
        		break;
        	default:
        		break;
        };
	}

	this.install_hash_handler = function() {
        console.log('Site.install_hash_handler()');
        var that = this;
        window.onhashchange = function() {
            console.log('Router.onhashchange()');
            var _page_name = window.location.hash.substr(2);
            that.display_page(_page_name, true);
        }
    };

	this.init = function() {

		this.install_hash_handler();
		
		var current_page = this.get_page();
		if( current_page == null )
			current_page = 'projects';
		this.display_page(current_page, true);

		console.log('Site.init() complete.');
	};

}